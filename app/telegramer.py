import os
import requests
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_telegram(chat_id: str | int, text: str) -> None:
    url = f"{BASE}/sendMessage"
    resp = requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True
    }, timeout=20)
    if resp.status_code >= 300:
        raise RuntimeError(f"Telegram send error {resp.status_code}: {resp.text}")
