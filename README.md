# Python 101 for Azure Developers

This repository contains exercises for a **Python 101 workshop** aimed at
developers with a background in **C# and Azure**.

## Prerequisites

- Python 3.10+ installed through the company portal, install the Pre-Approved catalogue, search for Python and install one of the versions
- (Recommended) VS Code with:
  - Python extension
  - Azure Functions extension
- For Exercise 6:
  - Azure Functions Core Tools
  - Azure Functions VS Code extension or CLI

## How to Use This Repo

Each folder `ex0X_*` contains:

- `starter_*.py` – the code you work on
- `solution_*.py` – a reference solution (for after the exercise)
- `README.md` – instructions and goals

Suggested order:

1. `ex01_config_loader`
2. `ex02_log_analyzer`
3. `ex03_weather_client`
4. `ex04_async_queue_processor`
5. `ex05_metrics_refactor`
6. `ex06_azure_function_http` (requires Azure Functions tooling)

---

## Running Python Code

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```
