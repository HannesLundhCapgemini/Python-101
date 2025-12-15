# Exercise 05 – Refactor to Pythonic Code + Tests (Workshop Version)

**Goal**  
Take a messy script and refactor it into clean, testable, idiomatic
Python with unit tests.

You’ll practice:

- Using context managers for files
- Working with JSON
- Writing pure functions
- Adding type hints
- Writing unit tests with pytest

---

## 🧩 Scenario

You are given an intentionally bad script: `bad_metrics_script.py`.

It:

- Opens file handles manually (`f = open(...); f.close()`).
- Calls `exit(1)` directly.
- Does everything at the top level (no functions).
- Has no type hints.
- Is hard to test.

Your job is to:

1. Move logic into small, testable functions.
2. Write tests for those functions using pytest.

---

## 📁 Files in this exercise

- `bad_metrics_script.py` – intentionally bad code (starting point).
- `starter_metrics.py` – **you work here** (contains TODOs).
- `test_metrics_starter.py` – **you write tests here**.
- `solution_metrics.py` – reference implementation.
- `test_metrics_solution.py` – reference tests.

---

## 🛠 Your Tasks

### 1️⃣ Inspect `bad_metrics_script.py`

Notice issues such as:

- No functions or reuse.
- Error handling via `exit(1)` instead of exceptions.
- File I/O, parsing and printing all mixed together.
- No type hints.

You’ll fix all of this in `starter_metrics.py`.

---

### 2️⃣ Implement `load_values(path: Path) -> list[float]` in `starter_metrics.py`

Responsibilities:

- Open the JSON file using a `with` context manager:

  ```python
  with path.open("r", encoding="utf-8") as f:
      raw = json.load(f)
  ```

- Expect JSON format:

  ```json
  [{ "value": 1.0 }, { "value": 2.5 }]
  ```

- Extract `"value"` from each entry and return a list of `float`.
- Let appropriate exceptions surface (or wrap them if desired):
  - `FileNotFoundError` if the file doesn’t exist.
  - `json.JSONDecodeError` if the JSON is invalid.
  - `KeyError` or `TypeError` if the structure isn’t as expected.

---

### 3️⃣ Implement `calculate_average(values: Sequence[float]) -> float`

Responsibilities:

- Return the arithmetic mean of the values.
- Decide what to do for an **empty sequence**, e.g.:

  ```python
  if not values:
      raise ValueError("values must not be empty")
  ```

- Then:

  ```python
  return sum(values) / len(values)
  ```

---

### 4️⃣ Implement `main() -> None`

Responsibilities:

- Determine the path to `metrics.json`, e.g.:

  ```python
  metrics_path = Path(__file__).parent / "metrics.json"
  ```

- Call `load_values(metrics_path)`.
- Call `calculate_average(values)`.
- Print the result using an f-string, e.g.:

  ```python
  print(f"Average value: {avg:.2f}")
  ```

- Use `try`/`except` to handle errors and print a friendly message instead of using `exit(1)`.

Finally, add the standard entrypoint (already in the starter):

```python
if __name__ == "__main__":
    main()
```

---

### 5️⃣ Implement tests in `test_metrics_starter.py`

Use `pytest` to write small, focused tests.

#### `test_calculate_average_simple`

- Assert that `calculate_average([1, 2, 3]) == 2.0`.

#### `test_calculate_average_empty_list`

- Decide on the behavior for an empty list (e.g. raise `ValueError`).
- Assert that behavior using `pytest.raises`.

Example pattern:

```python
import pytest

def test_calculate_average_empty_list() -> None:
    with pytest.raises(ValueError):
        calculate_average([])
```

Run tests:

```bash
pytest
```

---

## 💬 Discussion Points

- **Why test pure functions?**  
  They have no side effects, take inputs and return outputs → very easy to test.

- **Python tests (pytest) vs C# test frameworks:**

  - Less ceremony; use plain functions and `assert`.
  - No need for classes unless you want them.

- **Error handling:**
  - Using exceptions vs return codes.
  - How to surface clear error messages to users.

---

## 📚 Relevant Python Documentation

### 📦 Standard Library

- `json` → https://docs.python.org/3/library/json.html
- `pathlib.Path` → https://docs.python.org/3/library/pathlib.html

### 🧾 Typing & Sequences

- Type hints (`typing`) → https://docs.python.org/3/library/typing.html
  - `Sequence` → https://docs.python.org/3/library/typing.html#typing.Sequence
  - `List` → https://docs.python.org/3/library/typing.html#typing.List

### 🧪 Testing

- pytest documentation → https://docs.pytest.org/en/stable/
- `assert` statement → https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
- pytest `raises` → https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions

### 📘 Core Language & Style

- Python Tutorial → https://docs.python.org/3/tutorial/
- Style guide (PEP 8) → https://peps.python.org/pep-0008/
- Exceptions → https://docs.python.org/3/tutorial/errors.html

---

By completing this exercise you practice:

- Refactoring messy, script-style code into clean functions.
- Using context managers for files.
- Handling JSON data safely.
- Writing unit tests that validate behavior.
- Applying Pythonic style and idioms that map well from your C# background.
