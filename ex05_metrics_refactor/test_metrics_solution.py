from __future__ import annotations

import pytest

from solution_metrics import calculate_average  # or from solution_metrics import calculate_average


def test_calculate_average_simple() -> None:
    """Average of 1, 2, 3 should be 2.0."""
    values = [1, 2, 3]
    actual = calculate_average(values)
    assert actual == pytest.approx(2.0)


def test_calculate_average_empty_list() -> None:
    """Empty list should raise ValueError."""
    with pytest.raises(ValueError):
        calculate_average([])
