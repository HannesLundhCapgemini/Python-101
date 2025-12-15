# Exercise 01 – Config Loader & Validator (Workshop Version)

**Goal**  
Practice Python style, type hints, dataclasses, and exceptions by
building a small, reusable configuration loader – similar to how you’d
load `appsettings.json` in a C# app.

---

## 🧩 Scenario

We want a clean, reusable function:

```python
config = load_config(config_path)
```

This should:

1. Read a JSON file from disk.
2. Validate required keys and values.
3. Convert the raw data into an `AppConfig` dataclass.
4. Raise clear exceptions when something is wrong.

---

## 📁 Files in this exercise

- `starter_config_loader.py` – **you work here** (contains TODOs).
- `solution_config_loader.py` – reference solution.
- `appsettings/` – example JSON config files.

Key types and functions in the starter:

- `ConfigError` – custom exception for config problems.
- `AppConfig` – dataclass representing validated configuration.
- `read_json_file(path)` – helper that already reads + parses JSON.
- `validate_raw_config(raw)` – **you implement** validation here.
- `parse_config(raw)` – builds an `AppConfig` instance.
- `load_config(path)` – **you implement** high-level API.
- `main()` – small demo that loads and prints the config.

---

## 🛠 Your Tasks

### 1️⃣ Implement `validate_raw_config(raw: Dict[str, Any]) -> None`

Responsibilities:

- Ensure the following keys exist in `raw`:

  - `app_name`
  - `environment`
  - `log_level`
  - `retry_count`

- Validate:

  - `retry_count` can be converted to an `int`
  - `retry_count >= 0`

- (Stretch) Validate that:

  - `environment` is one of: `"dev"`, `"test"`, `"prod"`
  - `log_level` is one of: `"DEBUG"`, `"INFO"`, `"WARN"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`

- Raise `ConfigError` with **clear, helpful messages** when validation fails.

---

### 2️⃣ Implement `load_config(path: Path) -> AppConfig`

Steps:

1. Use `read_json_file(path)` (already provided) to read the JSON file into a `dict`.
2. Call `validate_raw_config(raw)` to ensure the config is valid.
3. Call `parse_config(raw)` to convert the dict into an `AppConfig` dataclass.
4. Return the resulting `AppConfig` instance.

---

### 3️⃣ Use the `main()` demo

In `starter_config_loader.py`, `main()` already:

1. Builds a path to `appsettings.json` in the `appsettings` subfolder.
2. Calls `load_config(config_path)`.
3. Prints the resulting `AppConfig` or catches `ConfigError` and prints a friendly error.

Run it with:

```bash
python starter_config_loader.py
```

---

## 💬 Discussion Points

- Compare `AppConfig` to a C# POCO class:
  - Same idea: a simple data holder with named fields.
- Why raise exceptions vs returning `None` or error codes?
  - Clearer control flow; errors can’t be silently ignored.
- Python style:
  - `snake_case` for functions and variables (`load_config`, `retry_count`)
  - Type hints for readability and tooling support
  - Docstrings to describe behavior and expectations

---

## 📚 Relevant Python Documentation

### 🧱 Dataclasses, Types & Exceptions

- Dataclasses → https://docs.python.org/3/library/dataclasses.html
- Type hints (`typing`) → https://docs.python.org/3/library/typing.html
- Exceptions & error handling → https://docs.python.org/3/tutorial/errors.html

### 📦 Files & JSON

- `pathlib.Path` (file paths) → https://docs.python.org/3/library/pathlib.html
- `json` (JSON encode/decode) → https://docs.python.org/3/library/json.html

### 🧾 Core Language & Style

- Python Tutorial (overview) → https://docs.python.org/3/tutorial/
- Style guide (PEP 8) → https://peps.python.org/pep-0008/

---

By completing this exercise you will:

- Read JSON config files.
- Validate input early and fail fast.
- Use dataclasses to represent structured configuration.
- Write small functions with clear responsibilities – a very transferable skill from C# to Python.
