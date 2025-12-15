from __future__ import annotations

from pathlib import Path
from typing import Sequence, List
import json


def load_values(path: Path) -> List[float]:
    """Load metric values from a JSON file.

    Expected JSON format:
      [
        {"value": 1.0},
        {"value": 2.5},
        ...
      ]

    Your tasks:

    - Open the file using path.open(..., encoding="utf-8") in a with-block.
    - Use json.load to parse the JSON.
    - Validate that the top-level value is a list.
    - For each item:
        - Ensure it is a dict with a "value" key.
        - Convert item["value"] to float and collect in a list.
    - Return the list of floats.

    Let appropriate exceptions propagate or wrap them with a clearer message
    if you prefer.
    """
    # TODO: implement according to the docstring.
    raise NotImplementedError("load_values is not implemented yet")


def calculate_average(values: Sequence[float]) -> float:
    """Calculate the arithmetic mean of a sequence of numbers.

    Requirements:

    - If values is empty, raise ValueError with a helpful message.
    - Otherwise, return sum(values) / len(values).
    """
    # TODO: implement average calculation.
    raise NotImplementedError("calculate_average is not implemented yet")


def main() -> None:
    """Entry point for the metrics script.

    Steps:

    - Determine the path to 'metrics.json' (same folder as this file).
    - Call load_values(path) to get a list of floats.
    - Call calculate_average(values) to get the mean.
    - Print the result using an f-string, e.g. 'Average metric value: 1.23'.
    - Catch and handle common exceptions (FileNotFoundError, JSON errors,
      KeyError, ValueError) and print a friendly error instead.
    """
    # TODO: implement main according to the steps above.
    raise NotImplementedError("main is not implemented yet")


if __name__ == "__main__":
    main()
