#!/usr/bin/env python3
"""Probe AIH v4 cloud agents for rate/quota status without starting a game."""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_AGENTS = [
    "openai:gpt-4.1-mini",
    "openai:gpt-5-nano",
    "gemini:gemini-3.1-flash-lite",
    "anthropic:claude-3-5-haiku",
]

HEADER_PREFIXES = (
    "x-ratelimit-",
    "ratelimit",
    "retry-after",
    "openai-",
    "x-request-id",
    "anthropic-ratelimit-",
    "anthropic-priority-",
    "anthropic-request-id",
    "x-goog-",
)


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def split_agents(value):
    if not value:
        return []
    return [item.strip() for item in value.replace("\n", ",").split(",") if item.strip()]


def model_name(agent):
    if ":" in agent:
        return agent.split(":", 1)[1]
    return agent


def provider_name(agent):
    lower = agent.lower()
    if lower.startswith("openai:") or lower.startswith("gpt-"):
        return "openai"
    if lower.startswith("gemini:") or lower.startswith("google:") or lower.startswith("gemini-"):
        return "gemini"
    if lower.startswith("anthropic:") or lower.startswith("claude-"):
        return "anthropic"
    return "unknown"


def interesting_headers(headers):
    out = {}
    for key, value in headers.items():
        lower = key.lower()
        if lower.startswith(HEADER_PREFIXES):
            out[lower] = value
    return out


def header_number(headers, name):
    value = headers.get(name)
    if value is None:
        return None
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def pct_remaining(headers, remaining_name, limit_name):
    remaining = header_number(headers, remaining_name)
    limit = header_number(headers, limit_name)
    if remaining is None or limit in (None, 0):
        return None
    return round((remaining / limit) * 100.0, 3)


def summarize_quota(provider, headers):
    h = {k.lower(): v for k, v in headers.items()}
    summary = {}
    if provider == "openai":
        summary["requests_remaining_pct"] = pct_remaining(
            h, "x-ratelimit-remaining-requests", "x-ratelimit-limit-requests"
        )
        summary["tokens_remaining_pct"] = pct_remaining(
            h, "x-ratelimit-remaining-tokens", "x-ratelimit-limit-tokens"
        )
        summary["requests_remaining"] = h.get("x-ratelimit-remaining-requests")
        summary["tokens_remaining"] = h.get("x-ratelimit-remaining-tokens")
        summary["requests_reset"] = h.get("x-ratelimit-reset-requests")
        summary["tokens_reset"] = h.get("x-ratelimit-reset-tokens")
    elif provider == "anthropic":
        summary["requests_remaining_pct"] = pct_remaining(
            h, "anthropic-ratelimit-requests-remaining", "anthropic-ratelimit-requests-limit"
        )
        summary["tokens_remaining_pct"] = pct_remaining(
            h, "anthropic-ratelimit-tokens-remaining", "anthropic-ratelimit-tokens-limit"
        )
        summary["input_tokens_remaining_pct"] = pct_remaining(
            h, "anthropic-ratelimit-input-tokens-remaining", "anthropic-ratelimit-input-tokens-limit"
        )
        summary["output_tokens_remaining_pct"] = pct_remaining(
            h, "anthropic-ratelimit-output-tokens-remaining", "anthropic-ratelimit-output-tokens-limit"
        )
        summary["tokens_remaining"] = h.get("anthropic-ratelimit-tokens-remaining")
        summary["tokens_reset"] = h.get("anthropic-ratelimit-tokens-reset")
    else:
        summary["documented_remaining_pct_header"] = None
    summary["retry_after"] = h.get("retry-after")
    return {k: v for k, v in summary.items() if v is not None}


def http_json(url, headers, payload, timeout):
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return response.status, dict(response.headers.items()), body
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, dict(exc.headers.items()), body
    except urllib.error.URLError as exc:
        return 0, {}, json.dumps({"error": {"type": "transport_error", "message": str(exc)}})


def probe_openai(agent, timeout):
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return {"status": "missing_key", "required_env": "OPENAI_API_KEY"}
    payload = {
        "model": model_name(agent),
        "input": "Return exactly: ok",
        "max_output_tokens": 16,
    }
    status, headers, body = http_json(
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        payload,
        timeout,
    )
    return result_from_response(agent, "openai", status, headers, body)


def probe_gemini(agent, timeout):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_GENAI_API_KEY")
    if not key:
        return {"status": "missing_key", "required_env": "GEMINI_API_KEY"}
    api_version = os.environ.get("GEMINI_API_VERSION", "v1beta").strip() or "v1beta"
    url = (
        f"https://generativelanguage.googleapis.com/{api_version}/models/"
        f"{model_name(agent)}:generateContent?key={key}"
    )
    payload = {
        "contents": [{"parts": [{"text": "Return exactly: ok"}]}],
        "generationConfig": {"maxOutputTokens": 1},
    }
    status, headers, body = http_json(url, {"Content-Type": "application/json"}, payload, timeout)
    return result_from_response(agent, "gemini", status, headers, body)


def probe_anthropic(agent, timeout):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return {"status": "missing_key", "required_env": "ANTHROPIC_API_KEY"}
    payload = {
        "model": model_name(agent),
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "Return exactly: ok"}],
    }
    status, headers, body = http_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        payload,
        timeout,
    )
    return result_from_response(agent, "anthropic", status, headers, body)


def result_from_response(agent, provider, status_code, headers, body):
    filtered_headers = interesting_headers(headers)
    result = {
        "timestamp_utc": now_utc(),
        "agent": agent,
        "provider": provider,
        "status": "completed" if 200 <= status_code < 300 else "request_failed",
        "http_status": status_code,
        "quota_headers": filtered_headers,
        "quota_summary": summarize_quota(provider, filtered_headers),
        "body_sha256_unavailable": False,
    }
    try:
        parsed = json.loads(body) if body.strip() else {}
    except json.JSONDecodeError:
        parsed = {}
    if isinstance(parsed, dict):
        if "usage" in parsed:
            result["usage"] = parsed["usage"]
        error = parsed.get("error")
        if error:
            result["error"] = error
        if provider == "gemini" and "usageMetadata" in parsed:
            result["usage"] = parsed["usageMetadata"]
    if status_code == 429:
        result["limit_reached"] = True
    return result


def probe(agent, timeout):
    provider = provider_name(agent)
    if provider == "openai":
        result = probe_openai(agent, timeout)
    elif provider == "gemini":
        result = probe_gemini(agent, timeout)
    elif provider == "anthropic":
        result = probe_anthropic(agent, timeout)
    else:
        result = {"status": "unsupported_provider"}
    result.setdefault("timestamp_utc", now_utc())
    result.setdefault("agent", agent)
    result.setdefault("provider", provider)
    return result


def write_outputs(results, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    jsonl_path = out_dir / f"cloud_agent_limit_probe_{stamp}.jsonl"
    md_path = out_dir / f"cloud_agent_limit_probe_{stamp}.md"
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# AIH v4 Cloud Agent Limit Probe\n\n")
        handle.write(f"Created: {now_utc()}\n\n")
        handle.write("| Agent | Provider | Status | HTTP | Requests remaining % | Tokens remaining % | Retry after |\n")
        handle.write("| --- | --- | --- | ---: | ---: | ---: | --- |\n")
        for result in results:
            quota = result.get("quota_summary", {})
            handle.write(
                f"| {result.get('agent', '')} | {result.get('provider', '')} | "
                f"{result.get('status', '')} | {result.get('http_status', '')} | "
                f"{quota.get('requests_remaining_pct', '')} | {quota.get('tokens_remaining_pct', '')} | "
                f"{quota.get('retry_after', '')} |\n"
            )
        handle.write("\nNotes:\n\n")
        handle.write("- This probe does not start an AIChess game.\n")
        handle.write("- OpenAI and Anthropic expose documented rate-limit headers that can be converted to remaining percentages.\n")
        handle.write("- Gemini API quota docs describe RPM, TPM, RPD, and spend limits, but this probe records only headers actually returned by the API.\n")
    return jsonl_path, md_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", default=os.environ.get("AIH_V4_CLOUD_PROBE_AGENTS", ",".join(DEFAULT_AGENTS)))
    parser.add_argument("--out-dir", default="runs/cloud_agent_limit_probes")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    agents = split_agents(args.agents)
    if args.dry_run:
        for agent in agents:
            print(f"{provider_name(agent)}\t{agent}")
        return 0

    results = []
    for agent in agents:
        result = probe(agent, args.timeout)
        results.append(result)
        print(json.dumps(result, sort_keys=True))
        time.sleep(1)
    jsonl_path, md_path = write_outputs(results, Path(args.out_dir))
    print(f"probe_jsonl={jsonl_path}")
    print(f"probe_markdown={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
