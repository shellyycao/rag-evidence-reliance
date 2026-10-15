"""Run pilot_conditions x repeats through Bedrock. Use --dry-run first: it makes zero API calls.

Real calls require --confirm.
"""
import argparse
import json
import sys
from pathlib import Path

from logging_utils import append_record, call_key, estimate_cost, load_done, log_path, make_record
from prompts import INFERENCE_CONFIG, PROMPT_VERSION, TOOL_CONFIG, build_prompt
from smoke_test import MODEL_ID, PRICE_IN_PER_M, PRICE_OUT_PER_M, PROFILE, REGION

CONDITIONS_PATH = Path(__file__).resolve().parent.parent / "data" / "pilot_conditions.jsonl"

# Dry-run token estimate, calibrated on the one measured call (C1, 3 docs: 902 in / 106 out):
# the forced tool-use schema adds a fixed overhead; the rest is roughly 4 characters per token.
TOOL_OVERHEAD_TOKENS = 750
CHARS_PER_TOKEN = 4
EST_OUTPUT_TOKENS = 110
MAX_CONSECUTIVE_ERRORS = 3


def load_conditions():
    return [json.loads(line) for line in CONDITIONS_PATH.read_text().splitlines() if line.strip()]


def jobs(conditions, repeats):
    """All (repeat, condition-line, prompt) calls. Repeat is the outer loop so a stopped run
    leaves complete repeat sets."""
    return [(r, c, build_prompt(c["question"], c["docs"]))
            for r in range(1, repeats + 1) for c in conditions]


def estimate(prompt):
    tokens_in = TOOL_OVERHEAD_TOKENS + len(prompt) / CHARS_PER_TOKEN
    return tokens_in, EST_OUTPUT_TOKENS, estimate_cost(tokens_in, EST_OUTPUT_TOKENS, PRICE_IN_PER_M, PRICE_OUT_PER_M)


def dry_run(all_jobs, path):
    done = load_done(path)
    todo = [j for j in all_jobs if call_key(j[1]["case_id"], j[1]["condition"], j[0]) not in done]
    first = all_jobs[0][1]["case_id"]
    print(f"prompt version: {PROMPT_VERSION} | model: {MODEL_ID} | settings: {INFERENCE_CONFIG}")
    for want in ("C0", "C1", "C4"):
        r, c, prompt = next(j for j in all_jobs if j[1]["case_id"] == first and j[1]["condition"] == want and j[0] == 1)
        print(f"\n===== EXAMPLE: case {c['case_id']} {want} (repeat {r}) | D1 position {c['d1_position']} "
              f"| map { {d['display_id']: d['internal'] for d in c['docs']} } =====")
        print(prompt)
    est = [estimate(p) for _, _, p in todo]
    total = sum(e[2] for e in est)
    print("\n===== DRY RUN SUMMARY (no API calls made) =====")
    print(f"calls in plan: {len(all_jobs)}  |  already logged (skipped): {len(all_jobs) - len(todo)}  |  to run: {len(todo)}")
    print(f"estimated tokens: in~{sum(e[0] for e in est):,.0f}, out~{sum(e[1] for e in est):,.0f}")
    print(f"estimated cost: ${total:.2f} at ${PRICE_IN_PER_M}/${PRICE_OUT_PER_M} per M tokens "
          f"(heuristic from one measured call; real cost is logged per call)")
    print("real run requires --confirm")


def call_model(client, prompt):
    response = client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig=INFERENCE_CONFIG,
        toolConfig=TOOL_CONFIG,
    )
    parsed = next((b["toolUse"]["input"] for b in response["output"]["message"]["content"] if "toolUse" in b), None)
    return response, parsed


def real_run(all_jobs, path, run_name):
    import boto3  # imported here so dry-run never touches AWS

    done = load_done(path)
    todo = [j for j in all_jobs if call_key(j[1]["case_id"], j[1]["condition"], j[0]) not in done]
    cap = 2 * sum(estimate(p)[2] for _, _, p in todo)  # stop if actual spend exceeds 2x the estimate
    client = boto3.Session(profile_name=PROFILE, region_name=REGION).client("bedrock-runtime")
    spent, errors_in_a_row = 0.0, 0
    print(f"running {len(todo)} calls (skipping {len(all_jobs) - len(todo)} already logged) -> {path}")
    for i, (repeat, cond, prompt) in enumerate(todo, 1):
        response = parsed = error = cost = None
        status = "ok"
        try:
            response, parsed = call_model(client, prompt)
            u = response["usage"]
            cost = estimate_cost(u["inputTokens"], u["outputTokens"], PRICE_IN_PER_M, PRICE_OUT_PER_M)
            spent += cost
            if response["stopReason"] == "max_tokens":
                status, error = "truncated", "stopReason max_tokens"
            elif parsed is None:
                status, error = "parse_error", "no toolUse block in response"
        except Exception as e:  # logged, never swallowed silently
            status, error = "error", f"{type(e).__name__}: {e}"
        append_record(path, make_record(
            run_name=run_name, cond=cond, repeat=repeat, model_id=MODEL_ID, region=REGION,
            settings=INFERENCE_CONFIG, prompt_version=PROMPT_VERSION, prompt=prompt,
            response=response, parsed=parsed, status=status, error=error, cost=cost))
        print(f"[{i}/{len(todo)}] {cond['case_id']} {cond['condition']} r{repeat}: {status}  spent ${spent:.4f}")
        errors_in_a_row = errors_in_a_row + 1 if status == "error" else 0
        if errors_in_a_row >= MAX_CONSECUTIVE_ERRORS:
            sys.exit(f"stopping: {MAX_CONSECUTIVE_ERRORS} consecutive errors (see {path})")
        if spent > cap:
            sys.exit(f"stopping: spend ${spent:.2f} exceeded cap ${cap:.2f}")
    print(f"done. total spent ${spent:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-name", default="pilot", help="log file is results/<run-name>.jsonl")
    ap.add_argument("--limit-case", nargs="+", metavar="CASE_ID",
                    help="only run these case IDs (for example --limit-case F3 P1)")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true", help="build prompts and estimate cost; no API calls")
    ap.add_argument("--confirm", action="store_true", help="required to make real API calls")
    args = ap.parse_args()

    conditions = load_conditions()
    if args.limit_case:
        unknown = set(args.limit_case) - {c["case_id"] for c in conditions}
        if unknown:
            sys.exit(f"unknown case ID(s): {sorted(unknown)}")
        conditions = [c for c in conditions if c["case_id"] in args.limit_case]
    all_jobs = jobs(conditions, args.repeats)
    path = log_path(args.run_name)
    if args.dry_run:
        dry_run(all_jobs, path)
    elif not args.confirm:
        sys.exit(f"refusing to start {len(all_jobs)} API calls without --confirm. Run with --dry-run first.")
    else:
        real_run(all_jobs, path, args.run_name)


if __name__ == "__main__":
    main()
