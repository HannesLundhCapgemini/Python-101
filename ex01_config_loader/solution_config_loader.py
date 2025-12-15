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
    """Read a JSON file and return its contents as a dictionary."""
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Config file is not valid JSON: {path}") from exc


def validate_raw_config(raw: Dict[str, Any]) -> None:
    """
    Validate that the raw config contains required fields
    and that values are of the expected type.
    """
    required_keys = ["app_name", "environment", "log_level", "retry_count"]
    missing = [k for k in required_keys if k not in raw]
    if missing:
        missing_str = ", ".join(missing)
        raise ConfigError(f"Missing required config keys: {missing_str}")

    # Validate retry_count
    try:
        retry_count = int(raw["retry_count"])
    except (TypeError, ValueError):
        raise ConfigError("retry_count must be an integer")

    if retry_count < 0:
        raise ConfigError("retry_count must be >= 0")

    # Optional: validate environment
    allowed_envs = {"dev", "test", "prod"}
    env = str(raw["environment"]).lower()
    if env not in allowed_envs:
        raise ConfigError(
            f"environment must be one of {sorted(allowed_envs)}, got {raw['environment']!r}"
        )

    # Optional: validate log_level
    allowed_levels = {"DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"}
    log_level = str(raw["log_level"]).upper()
    if log_level not in allowed_levels:
        raise ConfigError(
            f"log_level must be one of {sorted(allowed_levels)}, got {raw['log_level']!r}"
        )


def parse_config(raw: Dict[str, Any]) -> AppConfig:
    """
    Convert a raw config dictionary into an AppConfig object.

    Assumes raw has already been validated.
    """
    return AppConfig(
        app_name=str(raw["app_name"]),
        environment=str(raw["environment"]),
        log_level=str(raw["log_level"]).upper(),
        retry_count=int(raw["retry_count"]),
    )


def load_config(path: Path) -> AppConfig:
    """
    High-level API: load and validate config from a JSON file.
    """
    raw = read_json_file(path)
    validate_raw_config(raw)
    return parse_config(raw)


def main() -> None:
    """
    Simple manual test:
      - Loads 'appsettings.json' from the appsettings folder. Can change to the other json files to test error handling.
      - Prints the resulting AppConfig.
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
