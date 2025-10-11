# Daily Outfit Suggester

**One-line clothing tips to my Telegram bot based on the daily hours I’m outside.**

## Problem

I always forget to check the weather forecast for the day → I end up dressing based on what it looks like when I wake up (which apparently is the wrong way to estimate the full-day forecast!).

## Constraints

* Free to run
* Must be based on where I’m at that day (no hardcoded coordinates)

## Solution

An automation on my phone sends my location each morning to a Python app. The app fetches hourly weather for the area and the hours I’m outside. Based on that, an 8B param AI writes a concise clothing suggestion and DMs me on Telegram.

## How it works

* iPhone Shortcuts send current lat/lon each morning to a GitHub Gist
* Fetch Open-Meteo based on coordinates → filter to my outside hours
* Summarize the min/max temp, wind, rain prob/mm
* Generate a one-liner using llama-3.1-8b-instruct, a prompt for how to reason about clothing, and my sensitivity to wind/rain/cold (0–10)
* Send to my phone via a Telegram bot

## Next

* Feedback loop to tweak my cold/rain/wind sensitivity params
* Multi-user: allow people to subscribe to customized forecasts
* iPhone app: simpler onboarding, direct coordinate access (no Shortcut), push notifications, client-side execution

## Value

Faster mornings, consistent dress decisions, no need to check the daily weather and plan outfit based on it → just one message when waking up.

