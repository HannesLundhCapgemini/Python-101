from __future__ import annotations

from pathlib import Path
from typing import Sequence, List
import json


def load_values(path: Path) -> List[float]:
    """
    Load metric values from a JSON file.

    Expected JSON format:
      [
        {"value": 1.0},
        {"value": 2.5},
        ...
      ]
    """
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise ValueError("Expected top-level JSON array of objects.")

    values: List[float] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} is not an object.")
        if "value" not in item:
            raise KeyError(f"Missing 'value' key at index {idx}.")

        try:
            value = float(item["value"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Value at index {idx} is not numeric: {item['value']!r}") from exc

        values.append(value)

    return values


def calculate_average(values: Sequence[float]) -> float:
    """
    Calculate the arithmetic mean of a sequence of numbers.

    Raises:
        ValueError: if the sequence is empty.
    """
    if not values:
        raise ValueError("Cannot calculate average of empty sequence.")

    return sum(values) / len(values)


def main() -> None:
    """
    Entry point for the metrics script.

    - Determines the path to 'metrics.json' (same folder as this file).
    - Loads values using load_values.
    - Calculates the average.
    - Prints the result using an f-string.
    - Handles exceptions gracefully.
    """
    metrics_path = Path(__file__).parent / "metrics.json"
    try:
        values = load_values(metrics_path)
        avg = calculate_average(values)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"Failed to calculate metrics: {exc}")
        return

    print(f"Average metric value: {avg:.2f}")


if __name__ == "__main__":
    main()
