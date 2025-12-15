from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class LogEntry:
    """Represents a single parsed log entry."""
    level: str
    message: str


def read_log_lines(path: Path) -> List[str]:
    """Read all lines from a log file."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def parse_log_line(line: str) -> Optional[LogEntry]:
    """
    Parse a single log line into a LogEntry.

    Expected line format:
      [INFO] Application started
      [ERROR] Something went wrong

    Returns None if the line does not match the expected format.
    """
    line = line.strip()
    if not line:
        return None

    if not (line.startswith("[") and "]" in line):
        return None

    try:
        closing_bracket_index = line.index("]")
    except ValueError:
        return None

    level = line[1:closing_bracket_index].strip()
    # Everything after '] ' is the message
    remainder = line[closing_bracket_index + 1 :].lstrip()
    message = remainder

    if not level or not message:
        return None

    return LogEntry(level=level, message=message)


def count_by_level(entries: Iterable[LogEntry]) -> Dict[str, int]:
    """
    Count how many log entries exist per level.

    Example output:
      {"INFO": 10, "ERROR": 3}
    """
    counts: Dict[str, int] = {}
    for entry in entries:
        counts[entry.level] = counts.get(entry.level, 0) + 1
    return counts


def top_n_levels(counts: Dict[str, int], n: int) -> Dict[str, int]:
    """
    Return the top N log levels by frequency.
    """
    # Sort by frequency descending, then by name for stability
    sorted_items = sorted(
        counts.items(),
        key=lambda kv: (-kv[1], kv[0]),
    )
    top_items = sorted_items[:n]
    return dict(top_items)


def analyze_log(path: Path, n: int = 3) -> Dict[str, int]:
    """
    High-level helper that:
      - Reads the log file
      - Parses each line into LogEntry objects (skipping invalid lines)
      - Counts entries per level
      - Returns the top N levels by frequency
    """
    lines = read_log_lines(path)
    entries = [
        entry
        for line in lines
        if (entry := parse_log_line(line)) is not None
    ]
    counts = count_by_level(entries)
    return top_n_levels(counts, n)


def main() -> None:
    """Manual test: analyze 'sample.log' and print top 3 log levels."""
    log_path = Path(__file__).parent / "sample.log"
    result = analyze_log(log_path, n=3)
    print("Top log levels:", result)


if __name__ == "__main__":
    main()
