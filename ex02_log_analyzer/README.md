# Exercise 02 – Log Analyzer (Workshop Version)

**Goal**  
Work with strings, parsing, dataclasses, and dictionaries. Build a small
log analyzer that counts log levels (`INFO`, `WARN`, `ERROR`, etc.).

---

## 🧩 Scenario

You have log lines like:

```text
[INFO] Application started
[ERROR] Something went wrong
[WARN] Low disk space
```

You want to:

1. Parse each line into a structured object (`LogEntry`).
2. Count how many times each level occurs.
3. Get the top N log levels by frequency.

---

## 📁 Files in this exercise

- `starter_log_analyzer.py` – **you work here** (contains TODOs).
- `sample.log` – example log file for testing.
- `sample_timestamps.log` – **bonus** log file with timestamps (optional).
- `solution_log_analyzer.py` – reference solution.

Core pieces in the starter:

- `LogEntry` – frozen dataclass with `level` and `message`.
- `read_log_lines(path)` – helper that reads the file.
- `parse_log_line(line)` – **you implement** parsing.
- `count_by_level(entries)` – **you implement** counting.
- `top_n_levels(counts, n)` – **you implement** sorting/slicing.
- `analyze_log(path, n)` – uses the helpers to do the full analysis.
- `main()` – manual test that prints the result for `sample.log`.

---

## 🛠 Your Tasks

### 1️⃣ `parse_log_line(line: str) -> LogEntry | None`

Implement a parser that:

- Strips whitespace from the line.
- Returns `None` if:

  - The line is empty.
  - It doesn’t start with `"["`.
  - There is no closing `"]"`.
  - The extracted `level` or `message` is empty.

- Otherwise:
  - Extract `level` between the first `[` and `]`.
  - Take the message as everything after the closing bracket, minus leading spaces.
  - Return `LogEntry(level=..., message=...)`.

---

### 2️⃣ `count_by_level(entries: Iterable[LogEntry]) -> Dict[str, int]`

- Takes a list (or any iterable) of `LogEntry` objects.
- Returns a dictionary mapping levels to counts.

Example:

```python
{"INFO": 10, "ERROR": 3}
```

---

### 3️⃣ `top_n_levels(counts: Dict[str, int], n: int) -> Dict[str, int]`

- Sort levels by count (descending).
- For ties, sort by name ascending for determinism.
- Return a **new dictionary** containing only the top `n` items.

---

### 4️⃣ Run the full analysis

Run:

```bash
python starter_log_analyzer.py
```

You should see something like:

```text
Top log levels: {'INFO': 42, 'ERROR': 7, 'WARN': 5}
```

(Exact numbers depend on `sample.log`.)

---

## ⭐ Bonus: Timestamped log format (optional)

The file `sample_timestamps.log` contains a more realistic format like:

```text
[2024-05-20 09:15:23] [INFO] Application started
```

This is **not required** for the core exercise. The starter and reference solution focus on the simple format:

```text
[LEVEL] Message
```

If you want an extra challenge, try extending your parser to support the timestamped format (and optionally extract the timestamp into a new field).

---

## 💬 Discussion Points

- Pure functions → easier testing and fewer side effects.
- `dict` vs C# `Dictionary<TKey, TValue>`.
- Pythonic iteration:

  ```python
  for entry in entries:
      ...
  ```

---

## 📚 Relevant Python Documentation

### 🔤 Strings & Parsing

- String type → https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
- String methods → https://docs.python.org/3/library/stdtypes.html#string-methods

### 🧱 Dataclasses & Collections

- Dataclasses → https://docs.python.org/3/library/dataclasses.html
- Dictionaries (`dict`) → https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
- For loops → https://docs.python.org/3/tutorial/controlflow.html#for-statements

### 💾 Files

- Reading files → https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

### 🔢 Sorting

- Sorting HOWTO → https://docs.python.org/3/howto/sorting.html

---

By completing this exercise you practice:

- Turning unstructured text into structured data.
- Counting and sorting using dictionaries.
- Writing small, composable functions that can be tested in isolation.
