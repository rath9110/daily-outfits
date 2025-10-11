import requests
import os
from dotenv import load_dotenv
from prefs import Prefs

load_dotenv()  # This loads variables from .env into os.environ

API_TOKEN = os.environ['CL_API_TOKEN']

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/b02f1f2d39ac28eb46abf30933acaba1/ai/run/"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def outfit_for_day(
    t_min, t_max, wind_max, rain_prob_max, rain_mm_total,
    prefs, lat, lon, name="User", gender="gender"
) -> str:
    inputs = [
        {
            "role": "system",
            "content": (
                "You are a concise wardrobe and weather assistant. "
                "Given today's local weather and user sensitivity, reply with EXACTLY ONE short line for the weather and one for clothing: "
                "practical outfit layers + a brief note if needed (e.g., umbrella or windproof). "
                "If rain_prob<30 AND rain_mm<1.0 for the target hours, "
                "do NOT suggest rain gear; explicitly avoid umbrella/rain jacket/rain pants."
                f"suggest outift based on that I'm a {gender} "
                "Don't give colour suggestions or fit type. "
                "The rain, wind and cold sensitivities are on a scale 0-10, where 10 is very sensitive and 0 barely any sensitivity "
                "No preamble, no emojis, no bullet points."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Language: {prefs.language or 'en'}.\n"
                f"Context: {name or 'User'} in lat {lat}, lon {lon} today.\n"
                f"Weather: min {t_min}°C, max {t_max}°C, wind {wind_max} m/s, "
                f"rain {rain_prob_max}% ≈ {rain_mm_total} mm.\n"
                f"Sensitivity (colder→more layers): cold={prefs.cold_bias}, "
                f"wind={prefs.wind_tolerance}, rain={prefs.rain_tolerance}.\n"
                "Return one line only."
            ),
        },
    ]


    print("AI inputs:", inputs)
    response = requests.post(
        f"{API_BASE_URL}@cf/meta/llama-3-8b-instruct",
        headers=headers,
        json={"messages": inputs}
    )
    if response.status_code != 200:
        print(f"STATUS: {response.status_code} | CT: {response.headers.get('content-type')}")
        print(f"BODY: {response.text}")
        return "AI error: could not get outfit suggestion."
    result = response.json()
    outfit = (result.get("result", {}).get("response", "") or "").strip()
    return outfit
