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
    """Read all lines from a log file (helper provided for you)."""
    with path.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def parse_log_line(line: str) -> Optional[LogEntry]:
    """Parse a single log line into a LogEntry or return None.

    Expected line format:
      [INFO] Application started
      [ERROR] Something went wrong

    Rules:

    - Strip whitespace.
    - Return None if the line is empty.
    - Return None if:
        - it does not start with "["
        - there is no closing "]"
        - level or message is empty

    Otherwise:
    - Extract the level between '[' and ']'
    - Everything after the closing bracket (trimmed of leading spaces)
      is the message.
    """
    # TODO: implement according to the rules above.
    raise NotImplementedError("parse_log_line is not implemented yet")


def count_by_level(entries: Iterable[LogEntry]) -> Dict[str, int]:
    """Count how many log entries exist per level.

    Example output:
      {"INFO": 10, "ERROR": 3}
    """
    # TODO: implement counting logic.
    raise NotImplementedError("count_by_level is not implemented yet")


def top_n_levels(counts: Dict[str, int], n: int) -> Dict[str, int]:
    """Return the top N log levels by frequency.

    Sort by:
      - frequency (descending)
      - then by name (ascending) for stability
    """
    # TODO: implement sorting and slicing logic.
    raise NotImplementedError("top_n_levels is not implemented yet")


def analyze_log(path: Path, n: int = 3) -> Dict[str, int]:
    """High-level helper that:

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
