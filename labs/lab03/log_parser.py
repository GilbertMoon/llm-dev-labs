# labs/lab03/log_parser.py
"""
Lab 03: Draft implementation (verifiable draft)
- Spec-driven
- Fixed function signatures and output schema
- TODO markers for uncertain parts
"""

from __future__ import annotations
import re
import json
from typing import Dict, Any, List, Union


# --- Fixed output schema keys for valid lines ---
VALID_KEYS = [
    "timestamp",
    "level",
    "service",
    "user",
    "path",
    "status",
    "latency_ms",
    "message",
    "masked",
]

# Pre-compiled patterns (module-level for performance on 100k+ lines)
_TOKEN_RE = re.compile(r"token=\S+")
_LINE_RE = re.compile(
    r'^\s*\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+'
    r'(?P<level>[A-Z]+)\s+'
    r'service=(?P<service>\S+)\s+'
    r'user=(?P<user>\S+)\s+'
    r'path=(?P<path>\S+)\s+'
    r'status=(?P<status>\S+)\s+'
    r'latency_ms=(?P<latency_ms>\S+)\s+'
    r'msg="(?P<message>.*)"\s*$'
)


def mask_tokens(message: str) -> tuple[str, bool]:
    """
    Mask token-like substring: token=<anything> -> token=[REDACTED]
    Return (masked_message, masked_flag)
    """
    # TODO: clarify whether token values may contain whitespace or be quoted.
    # Safe default: mask until the next whitespace.
    masked_message, count = _TOKEN_RE.subn("token=[REDACTED]", message)
    return masked_message, count > 0


def parse_line(line: str) -> Dict[str, Any]:
    """
    Parse one log line.
    On success: return dict with EXACT keys in VALID_KEYS and correct types.
    On failure: return {"error": True, "raw": <line>, "reason": <short reason>}
    """
    raw = line
    if raw.strip() == "":
        return {"error": True, "raw": raw, "reason": "empty line"}

    match = _LINE_RE.match(raw)
    if not match:
        return {"error": True, "raw": raw, "reason": "invalid format"}

    # --- integer field conversion ---
    try:
        user = int(match.group("user"))
    except ValueError:
        return {"error": True, "raw": raw, "reason": "user is not int"}

    try:
        status = int(match.group("status"))
    except ValueError:
        return {"error": True, "raw": raw, "reason": "status is not int"}

    try:
        latency_ms = int(match.group("latency_ms"))
    except ValueError:
        return {"error": True, "raw": raw, "reason": "latency_ms is not int"}

    # --- message extraction & token masking ---
    message = match.group("message")
    masked_message, is_masked = mask_tokens(message)

    return {
        "timestamp": match.group("timestamp"),
        "level": match.group("level"),
        "service": match.group("service"),
        "user": user,
        "path": match.group("path"),
        "status": status,
        "latency_ms": latency_ms,
        "message": masked_message,
        "masked": is_masked,
    }


def parse_text(text: str) -> List[Dict[str, Any]]:
    """
    Parse multiline string into list of dict results (valid objects or error objects).
    Must not crash on invalid lines.
    """
    results: List[Dict[str, Any]] = []
    for raw in text.splitlines():
        if raw.strip() == "":
            # treat empty line as invalid (spec choice)
            results.append({"error": True, "raw": raw, "reason": "empty line"})
            continue
        results.append(parse_line(raw))
    return results


def parse_file(path: str) -> List[Dict[str, Any]]:
    """
    Parse a log file line-by-line (streaming friendly).
    """
    results: List[Dict[str, Any]] = []
    # TODO: implement streaming file read safely (encoding issues)
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.rstrip("\n")
            if raw.strip() == "":
                results.append({"error": True, "raw": raw, "reason": "empty line"})
                continue
            results.append(parse_line(raw))
    return results


def to_json_lines(items: List[Dict[str, Any]]) -> str:
    """
    Convert list of dicts to JSON Lines string.
    """
    return "\n".join(json.dumps(x, ensure_ascii=False) for x in items)


def main():
    sample = "\n".join(
        [
            '[2026-02-21 10:11:12] INFO service=api user=42 path=/login status=200 latency_ms=31 msg="ok"',
            '[2026-02-21 10:11:13] WARN service=api user=42 path=/login status=429 latency_ms=12 msg="rate limit"',
            '[2026-02-21 10:11:14] ERROR service=api user=42 path=/pay status=500 latency_ms=201 msg="db timeout token=abcd-1234"',
            "INVALID LINE HERE",
        ]
    )

    results = parse_text(sample)
    print(to_json_lines(results))


if __name__ == "__main__":
    main()