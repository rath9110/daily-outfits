import csv
from typing import List
from prefs import Prefs

def load_users(csv_path: str) -> List[dict]:
    users = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append({
                "chat_id": row["chat_id"].strip(),
                "name": row.get("name", "").strip(),
                "prefs": Prefs(
                    cold_bias=int(row.get("cold_bias", 0) or 0),
                    wind_tolerance=int(row.get("wind_tolerance", 0) or 0),
                    rain_tolerance=int(row.get("rain_tolerance", 0) or 0),
                    language=row.get("language", "en")
                ),
                "gender": row.get("gender", "").strip()
            })
    return users