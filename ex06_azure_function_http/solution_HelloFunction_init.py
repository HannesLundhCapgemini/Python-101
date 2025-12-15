import logging
from datetime import datetime
import json
import os

import azure.functions as func


def _get_default_name() -> str | None:
    """Optional helper to read a default name from environment."""
    return os.getenv("DEFAULT_NAME")


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP-triggered Azure Function that returns a greeting.

    - Reads "name" from query string or JSON body.
    - Falls back to DEFAULT_NAME env var if provided.
    - Returns JSON payload:
        {
          "greeting": "Hello <name>!",
          "timestamp": "<iso8601-utc>"
        }
    """
    logging.info("HelloFunction processed a request.")

    name = req.params.get("name")

    if not name:
        try:
            body = req.get_json()
        except ValueError:
            body = {}
        name = body.get("name")

    if not name:
        name = _get_default_name()

    if not name:
        error_body = {"error": "Please provide a 'name'."}
        return func.HttpResponse(
            body=json.dumps(error_body),
            status_code=400,
            mimetype="application/json",
        )

    if any(char.isdigit() for char in name):
        error_body = {"error": "Name must not contain digits."}
        return func.HttpResponse(
            body=json.dumps(error_body),
            status_code=422,
            mimetype="application/json",
        )

    response_data = {
        "greeting": f"Hello {name}!",
        "timestamp": datetime.utcnow().isoformat(),
    }

    return func.HttpResponse(
        body=json.dumps(response_data),
        status_code=200,
        mimetype="application/json",
    )
