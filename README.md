# TwilightBoxart API

Reimplementation of TwilightBoxart API, as the original one is down and I can't find the source anywhere.

Currently working:
- Literally nothing (Image seems to correctly convert but returns 0KB of image)

Currently not working:
- Literally everything else

To run:
1. Rebuild [TwilightBoxart](https://github.com/KirovAir/TwilightBoxart) with `ApiUrl` in `TwilightBoxart/BoxartConfig.cs` to a URL of your choice
    - I used localhost:40000 for internal testing
1. Run `pip install -r requirements.txt` on this repository to get what you need
1. Run `uvicorn main:app --port=<something>`
