from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import json


class ConfigError(Exception):
    """Raised when the configuration file is invalid or missing required values."""


@dataclass
class AppConfig:
    """Application configuration settings."""
    app_name: str
    environment: str
    log_level: str
    retry_count: int


def read_json_file(path: Path) -> Dict[str, Any]:
    """Read a JSON file and return its contents as a dictionary.

    This helper is fully implemented for you.

    - Verifies that the file exists.
    - Opens it with UTF-8 encoding.
    - Parses JSON into a Python dict using json.load().
    - Wraps JSON decoding errors in ConfigError.
    """
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Config file is not valid JSON: {path}") from exc


def validate_raw_config(raw: Dict[str, Any]) -> None:
    """Validate that the raw config contains required fields and sane values.

    Your tasks:

    - Ensure the following keys exist in raw:
        - "app_name"
        - "environment"
        - "log_level"
        - "retry_count"

    - Validate retry_count:
        - Can be converted to int
        - Is >= 0

    - (Stretch) Validate:
        - environment is one of: "dev", "test", "prod"
        - log_level is one of common levels:
          "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"

    On any validation error, raise ConfigError with a clear, helpful message.
    """
    # TODO: implement validation logic described in the docstring.
    raise NotImplementedError("validate_raw_config is not implemented yet")


def parse_config(raw: Dict[str, Any]) -> AppConfig:
    """Convert a raw config dictionary into an AppConfig object.

    Assumes raw has already been validated.
    """
    return AppConfig(
        app_name=str(raw["app_name"]),
        environment=str(raw["environment"]),
        log_level=str(raw["log_level"]).upper(),
        retry_count=int(raw["retry_count"]),
    )


def load_config(path: Path) -> AppConfig:
    """High-level API: load and validate config from a JSON file.

    Steps:

    1. Use read_json_file(path) to get a raw dict.
    2. Call validate_raw_config(raw).
    3. Call parse_config(raw) to convert the dict into an AppConfig.
    4. Return the AppConfig instance.
    """
    # TODO: implement according to the steps above.
    raise NotImplementedError("load_config is not implemented yet")


def main() -> None:
    """Simple manual test.

    - Loads 'appsettings.json' from the 'appsettings' subfolder.
    - Prints the resulting AppConfig.
    - Prints a friendly error message if loading fails.
    """
    config_path = Path(__file__).parent / "appsettings" / "appsettings.json"
    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"Failed to load config: {exc}")
        return

    print("Loaded config:")
    print(config)


if __name__ == "__main__":
    main()
