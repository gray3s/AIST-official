#!/usr/bin/env python3
"""Generate AIH v4 date-stamped Markdown and EPS run artifacts."""

import json
import math
import sys
from datetime import datetime
from pathlib import Path


def text(value, default=""):
    if value is None:
        return default
    return str(value)


def number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def ps_escape(value):
    return text(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def load_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def summarize(rows):
    summary = {
        "boards": len(rows),
        "plies": 0,
        "legal_moves": 0,
        "rejected": 0,
        "invalid": 0,
        "illegal": 0,
        "elapsed": 0.0,
        "completed": 0,
        "invalid_runs": 0,
        "transport_failures": 0,
        "missing_keys": 0,
        "authorization_failures": 0,
        "stack_availability": 0,
        "board_awareness_pass": 0,
        "board_awareness_fail": 0,
        "board_awareness_skipped": 0,
    }
    failure_classes = {}
    per_stack = {}
    for row in rows:
        stack = text(row.get("stktyp"), "unknown")
        per_stack.setdefault(stack, {"boards": 0, "legal_moves": 0, "rejected": 0, "elapsed": 0.0})
        per_stack[stack]["boards"] += 1
        per_stack[stack]["legal_moves"] += int(row.get("legal_moves_played", 0) or 0)
        per_stack[stack]["rejected"] += int(row.get("rejected_move_total", 0) or 0)
        per_stack[stack]["elapsed"] += number(row.get("total_elapsed_s"))

        summary["plies"] += int(row.get("plies_played", 0) or 0)
        summary["legal_moves"] += int(row.get("legal_moves_played", 0) or 0)
        summary["rejected"] += int(row.get("rejected_move_total", 0) or 0)
        summary["invalid"] += int(row.get("invalid_move_total", 0) or 0)
        summary["illegal"] += int(row.get("illegal_move_total", 0) or 0)
        summary["elapsed"] += number(row.get("total_elapsed_s"))
        summary["completed"] += 1 if row.get("completed_game") else 0
        summary["board_awareness_pass"] += int(row.get("pre_move_board_awareness_pass", 0) or 0)
        summary["board_awareness_pass"] += int(row.get("post_move_board_awareness_pass", 0) or 0)
        summary["board_awareness_fail"] += int(row.get("pre_move_board_awareness_fail", 0) or 0)
        summary["board_awareness_fail"] += int(row.get("post_move_board_awareness_fail", 0) or 0)
        summary["board_awareness_skipped"] += int(row.get("pre_move_board_awareness_skipped", 0) or 0)
        summary["board_awareness_skipped"] += int(row.get("post_move_board_awareness_skipped", 0) or 0)

        termination = text(row.get("termination")).lower()
        if "invalidated" in termination:
            summary["invalid_runs"] += 1
        if "transport" in termination:
            summary["transport_failures"] += 1
        for event in row.get("events", []) or []:
            failure = text(event.get("response_failure_class"), "none")
            if failure and failure != "none":
                failure_classes[failure] = failure_classes.get(failure, 0) + 1
            if failure == "missing_provider_key":
                summary["missing_keys"] += 1
            elif failure == "cloud_authorization_or_entitlement_failure":
                summary["authorization_failures"] += 1
            elif failure == "suspected_remote_disablement_or_stack_availability":
                summary["stack_availability"] += 1
    return summary, per_stack, failure_classes


def write_markdown(path, source_name, rows, summary, per_stack, failure_classes):
    created = datetime.now().isoformat(timespec="seconds")
    with path.open("w", encoding="utf-8") as out:
        out.write("# AIH v4 Run Analysis\n\n")
        out.write(f"Created: {created}\n\n")
        out.write(f"Source JSONL: `{source_name}`\n\n")
        out.write("## AIH Behavior Summary\n\n")
        out.write("| Boards | Plies | Legal moves | Rejected attempts | Invalid parses | Illegal moves | Completed games | Invalidated runs | Transport failures | Elapsed s |\n")
        out.write("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        out.write(
            f"| {summary['boards']} | {summary['plies']} | {summary['legal_moves']} | {summary['rejected']} | "
            f"{summary['invalid']} | {summary['illegal']} | {summary['completed']} | {summary['invalid_runs']} | "
            f"{summary['transport_failures']} | {summary['elapsed']:.3f} |\n\n"
        )
        out.write("## Stack Summary\n\n")
        out.write("| Stack type | Boards | Legal moves | Rejected attempts | Elapsed s |\n")
        out.write("| --- | ---: | ---: | ---: | ---: |\n")
        for stack, item in sorted(per_stack.items()):
            out.write(f"| {stack} | {item['boards']} | {item['legal_moves']} | {item['rejected']} | {item['elapsed']:.3f} |\n")
        out.write("\n## Failure Classes\n\n")
        if failure_classes:
            out.write("| Failure class | Events |\n| --- | ---: |\n")
            for failure, count in sorted(failure_classes.items()):
                out.write(f"| {failure} | {count} |\n")
        else:
            out.write("No non-none response failure classes were recorded.\n")
        out.write("\n## Board Awareness\n\n")
        out.write(f"- Pass: {summary['board_awareness_pass']}\n")
        out.write(f"- Fail: {summary['board_awareness_fail']}\n")
        out.write(f"- Skipped: {summary['board_awareness_skipped']}\n")


def write_eps(path, source_name, rows, summary, per_stack, failure_classes):
    width = 720
    height = 520
    max_bar = 430
    metrics = [
        ("Legal moves", summary["legal_moves"]),
        ("Rejected attempts", summary["rejected"]),
        ("Invalid parses", summary["invalid"]),
        ("Illegal moves", summary["illegal"]),
        ("Invalidated runs", summary["invalid_runs"]),
        ("Transport failures", summary["transport_failures"]),
    ]
    max_value = max([value for _, value in metrics] + [1])
    with path.open("w", encoding="utf-8") as out:
        out.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        out.write(f"%%BoundingBox: 0 0 {width} {height}\n")
        out.write("%%Title: AIH v4 Run Analysis\n")
        out.write("%%Creator: AIH v4 generate_run_artifacts.py\n")
        out.write("%%EndComments\n")
        out.write("/Helvetica findfont 12 scalefont setfont\n")
        out.write("36 488 moveto (AIH v4 Run Analysis) show\n")
        out.write("/Helvetica findfont 8 scalefont setfont\n")
        out.write(f"36 472 moveto (Source: {ps_escape(source_name)}) show\n")
        out.write(f"36 458 moveto (Boards: {summary['boards']}  Plies: {summary['plies']}  Elapsed s: {summary['elapsed']:.3f}) show\n")
        y = 420
        for label, value in metrics:
            bar = 0 if max_value == 0 else int(math.ceil(max_bar * value / max_value))
            out.write("0.90 setgray\n")
            out.write(f"180 {y - 3} {max_bar} 12 rectfill\n")
            out.write("0.15 0.35 0.55 setrgbcolor\n")
            out.write(f"180 {y - 3} {bar} 12 rectfill\n")
            out.write("0 setgray\n")
            out.write(f"36 {y} moveto ({ps_escape(label)}) show\n")
            out.write(f"620 {y} moveto ({value}) show\n")
            y -= 34
        out.write("/Helvetica findfont 9 scalefont setfont\n")
        out.write("36 170 moveto (Stack summary) show\n")
        y = 150
        out.write("/Helvetica findfont 8 scalefont setfont\n")
        for stack, item in sorted(per_stack.items()):
            line = f"{stack}: boards={item['boards']} legal={item['legal_moves']} rejected={item['rejected']} elapsed_s={item['elapsed']:.3f}"
            out.write(f"36 {y} moveto ({ps_escape(line[:120])}) show\n")
            y -= 16
            if y < 70:
                break
        if failure_classes:
            failures = ", ".join(f"{k}={v}" for k, v in sorted(failure_classes.items()))
        else:
            failures = "none"
        out.write(f"36 42 moveto (Failure classes: {ps_escape(failures[:130])}) show\n")
        out.write("showpage\n%%EOF\n")


def main(argv):
    if len(argv) != 3:
        print("Usage: generate_run_artifacts.py RUN.jsonl OUT_DIR", file=sys.stderr)
        return 2
    source = Path(argv[1])
    out_dir = Path(argv[2])
    rows = load_jsonl(source)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d")
    base = source.stem
    summary, per_stack, failure_classes = summarize(rows)
    md_path = out_dir / f"{base}_analysis_{stamp}.md"
    eps_path = out_dir / f"{base}_analysis_{stamp}.eps"
    write_markdown(md_path, source.name, rows, summary, per_stack, failure_classes)
    write_eps(eps_path, source.name, rows, summary, per_stack, failure_classes)
    print(f"analysis_md={md_path}")
    print(f"analysis_eps={eps_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
