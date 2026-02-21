from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import argparse
import re
from typing import Iterable


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>[A-Z]+)\] (?P<message>.*)$"
)


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    level: str
    message: str


class LogParseError(Exception):
    pass


def parse_line(line: str) -> LogEntry:
    stripped = line.strip()
    if not stripped:
        raise LogParseError("빈 로그 라인은 파싱할 수 없습니다.")

    match = LOG_PATTERN.match(stripped)
    if not match:
        raise LogParseError(f"로그 형식이 올바르지 않습니다: {stripped}")

    try:
        ts = datetime.strptime(match.group("timestamp"), "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise LogParseError(f"타임스탬프 파싱 실패: {match.group('timestamp')}") from exc

    return LogEntry(timestamp=ts, level=match.group("level"), message=match.group("message"))


def parse_lines(lines: Iterable[str], skip_invalid: bool = True) -> list[LogEntry]:
    parsed: list[LogEntry] = []
    for line in lines:
        try:
            parsed.append(parse_line(line))
        except LogParseError:
            if not skip_invalid:
                raise
    return parsed


def parse_file(file_path: str, encoding: str = "utf-8", skip_invalid: bool = True) -> list[LogEntry]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    try:
        with path.open("r", encoding=encoding) as f:
            return parse_lines(f, skip_invalid=skip_invalid)
    except OSError as exc:
        raise OSError(f"파일 읽기 중 오류가 발생했습니다: {file_path}") from exc


def summarize_by_level(entries: list[LogEntry]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for entry in entries:
        summary[entry.level] = summary.get(entry.level, 0) + 1
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="기본 파이썬 로그 파서 데모")
    parser.add_argument("--file", help="파싱할 로그 파일 경로", default="")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="형식이 잘못된 라인을 만나면 즉시 예외를 발생시킵니다.",
    )
    args = parser.parse_args()

    sample_logs = [
        "2026-02-21 10:00:00 [INFO] Application started",
        "2026-02-21 10:01:05 [WARN] Disk usage at 85%",
        "잘못된 로그 라인",
        "2026-02-21 10:02:30 [ERROR] Connection timeout",
    ]

    try:
        if args.file:
            entries = parse_file(args.file, skip_invalid=not args.strict)
            source = f"파일: {args.file}"
        else:
            entries = parse_lines(sample_logs, skip_invalid=not args.strict)
            source = "내장 데모 로그"

        print(f"\n[{source}] 파싱 결과: {len(entries)}건")
        for entry in entries:
            print(f"- {entry.timestamp:%Y-%m-%d %H:%M:%S} [{entry.level}] {entry.message}")

        print("\n레벨별 집계")
        for level, count in summarize_by_level(entries).items():
            print(f"- {level}: {count}")

    except FileNotFoundError as exc:
        print(f"파일 오류: {exc}")
    except LogParseError as exc:
        print(f"로그 파싱 오류: {exc}")
    except Exception as exc:
        print(f"예상하지 못한 오류: {exc}")


if __name__ == "__main__":
    main()
