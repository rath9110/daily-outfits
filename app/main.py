import os, sys, datetime as dt
import requests
import json
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from users import load_users
from weather_api import fetch_weather, summarize
from weather_ai import outfit_for_day
from telegramer import send_telegram

load_dotenv()

def fetch_coordinates():
    gist_id = os.environ.get("GIST_ID")
    token = os.getenv("GT_TOKEN")

    H = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"Bearer {token}",
    }

    # 1) Fetch the latest state of the gist (this is the latest commit)
    resp = requests.get(f"https://api.github.com/gists/{gist_id}", headers=H, timeout=20)
    resp.raise_for_status()
    gist = resp.json()

    # 2) Pick a JSON file (prefer one with .json extension; fallback to application/json type)
    files = gist.get("files", {}) or {}
    candidates = []
    for f in files.values():
        name = (f.get("filename") or "").lower()
        mime = (f.get("type") or "").lower()
        if name.endswith(".json") or "json" in mime:
            # Use updated_at to break ties if multiple JSON files exist
            updated = f.get("updated_at") or gist.get("updated_at") or gist.get("created_at")
            candidates.append((updated, f))

    if not candidates:
        raise RuntimeError("No JSON file found in the latest gist commit.")

    # newest JSON file by updated timestamp (most are in the single latest commit anyway)
    candidates.sort(key=lambda x: x[0] or "", reverse=True)
    _, jf = candidates[0]

    content = jf.get("content")
    if not content or jf.get("truncated"):
        raw_url = jf["raw_url"]  # guaranteed for gist files
        raw = requests.get(raw_url, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=20)
        raw.raise_for_status()
        content = raw.text

    # 4) Parse as JSON
    data = json.loads(content)
    return data

def run():
    tz = os.environ.get("LOCAL_TZ")
    now = dt.datetime.now(ZoneInfo(tz))
    weather_hours = os.environ.get("WEATHER_HOURS")
    
    coordinates = fetch_coordinates()
    users_path = os.path.join(os.path.dirname(__file__), "users.csv")
    users = load_users(users_path)

    for user in users:
        try:
            chat_id = user["chat_id"]
            name = user["name"]
            lat = coordinates["latitude"]
            lon = coordinates["longitude"]
            prefs = user["prefs"]

            wx = fetch_weather(lat, lon)
            t_min, t_max, wind_max, rain_prob_max, rain_mm_total = summarize(wx)
            outfit = outfit_for_day(
                t_min, t_max, wind_max, rain_prob_max, rain_mm_total, prefs, name, lat, lon
            )

            msg = (
                f"God morgon{f' {name}' if name else ''}!\n"
                f"Today you should wear {outfit}\n"
                f"Have a good one!"
                )
            send_telegram(chat_id, msg)
            print(f"Sent to chat_id={chat_id}")
        except Exception as e:
            print(f"Error for chat_id={user.get('chat_id')}: {e}", file=sys.stderr)

if __name__ == "__main__":
    run()
