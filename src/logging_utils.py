"""Append-only JSONL logging, one line per model call, with resume support."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def run_dir(run_name):
    """Pilot and plumbing runs share results/pilot/; every other run gets its own results/<run_name>/ folder."""
    return RESULTS_DIR / ("pilot" if run_name.startswith(("pilot", "plumbing")) else run_name)


def log_path(run_name):
    return run_dir(run_name) / f"{run_name}.jsonl"


def call_key(case_id, condition, repeat):
    return (case_id, condition, repeat)


def load_done(path):
    """Keys of calls already logged with status "ok". Errored calls are retried on resume.

    The log is never rewritten: error lines stay in the file and a retry appends a new line.
    """
    done = set()
    if Path(path).exists():
        for line in Path(path).read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                if r["status"] == "ok":
                    done.add(call_key(r["case_id"], r["condition"], r["repeat"]))
    return done


def estimate_cost(input_tokens, output_tokens, price_in_per_m, price_out_per_m):
    return (input_tokens * price_in_per_m + output_tokens * price_out_per_m) / 1e6


def append_record(path, record):
    """Write one JSON line and flush to disk so a crash never loses a completed call."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        f.flush()
        os.fsync(f.fileno())


def make_record(*, run_name, cond, repeat, model_id, region, settings, prompt_version, prompt,
                response=None, parsed=None, status="ok", error=None, cost=None):
    """Build the log record for one call. `cond` is a line from data/pilot_conditions.jsonl."""
    usage = (response or {}).get("usage", {})
    return {
        "run_name": run_name,
        "case_id": cond["case_id"],
        "tier": cond["tier"],
        "condition": cond["condition"],
        "repeat": repeat,
        "model_id": model_id,
        "region": region,
        "settings": settings,
        "prompt_version": prompt_version,
        "prompt": prompt,
        "order": cond["order"],
        "d1_position": cond["d1_position"],
        "display_map": {d["display_id"]: d["internal"] for d in cond["docs"]},
        "seed": cond["seed"],
        "raw_response": response,
        "parsed": parsed,
        "stop_reason": (response or {}).get("stopReason"),
        "input_tokens": usage.get("inputTokens"),
        "output_tokens": usage.get("outputTokens"),
        "estimated_cost_usd": cost,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "error": error,
    }
