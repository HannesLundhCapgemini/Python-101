# Exercise 06 – Python Azure Function (HTTP Trigger)

**Goal:**  
Create a simple **HTTP-triggered Azure Function** in Python and run it locally.  
Compare it with C# Functions and get comfortable with Python + HTTP + JSON.

You’ll practice:

- Handling HTTP requests in Python
- Parsing query parameters and JSON bodies
- Returning JSON responses
- Using environment variables and basic validation

---

## 🏗️ How to Generate the Function (Required Setup Step)

Before writing any code, you must generate a Python Function App and the HTTP-triggered function using **Azure Functions Core Tools**.

### 1️⃣ Create a new Function App

In your terminal, inside the Exercise 06 folder:

```bash
func init PythonHttpDemo --python
```

This generates a Python Azure Functions project.

### 2️⃣ Create the HTTP-triggered function

Move into the project folder and generate the function:

```bash
cd PythonHttpDemo
func new --name HelloFunction --template "HTTP trigger"
```

This produces:

```
PythonHttpDemo/
│
├── HelloFunction/
│   ├── __init__.py      <- your function code
│   └── function.json
│
├── host.json
└── local.settings.json
```

### 3️⃣ Replace or modify the generated function

Open:

```
HelloFunction/__init__.py
```

Then either:

- Replace its contents with the starter version in this exercise **or**
- Apply the TODO steps in this README.

---

## 🔗 Useful Documentation

### 🧵 Azure Functions (Python)

- Azure Functions (Python) docs → https://learn.microsoft.com/azure/azure-functions/functions-reference-python
- HTTP trigger & bindings → https://learn.microsoft.com/azure/azure-functions/functions-bindings-http-webhook-trigger
- Azure Functions Core Tools → https://learn.microsoft.com/azure/azure-functions/functions-core-tools-reference

### 📘 Core Python

- `logging` → https://docs.python.org/3/library/logging.html
- `datetime` → https://docs.python.org/3/library/datetime.html
- `json` → https://docs.python.org/3/library/json.html
- `os` & environment variables → https://docs.python.org/3/library/os.html#os.environ

---

## Steps

### 1. Inspect the Generated Function

Open:

```
HelloFunction/__init__.py
```

Replace its contents with the starter below **or** apply the TODOs to the generated file:

```python
import logging
from datetime import datetime

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP-triggered Azure Function that returns a greeting.

    TODOs:
      - Extract "name" from query string OR JSON body.
      - If name is missing, return 400 with an error JSON.
      - If name is present, return:
          {
            "greeting": "Hello <name>!",
            "timestamp": "<iso8601-utc>"
          }
      - Use proper content type (application/json).
    """
    logging.info("HelloFunction processed a request.")

    # TODO: get 'name' from query params
    name = req.params.get("name")

    # TODO: if not present, try to read from JSON body
    if not name:
        try:
            body = req.get_json()
        except ValueError:
            body = {}
        name = body.get("name")

    if not name:
        # TODO: return 400 with JSON error
        return func.HttpResponse(
            body='{"error": "Please provide a \\"name\\"."}',
            status_code=400,
            mimetype="application/json",
        )

    response_data = {
        "greeting": f"Hello {name}!",
        "timestamp": datetime.utcnow().isoformat(),
    }

    # TODO: serialize response_data as JSON
    import json
    return func.HttpResponse(
        body=json.dumps(response_data),
        status_code=200,
        mimetype="application/json",
    )
```

---

## 2. Run the Function Locally

```bash
func start
```

Expected URL:

```
http://localhost:7071/api/HelloFunction
```

---

## 3. Test the Function

### Query string:

```
http://localhost:7071/api/HelloFunction?name=Alice
```

### JSON body:

```bash
curl -X POST http://localhost:7071/api/HelloFunction   -H "Content-Type: application/json"   -d '{"name": "Bob"}'
```

### Example Response:

```json
{
  "greeting": "Hello Bob!",
  "timestamp": "2025-11-13T09:32:10.123456"
}
```

---

## Discussion Points

- Python Function Apps mirror C# structure but with more dynamic behavior.
- JSON handling is explicit instead of automatic model binding.
- Environment variables work exactly the same as in C# Functions.

---

## Stretch Goals

- Read `DEFAULT_NAME` from environment when no name is provided.
- Add input validation (e.g., reject names containing digits).
- Add additional endpoints like `/health`.
- Log metadata such as IPs and headers.

---

By completing this exercise you will:

- Understand Python’s approach to Azure Functions
- Work with HTTP, JSON, validation, and environment variables
- Compare the Python experience directly to C# Azure Functions
