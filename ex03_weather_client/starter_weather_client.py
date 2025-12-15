from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests


class ApiClientError(Exception):
    """Raised when an HTTP call fails or returns an unexpected response."""


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class WeatherInfo:
    """Simple container for the data our client returns to callers.

    This is the only thing your application needs to know about.
    Everything else in this file is plumbing to talk to the external APIs.
    """
    city: str          # Label, e.g. "Stockholm, Sweden"
    temperature_c: float
    summary: str       # Human-readable description, e.g. "Partly cloudy"


@dataclass
class GeoLocation:
    """Result from the geocoding service (Nominatim)."""
    lat: float
    lon: float
    display_name: str


# ---------------------------------------------------------------------------
# Weather (MET Norway) client
# ---------------------------------------------------------------------------


class WeatherClient:
    """HTTP client for MET Norway's Weather API (Locationforecast/2.0).

    Docs:
      - https://api.met.no/weatherapi/locationforecast/2.0/documentation
    """

    def __init__(
        self,
        base_url: str = "https://api.met.no/weatherapi/locationforecast/2.0",
        timeout_seconds: float = 5.0,
        user_agent: str = "my-weather-app/0.1 you@example.com",
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._user_agent = user_agent

    # ------------------------------------------------------------------
    # Shared HTTP response helper
    # ------------------------------------------------------------------
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Validate and parse an HTTP response as JSON.

        Your job:

        - If ``response.ok`` is ``False`` (non-2xx), raise ``ApiClientError``.
          Include the status code and body text in the error message.

        - Parse the body as JSON using ``response.json()``.

        - If JSON parsing fails (``ValueError``), wrap it in ``ApiClientError``
          with a helpful message like "Response body is not valid JSON".

        - Return the parsed JSON object (a ``dict[str, Any]``).

        Hints (Python vs C#):

        - ``response.ok`` is roughly like checking ``IsSuccessStatusCode``.
        - ``response.json()`` both reads and parses the body.
        """
        # TODO: implement this according to the docstring.
        raise NotImplementedError("_handle_response is not implemented yet")

    # ------------------------------------------------------------------
    # (Optional) helper: convert MET symbol_code to human text
    # ------------------------------------------------------------------
    @staticmethod
    def _symbol_to_text(symbol_code: str) -> str:
        """Convert a MET "symbol_code" into something more readable.

        Example:
            "partlycloudy_day" -> "Partly cloudy"
        """
        mapping = {
            "clearsky_day": "Clear sky",
            "clearsky_night": "Clear sky",
            "cloudy": "Cloudy",
            "fair_day": "Fair",
            "fair_night": "Fair",
            "partlycloudy_day": "Partly cloudy",
            "partlycloudy_night": "Partly cloudy",
            "rain": "Rain",
            "heavyrain": "Heavy rain",
            "lightrain": "Light rain",
            "snow": "Snow",
            "heavysnow": "Heavy snow",
            "lightsnow": "Light snow",
            "fog": "Fog",
        }

        if symbol_code in mapping:
            return mapping[symbol_code]

        # Fallback: prettify any unknown code.
        return (
            symbol_code.replace("_day", "")
            .replace("_night", "")
            .replace("_", " ")
            .capitalize()
        )

    def get_weather_for_coordinates(
        self,
        *,
        lat: float,
        lon: float,
        label: Optional[str] = None,
        altitude: Optional[float] = None,
    ) -> WeatherInfo:
        """Retrieve current-ish weather info for coordinates using MET.

        High-level steps (this mirrors the full solution file):

        1. Round ``lat`` and ``lon`` to 4 decimals (just to make nicer URLs).
        2. Build the URL: ``f"{self._base_url}/compact"``.
        3. Build ``params`` dict with ``lat`` and ``lon`` (and optional ``altitude``).
        4. Build ``headers`` dict with:
               "User-Agent": self._user_agent
               "Accept": "application/json"
        5. Call ``requests.get`` with:
               url, params=params, headers=headers,
               timeout=self._timeout_seconds
           Wrap ``requests.RequestException`` in ``ApiClientError``.
        6. Call ``self._handle_response(response)`` to get a JSON ``dict``.
        7. From the JSON, extract:
               properties.timeseries[0].data.instant.details.air_temperature
           Convert it to ``float``.
        8. Also try to extract a "symbol_code" from the first available of:
               next_1_hours.summary.symbol_code
               next_6_hours.summary.symbol_code
               next_12_hours.summary.symbol_code
           If you find one, convert it to text with ``self._symbol_to_text``.
           If not, fall back to something like "No summary available".
        9. Use ``label`` (if provided) as the city label; otherwise use a
           fallback like "(lat, lon)".
        10. Return a ``WeatherInfo`` instance.
        """
        # TODO: implement this based on the steps above.
        raise NotImplementedError("get_weather_for_coordinates is not implemented yet")


# ---------------------------------------------------------------------------
# Geocoding (Nominatim) client
# ---------------------------------------------------------------------------


class GeocodingClient:
    """Simple client for OpenStreetMap Nominatim search API.

    Docs:
      - https://nominatim.org/release-docs/latest/api/Search/
    """

    def __init__(
        self,
        base_url: str = "https://nominatim.openstreetmap.org/search",
        timeout_seconds: float = 5.0,
        user_agent: str = "my-weather-app/0.1 you@example.com",
    ) -> None:
        self._base_url = base_url
        self._timeout_seconds = timeout_seconds
        self._user_agent = user_agent

    def geocode_city(self, query: str, limit: int = 1) -> GeoLocation:
        """Geocode a city name (optionally with country).

        Example queries:
          - "Stockholm"
          - "Stockholm, Sweden"

        What you should do:

        1. Build a ``params`` dict:
               q = query
               format = "jsonv2"
               limit = str(limit)
               addressdetails = "1"
        2. Build ``headers`` with:
               "User-Agent": self._user_agent
               "Accept": "application/json"
        3. Call ``requests.get`` with:
               self._base_url, params=params, headers=headers,
               timeout=self._timeout_seconds
           Wrap ``requests.RequestException`` in ``ApiClientError``.
        4. If ``response.ok`` is False, raise ``ApiClientError`` with a
           helpful message.
        5. Parse the body as JSON (it will be a list). If JSON parsing fails,
           wrap the error in ``ApiClientError``.
        6. If the list is empty, raise ``ApiClientError`` saying there were
           no results.
        7. Take the first result (index 0) and extract:
               lat, lon, display_name
           Convert ``lat`` and ``lon`` to ``float``. If keys are missing or
           values have the wrong type, wrap the error in ``ApiClientError``.
        8. Return a ``GeoLocation`` instance.
        """
        # TODO: implement this method.
        raise NotImplementedError("geocode_city is not implemented yet")


# ---------------------------------------------------------------------------
# High-level service: city -> weather
# ---------------------------------------------------------------------------


class WeatherService:
    """High-level facade that exposes:

        get_weather_for_city("Stockholm")

    which internally:

      1. Uses ``GeocodingClient`` to convert the name to coordinates.
      2. Uses ``WeatherClient`` to fetch real weather data for those coords.
    """

    def __init__(
        self,
        weather_client: WeatherClient,
        geocoding_client: GeocodingClient,
    ) -> None:
        self._weather_client = weather_client
        self._geocoding_client = geocoding_client

    def get_weather_for_city(self, city: str) -> WeatherInfo:
        """Lookup a city name and then fetch weather for its coordinates.

        Steps:

        1. Call ``self._geocoding_client.geocode_city(city)`` to get a
           ``GeoLocation``.
        2. Call ``self._weather_client.get_weather_for_coordinates(...)``
           with the ``lat``, ``lon`` and ``display_name`` from the location.
        3. Return the resulting ``WeatherInfo``.
        """
        # TODO: implement this method.
        raise NotImplementedError("get_weather_for_city is not implemented yet")


# ---------------------------------------------------------------------------
# Manual test / demo
# ---------------------------------------------------------------------------


def main() -> None:
    """Manual smoke test.

    This will make real HTTP requests, so you need an internet connection,
    and you should replace the ``user_agent`` value with something that
    identifies YOUR app and includes contact info (as required by Nominatim
    and MET Norway).
    """
    user_agent = "example-weather-client/0.1 your-email@example.com"

    weather_client = WeatherClient(user_agent=user_agent)
    geocoding_client = GeocodingClient(user_agent=user_agent)
    service = WeatherService(weather_client, geocoding_client)

    city = "Stockholm, Sweden"

    try:
        info = service.get_weather_for_city(city)
    except ApiClientError as exc:
        print(f"Error: {exc}")
    else:
        print(f"Weather in {info.city}: {info.temperature_c:.1f}°C, {info.summary}")


if __name__ == "__main__":
    main()
