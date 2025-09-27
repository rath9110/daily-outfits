Daily Outfit suggester - A one-line clothing tips app to my Telegram bot based on the daily hours I'm outside

My problem statement: I always forget to check the weather forecast for the day -> this causes me to dress only on how it looks outside when I wake up 
(which turns out to be wrong way to estimate the daily forecast)

Limits I put on my project
- Free to run
- Must be based on where I'm at for the day -> can't rely on  a hardcoded value

Solution: An automation program on my phone sends my location each morning to a Python app, which then fetches the hourly weather for the area and hours I'm outside. 
Based on this, a 8B param AI writes a concise clothing suggestion and then DMs me on Telegram with the clothing suggestions.

How it works:

- Set up an automation program in Iphones's shortcuts that sends my lat and lon each morning to a GitHub gist.
- Fetch Open-Meteo → filter to my outside hours.
- Summarize (min/max temp, wind, rain prob/mm).
- Generate a one-liner using open-source model llama-3.1-8b-instruct based on the weather forecast, a prompt for how to resonate about the clothing
  and my sensitivity when it comes to wind, rain and cold on a scale 0-10.
- Send to my phone via a Telegram bot.


Features to add next:
- Add service that allows me to give feedback each day to the clothing suggestion -> allows me to tweak my cold, rain and wind sensitivity params
- Allow multiple people to subscribe to customized weather prognosis
- Move to iPhone app to allow easier onboarding of new people -> allows fetching coordinates directly without automation program,
  allows direct push notifications instead of Telegram messages, enables program to be run on client side


Value I get: Faster mornings, consistent dress decisions, no app-hopping—just one message at the right time.

What I did: Designed prompt + rules, built clean env-based config, added hour-window logic, wired CI to run daily/hourly, and handled delivery + edge cases.
