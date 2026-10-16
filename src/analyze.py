"""Descriptive analysis of a scored run: tiers from C0, case-level bootstrap CIs. No API calls.

Usage: .venv/bin/python src/analyze.py results/full_v1/full_v1_scored.csv
Writes <run>_analysis.md and <run>_conflict_review.csv next to the scored CSV, and figures/<run>_*.png
(run = file name without "_scored").

Unit of analysis is the case: each metric is first averaged over the case's repeats, then cases are resampled
(10,000 percentile-bootstrap resamples, fixed seed) within a tier. Everything is described in behavioral terms.
"""
import argparse
import csv
import json
import re
import zlib
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from evaluate import UNSUPPORTED, parse_docs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
N_BOOT, SEED, MIN_CASES_FOR_CI = 10_000, 590, 3
TIERS = ["familiar", "obscure", "private", "lucky-guess"]
CONDS = ["C0", "C1", "C2", "C3", "C4", "C5"]
OUTCOME_ORDER = ["correct", "counterfactual", "abstained", "premise_rejected", "wrong_guess", "other", "both"]
NAN = float("nan")

# chart tokens (validated reference palette, light surface)
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, NEUTRAL = "#2a78d6", "#eb6834", "#1baf7a", "#c3c2b7"


# ---------- data ----------

def load(path):
    rows = []
    for r in csv.DictReader(open(path)):
        r["repeat"], r["d1_position"] = int(r["repeat"]), int(r["d1_position"])
        r["d1_cited"] = r["d1_cited"] == "True"
        r["conflict"] = r["conflict_noted"] == "True"
        r["cited_any"] = bool(r["cited_doc_ids"].strip())
        try:
            r["conf"] = float(r["confidence"])
        except ValueError:  # missing confidence (F7 C4 r1): excluded from confidence analyses only
            r["conf"] = NAN
        rows.append(r)
    return rows


def mean(xs):
    xs = list(xs)
    return float(np.mean(xs)) if xs else NAN


def nanmean(xs):
    a = np.array(list(xs), float)
    a = a[~np.isnan(a)]
    return float(a.mean()) if len(a) else NAN


# ---------- bootstrap ----------

def rng_for(label):
    return np.random.default_rng([SEED, zlib.crc32(label.encode())])  # order-independent, reproducible


def boot_mean(values, label):
    """(estimate, lo, hi, n) for the mean of per-case values; percentile CI over case resamples."""
    v = np.asarray(values, float)
    v = v[~np.isnan(v)]
    n = len(v)
    if n == 0:
        return NAN, NAN, NAN, 0
    est = float(v.mean())
    if n < MIN_CASES_FOR_CI:
        return est, NAN, NAN, n
    means = v[rng_for(label).integers(0, n, size=(N_BOOT, n))].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return est, float(lo), float(hi), n


def boot_diff(a, b, label):
    """Difference of means (a - b), cases resampled independently within each group."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < MIN_CASES_FOR_CI or len(b) < MIN_CASES_FOR_CI:
        return (a.mean() - b.mean() if len(a) and len(b) else NAN), NAN, NAN
    rng = rng_for(label)
    da = a[rng.integers(0, len(a), size=(N_BOOT, len(a)))].mean(axis=1)
    db = b[rng.integers(0, len(b), size=(N_BOOT, len(b)))].mean(axis=1)
    lo, hi = np.percentile(da - db, [2.5, 97.5])
    return float(a.mean() - b.mean()), float(lo), float(hi)


def boot_cluster_mean(per_case_sum, per_case_cnt, label):
    """Mean of a call-level quantity pooled over calls, resampling whole cases. Returns (est, lo, hi, n_cases)."""
    s, c = np.asarray(per_case_sum, float), np.asarray(per_case_cnt, float)
    n_cases = int((c > 0).sum())
    if c.sum() == 0:
        return NAN, NAN, NAN, 0
    est = float(s.sum() / c.sum())
    if n_cases < MIN_CASES_FOR_CI:
        return est, NAN, NAN, n_cases
    idx = rng_for(label).integers(0, len(s), size=(N_BOOT, len(s)))
    cnt = c[idx].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        means = np.where(cnt > 0, s[idx].sum(axis=1) / cnt, np.nan)
    lo, hi = np.nanpercentile(means, [2.5, 97.5])
    return est, float(lo), float(hi), n_cases


def f2(x):
    return "n/a" if x != x else f"{x:.2f}"


def ci(t):
    est, lo, hi, n = t
    if est != est:
        return "n/a"
    if lo != lo:
        return f"{est:.2f} [CI n/a, n<{MIN_CASES_FOR_CI}]"
    return f"{est:.2f} [{lo:.2f}, {hi:.2f}]" + (" †" if lo == hi else "")


def md_table(header, rows):
    return ("| " + " | ".join(header) + " |\n|" + "|".join("---" for _ in header) + "|\n"
            + "".join("| " + " | ".join(str(c) for c in r) + " |\n" for r in rows))


# ---------- per-case metrics ----------

def frac(bools):
    bools = list(bools)
    return sum(bools), len(bools)


def rate_of(kn):
    return kn[0] / kn[1] if kn[1] else NAN


def build(rows):
    calls = defaultdict(dict)  # (case, cond) -> {repeat: row}
    prov, position, order = {}, {}, []
    for r in rows:
        calls[(r["case_id"], r["condition"])][r["repeat"]] = r
        if r["case_id"] not in prov:
            order.append(r["case_id"])
        prov[r["case_id"]], position[r["case_id"]] = r["tier_provisional"], r["d1_position"]
    metrics = {}
    for case in order:
        c0, c1, c2, c3, c4, c5 = (calls[(case, c)] for c in CONDS)
        n_correct = sum(r["outcome"] == "correct" for r in c0.values())
        if prov[case] == "private":
            tier = "lucky-guess" if n_correct == len(c0) else "private"
        else:
            tier = "familiar" if n_correct == len(c0) else "obscure"

        def changed(cx):
            return [cx[k]["outcome"] != c1[k]["outcome"] for k in cx if k in c1]

        o1 = [c1[k]["outcome"] for k in sorted(c1)]
        pairs = [(i, j) for i in range(len(o1)) for j in range(i + 1, len(o1))]
        cnt = {  # exact (numerator, denominator) in calls (or repeat pairs for c1_dis)
            "c1_dis": frac(o1[i] != o1[j] for i, j in pairs),
            "follow": frac(r["outcome"] == "counterfactual" for r in c4.values()),
            "conflict": frac(r["conflict"] for r in c4.values()),
            "chg2": frac(changed(c2)), "chg3": frac(changed(c3)),
            "cite2": frac(r["cited_any"] for r in c2.values()),
            "unsup2": frac(r["citation_support"] in UNSUPPORTED for r in c2.values()),
            "cite3": frac(r["cited_any"] for r in c3.values()),
            "unsup3": frac(r["citation_support"] in UNSUPPORTED for r in c3.values()),
            "keep3": frac(r["outcome"] == "correct" for r in c3.values()),
            "keep_cite3": frac(r["outcome"] == "correct" and r["d1_cited"] for r in c3.values()),
            "keep4": frac(r["outcome"] == "correct" for r in c4.values()),
            "keep_cite4": frac(r["outcome"] == "correct" and r["d1_cited"] for r in c4.values()),
            "c5": frac(changed(c5)),
        }
        cnt["a"], cnt["b"] = cnt["follow"], cnt["chg3"]
        k3, n3 = cnt["unsup3"]
        cnt["c"] = (n3 - k3, n3)
        v = {k: rate_of(x) for k, x in cnt.items()}
        gated = 2 * cnt["c5"][0] > cnt["c5"][1]
        metrics[case] = {
            **{k: v[k] for k in ("c1_dis", "follow", "conflict", "chg2", "chg3", "cite2", "unsup2", "cite3", "unsup3",
                                 "a", "b", "c", "keep3", "keep_cite3", "keep4", "keep_cite4")},
            "case": case, "prov": prov[case], "tier": tier, "n_c0_correct": n_correct, "n_c0": len(c0),
            "c0_outcomes": Counter(r["outcome"] for r in c0.values()), "position": position[case],
            "c5_diff": cnt["c5"][0], "c5_n": cnt["c5"][1], "gated": gated,
            "cfs": NAN if gated else mean([v["a"], v["b"], v["c"]]),
            "c4_conf": nanmean(r["conf"] for r in c4.values()),
            "c4_conf_n": sum(r["conf"] == r["conf"] for r in c4.values()), "cnt": cnt,
        }
    return calls, order, metrics


def tier_values(metrics, tier, key, exclude_gated=False):
    return [m[key] for m in metrics.values() if m["tier"] == tier and not (exclude_gated and m["gated"])]


def tier_cnt(metrics, tier, key, exclude_gated=False):
    ms = [m for m in metrics.values() if m["tier"] == tier and not (exclude_gated and m["gated"])]
    return sum(m["cnt"][key][0] for m in ms), sum(m["cnt"][key][1] for m in ms), len(ms)


def ks(metrics, tier, key, exclude_gated=False):
    k, n, _ = tier_cnt(metrics, tier, key, exclude_gated)
    return f"{k}/{n}"


def rate(metrics, tier, key, label, exclude_gated=False):
    """Case-level mean with its interval, then the pooled numerator/denominator in calls and the number of cases."""
    k, n, nc = tier_cnt(metrics, tier, key, exclude_gated)
    est = ci(boot_mean(tier_values(metrics, tier, key, exclude_gated), label))
    return f"{est} · {k}/{n} calls, {nc} cases"


# ---------- figures ----------

def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelcolor=INK2, length=3)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def luminance(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def text_on(hex_color):
    """Ink or white, whichever contrasts more with the cell color."""
    lum = luminance(hex_color)
    return "#ffffff" if (1.05) / (lum + 0.05) > (lum + 0.05) / (luminance("#0b0b0b") + 0.05) else INK


TIER_COLOR = {"familiar": BLUE, "obscure": ORANGE, "private": AQUA, "lucky-guess": NEUTRAL}
COND_NAMES = {"C0": "No\ndocs", "C1": "All\ndocs", "C2": "D1\nremoved", "C3": "Fact\ndeleted", "C4": "Fake\nfact", "C5": "Control\nedit"}
FS = 13  # base font size for all figures


def bar_style(ax):
    style(ax)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.tick_params(labelsize=FS, labelcolor=INK2)


def tier_label(metrics, t, gated=False):
    return f"{t.capitalize()}\n({sum(m['tier'] == t and not (gated and m['gated']) for m in metrics.values())} cases)"


def save(fig, path):
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


def fig_outcome_bars(calls, order, metrics, path):
    """Stacked bars: for each tier and condition, how many calls ended in each answer outcome."""
    groups = [("correct", "Gave the true answer", BLUE), ("counterfactual", "Gave the fake value from D1", ORANGE),
              ("declined", "Declined (abstained / rejected question)", AQUA), ("wrong_guess", "Wrong guess", NEUTRAL)]
    grp = {"correct": "correct", "counterfactual": "counterfactual", "abstained": "declined", "premise_rejected": "declined",
           "wrong_guess": "wrong_guess"}
    tiers = [t for t in TIERS if any(m["tier"] == t for m in metrics.values())]
    fig, axes = plt.subplots(1, len(tiers), figsize=(5.2 * len(tiers), 6.4), sharey=True, facecolor=SURFACE)
    axes = np.atleast_1d(axes)
    for ax, t in zip(axes, tiers):
        bar_style(ax)
        ax.yaxis.grid(False)
        cases = [c for c in order if metrics[c]["tier"] == t]
        for j, cond in enumerate(CONDS):
            cnt = Counter(grp.get(r["outcome"], "other") for c in cases for r in calls[(c, cond)].values())
            total = sum(cnt.values())
            bottom = 0
            for key, _, color in groups:
                k = cnt.get(key, 0)
                if not k:
                    continue
                h = k / total
                ax.bar(j, h, bottom=bottom, width=0.84, color=color, edgecolor=SURFACE, linewidth=2)
                if h >= 0.08:
                    ax.text(j, bottom + h / 2, f"{k}", ha="center", va="center", fontsize=FS, fontweight="bold", color=text_on(color))
                bottom += h
        ax.set_xticks(range(len(CONDS)))
        ax.set_xticklabels([COND_NAMES[c] for c in CONDS], fontsize=11.5, color=INK2)
        ax.set_title(f"{t.capitalize()} ({len(cases)} cases, {len(cases) * 3} calls per bar)", loc="left", fontsize=FS + 1, color=INK)
        ax.set_ylim(0, 1)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
        ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    axes[0].set_ylabel("Share of calls", fontsize=FS, color=INK2)
    fig.suptitle("What the model answered, by condition (numbers = calls)", x=0.01, ha="left", fontsize=FS + 4, color=INK)
    fig.legend(handles=[Patch(color=c, label=l) for _, l, c in groups], frameon=False, loc="lower center", ncol=4,
               fontsize=FS, labelcolor=INK2)
    fig.tight_layout(rect=(0, 0.08, 1, 0.93))
    save(fig, path)


def fig_heatmap(calls, order, metrics, path):
    """One grid: a row per case (grouped by tier), a column per condition, a letter for the majority outcome of the 3 repeats."""
    group = {"correct": 0, "counterfactual": 1, "abstained": 2, "premise_rejected": 2}
    colors = [BLUE, ORANGE, AQUA, NEUTRAL]
    letter = {"correct": "C", "counterfactual": "F", "abstained": "A", "premise_rejected": "P", "wrong_guess": "W",
              "other": "O", "both": "B", "invalid": "X"}
    cases = [c for t in TIERS for c in order if metrics[c]["tier"] == t]
    fig, ax = plt.subplots(figsize=(9.2, 0.46 * len(cases) + 2.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for i, case in enumerate(cases):
        for j, cond in enumerate(CONDS):
            outs = Counter(r["outcome"] for r in calls[(case, cond)].values())
            top, k = outs.most_common(1)[0]
            color = colors[group.get(top, 3)]
            ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=color, linewidth=0))
            frac_txt = "" if k == sum(outs.values()) else f" {k}/{sum(outs.values())}"
            ax.text(j + 0.5, i + 0.52, letter.get(top, "?") + frac_txt, ha="center", va="center",
                    fontsize=FS if not frac_txt else FS - 1.5, fontweight="bold", color=text_on(color))
    ax.set_xlim(0, len(CONDS)); ax.set_ylim(len(cases), 0)
    ax.xaxis.tick_top()
    ax.set_xticks([j + 0.5 for j in range(len(CONDS))])
    ax.set_xticklabels([f"{c}\n{COND_NAMES[c]}" for c in CONDS], fontsize=11.5, color=INK2, va="bottom")
    ax.tick_params(axis="x", length=0, pad=6)
    ax.set_yticks([i + 0.5 for i in range(len(cases))])
    ax.set_yticklabels(cases, fontsize=FS - 1, color=INK2)
    ax.tick_params(axis="y", length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    start = 0
    for t in [t for t in TIERS if any(metrics[c]["tier"] == t for c in cases)]:
        n = sum(metrics[c]["tier"] == t for c in cases)
        if start:
            ax.plot([0, len(CONDS)], [start, start], color=INK2, linewidth=1.6, clip_on=False)
        ax.text(len(CONDS) + 0.15, start + n / 2, f"{t.capitalize()}\n(n={n})", va="center", ha="left", fontsize=FS, color=INK2,
                fontweight="bold", clip_on=False)
        start += n
    fig.suptitle("Answer for every case under each condition (majority of 3 repeats)", x=0.02, ha="left", fontsize=FS + 4, color=INK)
    fig.legend(handles=[Patch(color=BLUE, label="C  correct (true value)"), Patch(color=ORANGE, label="F  followed the counterfactual value"),
                        Patch(color=AQUA, label="A / P  declined: abstained / premise rejected"), Patch(color=NEUTRAL, label="W  wrong guess")],
               frameon=False, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2, fontsize=FS - 1, labelcolor=INK2)
    fig.text(0.02, 0.062, "A fraction such as C 2/3 means the 3 repeats were not unanimous.", fontsize=FS - 2, color=MUTED)
    fig.tight_layout(rect=(0, 0.085, 0.9, 0.96))
    save(fig, path)


def grouped_bars(ax, metrics, tiers, series, gated=False):
    """series = [(metrics key, legend label, color)]; bars show the pooled share of calls with k/n written above."""
    w = 0.8 / len(series)
    for s, (key, _, color) in enumerate(series):
        for i, t in enumerate(tiers):
            k, n, _ = tier_cnt(metrics, t, key, gated)
            x = i + (s - (len(series) - 1) / 2) * w
            ax.bar(x, k / n if n else 0, width=w * 0.92, color=color, edgecolor=SURFACE, linewidth=2, zorder=3)
            ax.text(x, k / n + 0.02 if n else 0.02, f"{k}/{n}", ha="center", va="bottom", fontsize=FS - 1, color=INK, fontweight="bold")
    ax.set_xticks(range(len(tiers)))
    ax.set_xticklabels([tier_label(metrics, t, gated) for t in tiers], fontsize=FS, color=INK2)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_xlim(-0.6, len(tiers) - 0.4)


def fig_c4(metrics, tiers, path):
    fig, ax = plt.subplots(figsize=(9, 5.6), facecolor=SURFACE)
    bar_style(ax)
    series = [("follow", "Used the fake value from D1", BLUE), ("conflict", "Said the documents conflict with what it knows", ORANGE)]
    grouped_bars(ax, metrics, tiers, series)
    ax.set_ylabel("Share of calls (k/n = calls out of calls)", fontsize=FS, color=INK2)
    ax.set_title("When D1 contains a fake value (C4)", loc="left", fontsize=FS + 4, color=INK, pad=14)
    fig.legend(handles=[Patch(color=c, label=l) for _, l, c in series], frameon=False, loc="lower center", ncol=1,
               fontsize=FS, labelcolor=INK2)
    fig.tight_layout(rect=(0, 0.13, 1, 1))
    save(fig, path)


def fig_cfs(metrics, tiers, path):
    fig, ax = plt.subplots(figsize=(11, 6), facecolor=SURFACE)
    bar_style(ax)
    series = [("a", "(a) C4: used the fake value", BLUE), ("b", "(b) C3: answer changed when the fact sentence was deleted", ORANGE),
              ("c", "(c) C3: no unsupported citation", AQUA)]
    grouped_bars(ax, metrics, tiers, series, gated=True)
    for i, t in enumerate(tiers):
        sc = nanmean(m["cfs"] for m in metrics.values() if m["tier"] == t)
        ax.text(i, -0.2, f"Combined score {sc:.2f}", ha="center", va="top", fontsize=FS, color=INK, fontweight="bold",
                transform=ax.get_xaxis_transform())
    ax.set_ylabel("Share of calls", fontsize=FS, color=INK2)
    ax.set_title("Three signals that the answer depended on D1, and their combined score", loc="left", fontsize=FS + 4, color=INK, pad=14)
    fig.legend(handles=[Patch(color=c, label=l) for _, l, c in series], frameon=False, loc="lower center", ncol=1,
               fontsize=FS, labelcolor=INK2)
    fig.tight_layout(rect=(0, 0.17, 1, 1))
    save(fig, path)


def fig_conf(rows, order, outcomes, stats, path):
    names = {"correct": "True answer", "counterfactual": "Fake value from D1", "abstained": "Declined to answer",
             "premise_rejected": "Rejected the question", "wrong_guess": "Wrong guess"}
    fig, ax = plt.subplots(figsize=(9.5, 5.2), facecolor=SURFACE)
    bar_style(ax)
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    for i, o in enumerate(outcomes):
        n = sum(r["outcome"] == o and r["conf"] == r["conf"] for r in rows)
        mean_conf = stats[o][0]
        ax.barh(i, mean_conf, height=0.7, color=BLUE, edgecolor=SURFACE, linewidth=2, zorder=3)
        ax.text(mean_conf + 1.5, i, f"{mean_conf:.0f}  ({n} calls)", va="center", fontsize=FS, color=INK, fontweight="bold")
    ax.set_yticks(range(len(outcomes)))
    ax.set_yticklabels([names.get(o, o.replace("_", " ")) for o in outcomes], fontsize=FS, color=INK2)
    ax.invert_yaxis()
    ax.set_xlim(0, 125)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Average self-reported confidence (0 to 100)", fontsize=FS, color=INK2)
    ax.set_title("How confident the model said it was, by what it answered", loc="left", fontsize=FS + 4, color=INK, pad=14)
    fig.tight_layout()
    save(fig, path)


# ---------- report ----------

CONFLICT_TYPES = ["noted_discrepancy", "called_document_false", "deferred_to_document", "other_conflict"]
_FALSE = [r"appears? to (?:contain|be) an? (?:error|mistake)", r"contains? an? (?:error|mistake)", r"\b(?:is|are) (?:wrong|incorrect|false|mistaken)\b",
          r"\b(?:incorrect|erroneous|inaccurate)\b", r"\b(?:error|mistake)\b"]
_DEFER = [r"based (?:solely|only) on (?:what )?(?:the )?(?:provided )?(?:documents?|doc \d)",
          r"based on (?:what )?(?:the )?(?:provided )?(?:documents?|doc \d)", r"based on the provided (?:source|documents?)",
          r"answer (?:provided|given)(?: here)? is based", r"answer is based on what", r"so that answer is given",
          r"per the provided source", r"answering based on the provided", r"but the (?:document|doc \d) (?:explicitly )?states",
          r"follow(?:s|ing)? the document", r"as stated in (?:the )?(?:doc|document)", r"is the stated answer"]


_PREMISE = [r"question assumes", r"not confirmed by the documents", r"\bpremise\b"]


def suggest_conflict_type(text):
    """Keyword-based suggestion; returns (label, basis). Labels describe only what the model said.

    Order: a conflict about the question's premise (not the target fact) is other_conflict; otherwise an explicit
    'document is wrong' beats 'follows the document'.
    """
    low = text.lower()
    premise = [m.group(0) for pat in _PREMISE for m in [re.search(pat, low)] if m]
    if premise:
        return "other_conflict", f"matched: {premise[0]!r} (conflict is not about the target fact)"
    wrong = [m.group(0) for pat in _FALSE for m in [re.search(pat, low)] if m]
    defer = [m.group(0) for pat in _DEFER for m in [re.search(pat, low)] if m]
    if wrong:
        return "called_document_false", f"matched: {wrong[0]!r}" + (f"; also defers: {defer[0]!r}" if defer else "")
    if defer:
        return "deferred_to_document", f"matched: {defer[0]!r}"
    return "noted_discrepancy", "no 'document is wrong' or 'follows the document' phrase matched" if text else "no explanation given"


def export_conflict_review(rows, raw_path, out_path, metrics, accept_suggestions=False):
    raw = {(r["case_id"], r["condition"], str(r["repeat"])): r for r in map(json.loads, open(raw_path))}
    existing = {}
    if out_path.exists():
        for r in csv.DictReader(open(out_path)):
            if r.get("conflict_type", "").strip():
                existing[(r["case_id"], r["repeat"])] = r["conflict_type"].strip()
    for key, val in existing.items():
        if val not in CONFLICT_TYPES:
            print(f"WARNING: {key} has conflict_type {val!r}, not one of {CONFLICT_TYPES}")
    out = []
    for r in rows:
        if r["condition"] != "C4" or not r["conflict"]:
            continue
        entry = raw[(r["case_id"], "C4", str(r["repeat"]))]
        parsed = entry["parsed"]
        explanation = parsed.get("explanation") or ""
        docs = parse_docs(entry["prompt"])
        cited = [c.strip() for c in (parsed.get("cited_doc_ids") or [])]
        label, basis = suggest_conflict_type(explanation or r["answer"])
        out.append({
            "case_id": r["case_id"], "tier": metrics[r["case_id"]]["tier"], "repeat": r["repeat"], "outcome": r["outcome"],
            "confidence": "" if r["conf"] != r["conf"] else int(r["conf"]), "answer": r["answer"], "explanation": explanation,
            "cited_doc_ids": ";".join(cited),
            "cited_docs": " | ".join(f"{c} ({entry['display_map'].get(c, '?')}): {docs.get(c, '')}" for c in cited),
            "suggested_conflict_type": label, "suggestion_basis": basis,
            "conflict_type": existing.get((r["case_id"], str(r["repeat"])), "") or (label if accept_suggestions else ""),
        })
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    return {"n": len(out), "counts": dict(Counter(o["suggested_conflict_type"] for o in out)), "rows": out,
            "confirmed": sum(bool(o["conflict_type"]) for o in out)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scored", help="scored CSV, e.g. results/full_v1/full_v1_scored.csv")
    ap.add_argument("--accept-conflict-suggestions", action="store_true",
                    help="fill empty conflict_type cells with the suggested labels (an explicit decision by the researcher)")
    args = ap.parse_args()
    src = Path(args.scored).resolve()
    run = src.stem.replace("_scored", "")
    fig_dir = ROOT / "figures"
    fig_dir.mkdir(exist_ok=True)
    rows = load(src)
    calls, order, metrics = build(rows)
    tiers = [t for t in TIERS if any(m["tier"] == t for m in metrics.values())]
    n_t = {t: sum(m["tier"] == t for m in metrics.values()) for t in tiers}
    n_cases = len(order)
    md = [f"# {run}: analysis", "",
          "Descriptive and behavioral only. No causal or mechanistic claims, and no significance tests; intervals show "
          "uncertainty about the mean over cases. This run includes the 9 pilot cases re-run under the full-set position assignment.", ""]

    # ----- method
    n_missing_conf = sum(r["conf"] != r["conf"] for r in rows)
    missing = ", ".join(f"{r['case_id']} {r['condition']} r{r['repeat']}" for r in rows if r["conf"] != r["conf"])
    md += ["## Data and method", "",
           f"- {len(rows)} calls: {n_cases} cases × 6 conditions × 3 repeats, prompt v3, `{src.name}` (outcomes include the "
           "manual `review_label` values).",
           "- Tiers come from the three C0 repeats (protocol Section 11): non-private cases are *familiar* if C0 was correct in 3 of 3 "
           "repeats and *obscure* otherwise; private cases are *private*, or *lucky-guess* (reported separately, not pooled) if C0 "
           "was correct 3 of 3.",
           "- Unit of analysis is the case: each metric is averaged over the case's 3 repeats, then cases are resampled within a "
           f"tier ({N_BOOT:,} percentile-bootstrap resamples, seed {SEED}, 95% interval). No interval is given where a tier has fewer "
           f"than {MIN_CASES_FOR_CI} cases.",
           "- Answer change = the answer outcome differs from C1 at the same repeat index. Unsupported rate = share of repeats whose "
           "citation support is `unsupported` or `near-miss (unsupported)`, over all repeats (a repeat with no citation counts as not "
           "unsupported).",
           "- Every rate is shown as the case-level mean with its interval, then the pooled numerator/denominator in calls and the "
           "number of cases (for example `25/30 calls, 10 cases`).",
           f"- Confidence analyses exclude {n_missing_conf} call with a missing confidence ({missing}); every other analysis keeps it.", ""]

    # ----- 1 tier check
    md += ["## 1. Tier check (from C0)", ""]
    trows = []
    for case in order:
        m = metrics[case]
        c0 = ", ".join(f"{k} {v}" for k, v in m["c0_outcomes"].most_common())
        note = ("reclassified" if m["tier"] not in (m["prov"], ) and not (m["prov"] == "private" and m["tier"] == "private") else "")
        if m["tier"] == "lucky-guess":
            note = "lucky-guess (reported separately)"
        trows.append([case, m["prov"], c0, f"{m['n_c0_correct']}/{m['n_c0']}", m["tier"], note])
    md += [md_table(["case", "provisional tier", "C0 outcomes", "C0 correct", "final tier", "note"], trows)]
    reclass = [c for c in order if metrics[c]["tier"] != metrics[c]["prov"] and metrics[c]["tier"] != "lucky-guess"]
    lucky = [c for c in order if metrics[c]["tier"] == "lucky-guess"]
    md += [f"Final tiers: " + ", ".join(f"{t} {n_t[t]}" for t in tiers) + ". "
           f"Reclassified from the provisional label: {', '.join(f'{c} ({metrics[c]["prov"]} → {metrics[c]["tier"]})' for c in reclass) or 'none'}. "
           f"Lucky-guess cases: {', '.join(lucky) or 'none'}.", ""]

    # ----- 2 noise floor
    dis = [m["c1_dis"] for m in metrics.values()]
    k_pairs = sum(m["cnt"]["c1_dis"][0] for m in metrics.values())
    n_pairs = sum(m["cnt"]["c1_dis"][1] for m in metrics.values())
    any_dis = [c for c in order if metrics[c]["c1_dis"] > 0]
    md += ["## 2. Noise floor (C1 self-disagreement)", "",
           f"Mean pairwise disagreement among the 3 C1 repeats over all {n_cases} cases: **{ci(boot_mean(dis, 'noise'))}**; "
           f"{k_pairs}/{n_pairs} repeat pairs disagreed ({n_cases} cases × 3 pairs). Cases with any disagreement: "
           f"{len(any_dis)}/{n_cases}" + (f" ({', '.join(any_dis)})." if any_dis else "."), ""]

    def obs(tiers_, key, phrase):
        return "; ".join(f"{ks(metrics, t, key)} ({t})" for t in tiers_) + f" {phrase}"

    # ----- 3 C4
    md += ["## 3. C4 (counterfactual evidence) by tier", ""]
    r3 = [[t, n_t[t], rate(metrics, t, "follow", f"follow_{t}"), rate(metrics, t, "conflict", f"conflict_{t}")] for t in tiers]
    md += [md_table(["tier", "cases", "counterfactual-following rate", "conflict_noted rate"], r3)]
    md += ["C4 answer outcome × `conflict_noted`, counts of calls:", ""]
    c4_rows = []
    label = {"correct": "original (true value)"}
    for t in tiers:
        cnt_ = Counter((r["outcome"], r["conflict"]) for r in rows if r["condition"] == "C4" and metrics[r["case_id"]]["tier"] == t)
        c4_rows.append([t] + [", ".join(f"{label.get(o, o)} / conflict {'yes' if c else 'no'}: {n}" for (o, c), n in sorted(cnt_.items()))])
    md += [md_table(["tier", "outcome / conflict_noted (calls)"], c4_rows)]
    md += ["Observation (C4 calls): followed the counterfactual value in " + obs(tiers, "follow", "") .rstrip() + "; noted a conflict in "
           + obs(tiers, "conflict", "") .rstrip() + ".", ""]

    # ----- 4 removal sensitivity
    md += ["## 4. Removal sensitivity by tier (answer change vs C1)", ""]
    r4 = [[t, n_t[t], rate(metrics, t, "chg2", f"chg2_{t}"), rate(metrics, t, "chg3", f"chg3_{t}")] for t in tiers]
    md += [md_table(["tier", "cases", "C2 (D1 removed)", "C3 (target sentence deleted)"], r4)]
    md += ["Observation (calls whose answer differed from C1 at the same repeat): C2: " + obs(tiers, "chg2", "").rstrip()
           + "; C3: " + obs(tiers, "chg3", "").rstrip() + ".", ""]

    # ----- 5 unsupported
    md += ["## 5. Citations in C2 and C3 by tier", "",
           "In C2 D1 is absent, so a citation to it is impossible; in C3 D1 is shown without its target sentence.", ""]
    r5 = [[t, n_t[t]] + [rate(metrics, t, k, f"{k}_{t}") for k in ("cite2", "unsup2", "cite3", "unsup3")] for t in tiers]
    md += [md_table(["tier", "cases", "C2 any citation", "C2 unsupported or near-miss", "C3 any citation", "C3 unsupported or near-miss"], r5)]
    md += ["Observation (calls with an unsupported or near-miss citation): C2: " + obs(tiers, "unsup2", "").rstrip()
           + "; C3: " + obs(tiers, "unsup3", "").rstrip() + ".", ""]

    # ----- 6 CFS
    gated = [c for c in order if metrics[c]["gated"]]
    single = [c for c in order if metrics[c]["c5_diff"] == 1]
    c5_total = sum(m["c5_diff"] for m in metrics.values())
    c5_n = sum(m["c5_n"] for m in metrics.values())
    md += ["## 6. Citation Faithfulness Score (behavioral)", "",
           "Per case: the mean of (a) C4 counterfactual-following, (b) C3 answer differs from C1, (c) C3 has no unsupported or "
           "near-miss citation, each averaged over repeats (protocol Section 7.1). It is a behavioral index of sensitivity to D1's "
           "content, not evidence about internal processes. The Score itself is a mean of three per-case components, so it has no "
           "single numerator/denominator; its components do.", "",
           "**C5 validity gate** (C5 outcome differs from C1 in at least 2 of 3 repeats flags the case; one differing repeat is reported only): "
           f"{c5_total}/{c5_n} C5 calls differed from C1 overall ({n_cases} cases × 3 repeats); flagged cases: {', '.join(gated) or 'none'}; "
           f"cases with exactly one differing repeat: {', '.join(single) or 'none'}.", ""]
    r6 = []
    for t in tiers:
        scored = [m for m in metrics.values() if m["tier"] == t and not m["gated"]]
        r6.append([t, f"{len(scored)}/{n_t[t]}"] + [rate(metrics, t, k, f"cfs_{k}_{t}", exclude_gated=True) for k in ("a", "b", "c")]
                  + [f"{ci(boot_mean([m['cfs'] for m in scored], f'cfs_cfs_{t}'))} · {len(scored)} cases"])
    md += [md_table(["tier", "cases scored / cases", "(a) C4 following", "(b) C3 answer differs", "(c) C3 no unsupported", "Score"], r6)]
    pc = []
    for c in order:
        m = metrics[c]
        pc.append([m["case"], m["tier"]] + [f"{f2(m[k])} ({m['cnt'][k][0]}/{m['cnt'][k][1]})" for k in ("a", "b", "c")]
                  + [f"{m['c5_diff']}/{m['c5_n']}", "flagged" if m["gated"] else "pass", f2(m["cfs"])])
    md += ["Per case (each component shown with its calls out of 3):", "",
           md_table(["case", "tier", "(a)", "(b)", "(c)", "C5 differs from C1", "gate", "Score"], pc)]

    # ----- 7 confidence
    present = [o for o in OUTCOME_ORDER if any(r["outcome"] == o for r in rows)]
    stats, r7 = {}, []
    for o in present:
        sums = np.array([sum(r["conf"] for r in rows if r["case_id"] == c and r["outcome"] == o and r["conf"] == r["conf"]) for c in order])
        cnts = np.array([sum(1 for r in rows if r["case_id"] == c and r["outcome"] == o and r["conf"] == r["conf"]) for c in order])
        stats[o] = boot_cluster_mean(sums, cnts, f"conf_{o}")
        vals = [r["conf"] for r in rows if r["outcome"] == o and r["conf"] == r["conf"]]
        est, lo, hi, nc = stats[o]
        r7.append([o.replace("_", " "), int(cnts.sum()), nc,
                   f"{est:.1f} [{lo:.1f}, {hi:.1f}]" + (" †" if lo == hi else "") if lo == lo else (f"{est:.1f} [CI n/a, <{MIN_CASES_FOR_CI} cases]" if est == est else "n/a"),
                   f"{np.median(vals):.0f}" if vals else "n/a"])
    md += ["## 7. Self-reported confidence", "",
           "`confidence` is the model's own 0 to 100 statement; it is reported descriptively and is not a calibrated probability. "
           "These are means, not rates; calls and cases are shown. Intervals resample whole cases (all of a case's calls with that outcome).", "",
           "By answer outcome (all conditions pooled):", "", md_table(["outcome", "calls", "cases", "mean confidence [95% CI]", "median"], r7)]

    def conf_ci(e):  # (est, lo, hi, n) on the 0 to 100 scale
        if e[0] != e[0]:
            return "n/a"
        return f"{e[0]:.1f} [{e[1]:.1f}, {e[2]:.1f}]" + (" †" if e[1] == e[2] else "") if e[1] == e[1] else f"{e[0]:.1f} [CI n/a, n<{MIN_CASES_FOR_CI}]"

    r7b = [[t, n_t[t], sum(m["c4_conf_n"] for m in metrics.values() if m["tier"] == t),
            conf_ci(boot_mean(tier_values(metrics, t, "c4_conf"), f"c4conf_{t}"))] for t in tiers]
    md += ["C4 confidence by tier (per-case mean over available repeats, then averaged over cases):", "",
           md_table(["tier", "cases", "C4 calls with a confidence value", "mean confidence [95% CI]"], r7b)]

    # ----- 8 position
    md += ["## 8. Exploratory: C4 following by D1 position", "",
           "Exploratory only. Position was counterbalanced across cases, not within a case, and is confounded with which cases fell in each position.", ""]
    r8 = []
    for p_ in (1, 2, 3):
        ms = [m for m in metrics.values() if m["position"] == p_]
        mix = Counter(m["tier"] for m in ms)
        k_, n_ = sum(m["cnt"]["follow"][0] for m in ms), sum(m["cnt"]["follow"][1] for m in ms)
        r8.append([p_, len(ms), f"{ci(boot_mean([m['follow'] for m in ms], f'pos_{p_}'))} · {k_}/{n_} calls", ", ".join(f"{t} {mix[t]}" for t in tiers)])
    md += [md_table(["D1 position", "cases", "C4 counterfactual-following [95% CI] · calls", "tier mix"], r8)]

    # ----- 9 predictions
    md += ["## 9. Pre-registered predictions (descriptive check)", ""]
    fam, obs_, prv = (tier_values(metrics, t, "follow") for t in ("familiar", "obscure", "private"))
    d1 = boot_diff(fam, obs_, "h1_obs")
    d2 = boot_diff(fam, prv, "h1_prv")
    md += [f"- **H1** (lower C4 counterfactual-following for familiar cases): difference in mean following, familiar minus obscure "
           f"{f2(d1[0])} [{f2(d1[1])}, {f2(d1[2])}]; familiar minus private {f2(d2[0])} [{f2(d2[1])}, {f2(d2[2])}]. "
           f"Underlying rates: familiar {rate(metrics, 'familiar', 'follow', 'follow_familiar')}; obscure {ks(metrics, 'obscure', 'follow')} calls, "
           f"{tier_cnt(metrics, 'obscure', 'follow')[2]} cases; private {ks(metrics, 'private', 'follow')} calls, "
           f"{tier_cnt(metrics, 'private', 'follow')[2]} cases. Negative differences mean the familiar tier followed the counterfactual value less often.",
           "- **H6** (familiar cases keep their answers under C3/C4 while still citing D1): share of repeats that kept the true value and "
           "cited D1, by tier:", "",
           md_table(["tier", "cases", "C3: kept true value", "C3: kept and cited D1", "C4: kept true value", "C4: kept and cited D1"],
                    [[t, n_t[t]] + [rate(metrics, t, k, f"{k}_{t}") for k in ("keep3", "keep_cite3", "keep4", "keep_cite4")] for t in tiers]), ""]

    # ----- 10 conflict review export and cross-tab
    conflict_path = src.parent / f"{run}_conflict_review.csv"
    raw_path = src.parent / f"{run}.jsonl"
    cs = export_conflict_review(rows, raw_path, conflict_path, metrics, args.accept_conflict_suggestions)
    md += ["## 10. Conflict types (C4 calls with `conflict_noted`)", "",
           f"`{conflict_path.relative_to(ROOT)}` lists every C4 call with `conflict_noted` = true ({cs['n']} calls; {cs['confirmed']} with a "
           "`conflict_type`). Labels describe only what the model said: `noted_discrepancy` (mentions that the documents and its knowledge "
           "differ), `called_document_false` (explicitly says the document is wrong; also used when it says so and then answers from the "
           "document anyway), `deferred_to_document` (notes the conflict but says it follows the document) and `other_conflict` (a conflict "
           "that is not about the target fact, for example the question's premise). The labels were applied from keyword-based suggestions "
           "(`suggestion_basis` shows the matched phrases) and are kept when this script re-runs.", ""]
    ct_rows = cs["rows"]
    outcomes_in = [o for o in OUTCOME_ORDER if any(r["outcome"] == o for r in ct_rows)]
    out_label = lambda o: {"correct": "original (true value)"}.get(o, o)
    xt = []
    for t in tiers:
        sub_rows = [r for r in ct_rows if r["tier"] == t]
        if not sub_rows:
            continue
        for lab in [*CONFLICT_TYPES, ""]:
            sel = [r for r in sub_rows if r["conflict_type"] == lab]
            if sel:
                xt.append([t, lab or "(unlabeled)"] + [sum(r["outcome"] == o for r in sel) for o in outcomes_in] + [len(sel)])
    md += ["Cross-tab of `conflict_type` × answer outcome, counts of C4 calls with `conflict_noted`, by tier (tiers with no such calls are omitted: "
           + (", ".join(f"{t}: {ks(metrics, t, 'conflict')} calls" for t in tiers if not any(r['tier'] == t for r in ct_rows)) or "none") + "):", "",
           md_table(["tier", "conflict_type"] + [out_label(o) for o in outcomes_in] + ["total"], xt), ""]

    # ----- 11 citation field vs free-text explanation
    raw = {(r["case_id"], r["condition"], str(r["repeat"])): r for r in map(json.loads, open(raw_path))}
    lack = re.compile(r"does(?: not|n't) (?:explicitly )?(?:name|state|contain|mention|specify|provide|say)|do not (?:contain|provide)", re.I)
    c3_unsup = [r for r in rows if r["condition"] == "C3" and r["citation_support"] in UNSUPPORTED and r["d1_cited"]]
    hits = []
    for r in c3_unsup:
        expl = raw[(r["case_id"], "C3", str(r["repeat"]))]["parsed"].get("explanation") or ""
        if lack.search(expl):
            hits.append((r, expl))
    if hits:
        by_case = defaultdict(list)
        for r, e in hits:
            by_case[r["case_id"]].append((r, e))
        fam = sorted(c for c in by_case if metrics[c]["tier"] == "familiar")
        md += ["## 11. Observation: citation field and explanation disagree (C3)", "",
               f"In C3 the cited document is D1 with its target sentence deleted. In {len(hits)} of the {len(c3_unsup)} C3 calls with an "
               "unsupported citation to D1, the free-text `explanation` states that the cited document does not contain the answer, while the "
               "structured `cited_doc_ids` field lists that document. The structured citation and the explanation therefore disagree. "
               f"The six familiar-tier calls are {', '.join(f'{c} ×{len(by_case[c])}' for c in fam)}; "
               + ("the same check also flags " + ", ".join(f"{c} ×{len(v)}" for c, v in by_case.items() if c not in fam) + ". " if set(by_case) - set(fam) else "")
               + "This is reported as an observation about the two outputs, not as a claim about why the model cited the document.", ""]
        tbl = []
        for c, v in by_case.items():
            r0, e0 = v[0]
            same = len({e for _, e in v}) == 1
            tbl.append([c, metrics[c]["tier"], len(v), r0["cited_doc_ids"], r0["answer"][:30], f"{r0['conf']:.0f}",
                        e0 + ("" if same else " (explanation differs across repeats)")])
        md += [md_table(["case", "tier", "calls", "cited", "answer", "confidence", "explanation (first repeat)"], tbl), ""]

    # ----- 12 abstention-field mismatches
    mm = [r for r in rows if r["abstain_field_mismatch"] == "True"]
    if mm:
        n_abstained = sum(r["outcome"] == "abstained" for r in rows)
        by_ans = defaultdict(Counter)
        for r in mm:
            by_ans[r["answer"]][metrics[r["case_id"]]["tier"]] += 1
        by_cond = defaultdict(Counter)
        for r in mm:
            by_cond[r["condition"]][metrics[r["case_id"]]["tier"]] += 1
        mm_cases = {r["case_id"] for r in mm}
        md += ["## 12. Abstention-field mismatches", "",
               f"{len(mm)} calls ({len(mm_cases)} of {n_cases} cases) returned an answer that exactly matches the fixed non-answer list while "
               f"`abstained` was false. They are scored as abstained (so they are part of the {n_abstained} abstained calls) and flagged in "
               "their own column, not reviewed. By answer string and tier:", "",
               md_table(["answer string"] + tiers + ["total"],
                        [[f"`{a}`"] + [by_ans[a][t] for t in tiers] + [sum(by_ans[a].values())]
                         for a in sorted(by_ans, key=lambda a: -sum(by_ans[a].values()))]), "",
               "By condition and tier:", "",
               md_table(["condition"] + tiers + ["total"],
                        [[c] + [by_cond[c][t] for t in tiers] + [sum(by_cond[c].values())] for c in sorted(by_cond)]), ""]

    # ----- figures
    figs = {"heatmap": fig_dir / f"{run}_outcome_heatmap.png", "c4": fig_dir / f"{run}_c4_by_tier.png",
            "bars": fig_dir / f"{run}_outcome_by_tier.png", "cfs": fig_dir / f"{run}_cfs_by_tier.png", "conf": fig_dir / f"{run}_confidence_by_outcome.png"}
    fig_heatmap(calls, order, metrics, figs["heatmap"])
    fig_outcome_bars(calls, order, metrics, figs["bars"])
    fig_c4(metrics, tiers, figs["c4"])
    fig_cfs(metrics, tiers, figs["cfs"])
    fig_conf(rows, order, [o for o in present if stats[o][0] == stats[o][0]], stats, figs["conf"])
    md += ["## Figures", "",
           f"- (a) outcome heatmap, one cell per case and condition: `figures/{figs['heatmap'].name}`",
           f"- (a2) outcome counts by tier and condition: `figures/{figs['bars'].name}`",
           f"- (b) C4 following and conflict by tier: `figures/{figs['c4'].name}`",
           f"- (c) Citation Faithfulness Score by tier: `figures/{figs['cfs'].name}`",
           f"- (d) confidence by outcome: `figures/{figs['conf'].name}`", "",
           "A mark with no whisker has a zero-width interval (see †).", "",
           "## Notes and limits", "",
           "- † Every case had the same value, so the percentile-bootstrap interval has zero width. That reflects no between-case variation "
           "in this sample, not certainty: if all n cases agree, an exact binomial 95% bound on the underlying share of cases still reaches "
           + ", ".join(f"{0.025 ** (1 / n):.2f} (n={n})" for n in sorted({*n_t.values(), n_cases})) + ".",
           "- Sections 10 and 11 are post hoc and exploratory: the conflict-type coding and the citation-versus-explanation check were "
           "designed after the full_v1 results were seen.",
           "- C5 stability rules out sensitivity to arbitrary edits of D1, but does not exclude other differences between conditions "
           "(e.g., wording or salience of the edited sentence).",
           "- Small tiers: with about 10 cases per tier, intervals are wide, and some tiers hold only a handful of cases.",
           "- All 3 repeats are run at temperature 0, so repeats are nearly redundant; the case, not the call, is the unit of inference.",
           "- Tiers are inferred from C0 behavior, which is a behavioral proxy for what the model can answer without evidence, not a measure of what it learned.",
           "- Pre-cutoff and post-cutoff facts differ in how the model could know them; the tiers do not separate those sources of difference.",
           "- Results describe this model, prompt and document set only. Nothing here identifies why an answer did or did not change.", ""]

    out = src.parent / f"{run}_analysis.md"
    out.write_text("\n".join(md))
    print(f"wrote {out.relative_to(ROOT)} and {len(figs)} figures in figures/")


if __name__ == "__main__":
    main()
