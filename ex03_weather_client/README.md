# Exercise – Real HTTP Weather Client in Python (for Azure/C# Developers)

## 🎯 Goal

In this exercise you will:

- Call **real HTTP APIs** from Python using [`requests`](https://requests.readthedocs.io/)
- Map JSON responses into **dataclasses**
- Handle **errors** properly (network errors, bad status codes, bad JSON)
- Compose two APIs into a clean, testable **service layer**

You will start from `starter_weather_client.py` and work your way towards  
`solution_weather_client.py`.

---

## 🌍 Scenario

We want a simple, high-level call:

```python
service.get_weather_for_city("Stockholm, Sweden")
```

Internally this should:

1. Use **Nominatim (OpenStreetMap)** to convert the city name into latitude/longitude.
2. Use **MET Norway Locationforecast/2.0** to fetch real weather data for those coordinates.
3. Return a `WeatherInfo` dataclass with:
   - `city` – nice label (e.g. `"Stockholm, Stockholms kommun, Sverige"`)
   - `temperature_c` – current-ish temperature in Celsius
   - `summary` – human readable text (e.g. `"Partly cloudy"`)

---

## 🧱 Architecture

The solution is structured into three layers:

```text
WeatherService (high-level, what your app would use)
    |
    +-- GeocodingClient (Nominatim)
    |
    +-- WeatherClient   (MET Norway)
```

- **`WeatherService`** exposes a single method:

  - `get_weather_for_city(city: str) -> WeatherInfo`

- **`GeocodingClient`** talks to:

  - `https://nominatim.openstreetmap.org/search`

- **`WeatherClient`** talks to:
  - `https://api.met.no/weatherapi/locationforecast/2.0/compact`

The **public API** of the module is `WeatherService` and `WeatherInfo`.  
Everything else is implementation detail.

---

## 📁 Files in this exercise

- `starter_weather_client.py` – the file you will work in (with `TODO` markers).
- `solution_weather_client.py` – a full reference implementation.
- `README.md` – this file.

> ✅ **Important:**  
> The starter file has the **same class and method structure** as the solution:
>
> - `WeatherInfo`, `GeoLocation`
> - `WeatherClient`
> - `GeocodingClient`
> - `WeatherService`
>
> Your job is to fill in the missing implementations so the starter behaves like the solution.

---

## 🧩 Step-by-step tasks

All work happens in **`starter_weather_client.py`**.  
Look for `# TODO:` markers.

### 1️⃣ Implement `_handle_response` in `WeatherClient`

Location: `WeatherClient._handle_response(self, response)`

Requirements:

- If `response.ok` is `False`:
  - raise `ApiClientError` with status code and body text.
- Otherwise:
  - call `response.json()` and return the parsed dict.
- If `response.json()` raises `ValueError`, wrap it in `ApiClientError` with a clear message.

> 💡 **C# mapping:**  
> Similar to checking `HttpResponseMessage.IsSuccessStatusCode` and then
> calling `ReadFromJsonAsync<T>()`, but here both steps live in one helper.

---

### 2️⃣ Implement `GeocodingClient.geocode_city`

Location: `GeocodingClient.geocode_city(self, query, limit=1)`

Use Nominatim:

- **Endpoint:** `https://nominatim.openstreetmap.org/search`
- **Query params:**
  - `q = query`
  - `format = "jsonv2"`
  - `limit = str(limit)`
  - `addressdetails = "1"`
- **Headers:**
  - `User-Agent = self._user_agent`
  - `Accept = "application/json"`

Steps:

1. Call `requests.get(...)` with params, headers, and `timeout=self._timeout_seconds`.
2. Wrap `requests.RequestException` in `ApiClientError`.
3. If `response.ok` is `False`, raise `ApiClientError`.
4. Parse body as JSON → list of results.
5. If the list is empty, raise `ApiClientError` (“no results”).
6. Take `first = data[0]` and extract:
   - `lat`, `lon` → convert to `float`
   - `display_name` → fall back to the original query if missing
7. Build and return `GeoLocation(lat=..., lon=..., display_name=...)`.

Run just this part by temporarily adding a small snippet in `main()`:

```python
geo = geocoding_client.geocode_city("Stockholm, Sweden")
print(geo)
```

---

### 3️⃣ Implement `WeatherClient.get_weather_for_coordinates`

Location: `WeatherClient.get_weather_for_coordinates(...)`

Use MET Norway Locationforecast:

- **Base URL** (already in `self._base_url`):
  - `https://api.met.no/weatherapi/locationforecast/2.0`
- **Endpoint:**
  - `f"{self._base_url}/compact"`

Steps:

1. Round `lat` and `lon` to 4 decimal places.
2. Build `params`:
   - `{"lat": lat_rounded, "lon": lon_rounded}`
   - optionally also `"altitude": round(altitude)` if provided.
3. Build `headers`:
   - `User-Agent = self._user_agent`
   - `Accept = "application/json"`
4. Call `requests.get(...)` with URL, params, headers, timeout.
   - Wrap `requests.RequestException` in `ApiClientError`.
5. Use `_handle_response` to parse the JSON into a dict.
6. Extract temperature:

   ```python
   properties = data["properties"]
   timeseries = properties["timeseries"]
   first_ts = timeseries[0]
   details = first_ts["data"]["instant"]["details"]
   temp_c = float(details["air_temperature"])
   ```

   - Wrap `KeyError`, `TypeError` and `ValueError` in `ApiClientError`
     with helpful messages.

7. Extract a `symbol_code` from the first available of:

   ```text
   next_1_hours.summary.symbol_code
   next_6_hours.summary.symbol_code
   next_12_hours.summary.symbol_code
   ```

   - If found: `summary_text = self._symbol_to_text(symbol_code)`
   - If none are found: `summary_text = "No summary available"`

8. Decide on the city label:

   ```python
   city_label = label or f"({lat_rounded:.4f}, {lon_rounded:.4f})"
   ```

9. Return:

   ```python
   return WeatherInfo(city=city_label, temperature_c=temp_c, summary=summary_text)
   ```

---

### 4️⃣ Implement `WeatherService.get_weather_for_city`

Location: `WeatherService.get_weather_for_city(self, city)`

This one is intentionally simple:

1. Call `self._geocoding_client.geocode_city(city)` → `location`.
2. Call `self._weather_client.get_weather_for_coordinates(...)` with:
   - `lat=location.lat`
   - `lon=location.lon`
   - `label=location.display_name`
3. Return the resulting `WeatherInfo`.

This mirrors how you might compose services in C# (e.g. one service for
geocoding, another for weather, plus a facade on top).

---

### 5️⃣ Run the full flow

Now run:

```bash
python starter_weather_client.py
```

If everything works, you should see something like:

```text
Weather in Stockholm, Stockholms kommun, Sverige: 5.7°C, Partly cloudy
```

(Actual numbers and text will vary based on the real weather.)

---

## 🔍 Comparing with the solution

Once your implementation works:

1. Open `solution_weather_client.py`.
2. Compare class by class, method by method.
3. Check:
   - How errors are handled.
   - How types are annotated.
   - How helper methods keep `get_weather_for_city` small and readable.

Focus on **structure** and **Python idioms**:

- Use `dataclasses` instead of manual POCOs.
- Use exceptions for error handling, not error codes.
- Use composition (`WeatherService` combining two clients), not static methods.

---

## 🚀 Stretch goals

If you finish early or want more practice:

1. **Batch lookup**

   - Add `WeatherService.get_weather_for_cities(cities: list[str]) -> list[WeatherInfo]`.

2. **Retries**

   - Add simple retry logic around the HTTP calls for transient failures.

3. **Caching**

   - Cache geocoding results in memory (a `dict[str, GeoLocation]`) so repeated
     calls for the same city don’t hit Nominatim again.

4. **Async version**
   - Try building an async version using `aiohttp` and `async/await`.

---

## ✅ Summary

By the end of this exercise you will have:

- Called real HTTP APIs from Python
- Parsed and validated JSON payloads
- Used `dataclasses` for clean, typed data models
- Composed multiple services into a clean, testable design

…all using concepts that map nicely from your existing **Azure/C#** experience.

Happy hacking! 🐍

---

## 📚 Relevant Python Documentation

### 🔧 Language & Syntax Basics

- Functions — https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Exceptions — https://docs.python.org/3/tutorial/errors.html
- Modules & imports — https://docs.python.org/3/tutorial/modules.html
- Type hints — https://docs.python.org/3/library/typing.html

### 🧱 Data Structures

- Dataclasses — https://docs.python.org/3/library/dataclasses.html
- Dictionaries — https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- Lists — https://docs.python.org/3/tutorial/introduction.html#lists

### 🌐 HTTP & JSON

- `requests` library — https://requests.readthedocs.io/en/stable/
- `response.json()` — https://requests.readthedocs.io/en/stable/user/quickstart/#json-response-content
- Built‑in `json` module — https://docs.python.org/3/library/json.html

### 🛠 Error Handling

- Built‑in exceptions — https://docs.python.org/3/library/exceptions.html
- `try` / `except` — https://docs.python.org/3/tutorial/errors.html#handling-exceptions

### 🧵 OOP & Classes in Python

- Classes — https://docs.python.org/3/tutorial/classes.html
- Special methods (`__init__`, etc.) — https://docs.python.org/3/reference/datamodel.html
