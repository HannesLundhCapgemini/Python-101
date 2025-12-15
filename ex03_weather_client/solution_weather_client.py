from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests


class ApiClientError(Exception):
    """Raised when HTTP call fails or returns an unexpected response."""


@dataclass
class WeatherInfo:
    city: str          # Label, e.g. "Stockholm, Sweden"
    temperature_c: float
    summary: str


# -------------------- Weather (MET Norway) client --------------------


class WeatherClient:
    """
    HTTP client for MET Norway's Weather API (Locationforecast/2.0).

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

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if not response.ok:
            raise ApiClientError(
                f"Unexpected status code {response.status_code}: {response.text}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise ApiClientError("Response body is not valid JSON") from exc

    @staticmethod
    def _symbol_to_text(symbol_code: str) -> str:
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

        # fallback: prettify arbitrary symbol_code
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
        """
        Retrieve current-ish weather info for coordinates using MET Locationforecast.
        """
        lat_rounded = round(lat, 4)
        lon_rounded = round(lon, 4)

        url = f"{self._base_url}/compact"
        params: Dict[str, Any] = {"lat": lat_rounded, "lon": lon_rounded}
        if altitude is not None:
            params["altitude"] = round(altitude)

        headers = {
            "User-Agent": self._user_agent,
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self._timeout_seconds,
            )
        except requests.RequestException as exc:
            raise ApiClientError(f"HTTP request failed: {exc}") from exc

        data = self._handle_response(response)

        try:
            properties = data["properties"]
            timeseries = properties["timeseries"]
            if not timeseries:
                raise ApiClientError("No timeseries data in MET response")

            first_ts = timeseries[0]
            details = first_ts["data"]["instant"]["details"]
            temp_c = float(details["air_temperature"])
        except KeyError as exc:
            raise ApiClientError(f"Missing expected key in MET response: {exc}") from exc
        except (TypeError, ValueError) as exc:
            raise ApiClientError(f"Invalid data types in MET response: {exc}") from exc

        summary_text = "No summary available"
        try:
            data_block = first_ts["data"]
            for key in ("next_1_hours", "next_6_hours", "next_12_hours"):
                block = data_block.get(key)
                if not block:
                    continue
                summary = block.get("summary")
                if not summary:
                    continue
                symbol_code = summary.get("symbol_code")
                if not symbol_code:
                    continue
                summary_text = self._symbol_to_text(str(symbol_code))
                break
        except Exception:
            pass

        city_label = label or f"({lat_rounded:.4f}, {lon_rounded:.4f})"

        return WeatherInfo(city=city_label, temperature_c=temp_c, summary=summary_text)


# -------------------- Geocoding (Nominatim) client --------------------


@dataclass
class GeoLocation:
    lat: float
    lon: float
    display_name: str


class GeocodingClient:
    """
    Simple client for OpenStreetMap Nominatim search API.

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
        """
        Geocode a city name (optionally with country), e.g.:
          "Stockholm"
          "Stockholm, Sweden"
        """
        params = {
            "q": query,
            "format": "jsonv2",
            "limit": str(limit),
            "addressdetails": "1",
        }
        headers = {
            "User-Agent": self._user_agent,
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                self._base_url,
                params=params,
                headers=headers,
                timeout=self._timeout_seconds,
            )
        except requests.RequestException as exc:
            raise ApiClientError(f"Geocoding request failed: {exc}") from exc

        if not response.ok:
            raise ApiClientError(
                f"Geocoding returned {response.status_code}: {response.text}"
            )

        try:
            data: List[Dict[str, Any]] = response.json()
        except ValueError as exc:
            raise ApiClientError("Geocoding response is not valid JSON") from exc

        if not data:
            raise ApiClientError(f"No geocoding results for query: {query!r}")

        first = data[0]

        try:
            lat = float(first["lat"])
            lon = float(first["lon"])
            display_name = str(first.get("display_name", query))
        except KeyError as exc:
            raise ApiClientError(f"Missing expected key in geocoding response: {exc}") from exc
        except (TypeError, ValueError) as exc:
            raise ApiClientError(f"Invalid data types in geocoding response: {exc}") from exc

        return GeoLocation(lat=lat, lon=lon, display_name=display_name)


# -------------------- High-level service: city → weather --------------------


class WeatherService:
    """
    High-level facade that lets you call:
        get_weather_for_city("Stockholm")
    which:
        1. Geocodes the city with Nominatim.
        2. Fetches weather from MET for the resulting coordinates.
    """

    def __init__(
        self,
        weather_client: WeatherClient,
        geocoding_client: GeocodingClient,
    ) -> None:
        self._weather_client = weather_client
        self._geocoding_client = geocoding_client

    def get_weather_for_city(self, city: str) -> WeatherInfo:
        location = self._geocoding_client.geocode_city(city)
        return self._weather_client.get_weather_for_coordinates(
            lat=location.lat,
            lon=location.lon,
            label=location.display_name,
        )


def main() -> None:
    """
    Manual test: look up a city by name, then fetch MET weather for it.

    IMPORTANT:
      - Replace `user_agent` values below with something that identifies YOUR app
        and contact info, to comply with both Nominatim and MET policies.
    """
    user_agent = "example-weather-client/0.1 hl96sopor@gmail.com"

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
