import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

import requests, datetime as dt
from zoneinfo import ZoneInfo

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

import os, requests, datetime as dt
from zoneinfo import ZoneInfo

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

# Parse env: WEATHER_HOURS="07,08,09,10,11,12,13,14,15,16,17,18,19,20,21"
WEATHER_HOURS = {int(h) for h in os.getenv("WEATHER_HOURS").split(",") if h.strip()}
LOCAL_TZ = os.getenv("LOCAL_TZ", "Europe/Stockholm")

def fetch_weather(lat: float, lon: float) -> dict:
    today = dt.datetime.now(ZoneInfo(LOCAL_TZ)).date().isoformat()
    r = requests.get(OPEN_METEO, params={
        "latitude": lat, "longitude": lon, "timezone": LOCAL_TZ, "timeformat": "iso8601",
        "start_date": today, "end_date": today,
        "hourly": "temperature_2m,precipitation,precipitation_probability,wind_speed_10m",
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
    }, timeout=25)
    r.raise_for_status()
    j = r.json()

    times = j["hourly"]["time"]
    idx = [i for i, t in enumerate(times) if dt.datetime.fromisoformat(t).hour in WEATHER_HOURS]
    hourly = {"time": [times[i] for i in idx]}
    for k, v in j["hourly"].items():
        if k != "time":
            hourly[k] = [v[i] for i in idx]

    return {"hourly": hourly, "daily": j["daily"]}

def summarize(payload: dict) -> tuple:
    d = payload["daily"]
    return (
        float(d["temperature_2m_min"][0]),
        float(d["temperature_2m_max"][0]),
        float(d["wind_speed_10m_max"][0]),
        int(d["precipitation_probability_max"][0]),
        float(d["precipitation_sum"][0]),
    )