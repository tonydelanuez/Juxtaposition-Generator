import random
from flask import Response
from json.decoder import JSONDecodeError
from typing import List, Dict
import requests

REDDIT_USER_AGENT = "x86_64_GNU/Linux:juxtaposition-generator:v0.0.1 (by /u/TonyDarko)"


def get_top_images() -> List[Dict]:
    timespan = random.choice(["month", "day", "year", "all"])
    resp = make_request(
        "https://www.reddit.com/r/wallpaper/top/.json?t={}&limit=100".format(timespan)
    )
    if resp.ok:
        data = resp.json()["data"]["children"]
        return [item["data"]["url"] for item in data]
    else:
        return []


def make_request(url: str) -> requests.Response:
    return requests.get(url, headers={"User-Agent": REDDIT_USER_AGENT})
