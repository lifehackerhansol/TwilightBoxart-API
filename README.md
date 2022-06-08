# TwilightBoxart API

Reimplementation of TwilightBoxart API, as the original one is down and I can't find the source anywhere.

Currently working:
- Image resizing
- DS/DSi boxarts

Currently not working:
- SHA1 matching (No-Intro DB is not implemented)
- Borders (ignored for now)
- Any console other than DS/DSi (will return 404)

To run:
1. Rebuild [TwilightBoxart](https://github.com/KirovAir/TwilightBoxart) with `ApiUrl` in `TwilightBoxart/BoxartConfig.cs` to a URL of your choice
    - I used localhost:40000 for internal testing
1. Run `pip install -r requirements.txt` on this repository to get what you need
1. Run `uvicorn main:app --port=<something>`
