import random
from flask import Response
from json.decoder import JSONDecodeError
from typing import List, Dict
import requests

REDDIT_USER_AGENT = 'x86_64_GNU/Linux:juxtaposition-generator:v0.0.1 (by /u/TonyDarko)'

def get_top_images() -> List[Dict]:
    timespan = random.choice(['month', 'day', 'year', 'all'])
    print("Fetching images from reddit, timespan: {}".format(timespan))
    resp = make_request(
        "https://www.reddit.com/r/wallpaper/top/.json?t={}&limit=100".format(timespan))
    if resp.ok:
        data = resp.json()['data']['children']
        print("{} images fetched".format(len(data)))
        return data
    else:
        print("could not fetch images from reddit")
        print("{}".format(resp.reason))
        return [{}]


def make_request(url: str) -> requests.Response:
    return requests.get(
        url, headers={
            'User-Agent': REDDIT_USER_AGENT
        }
    )


def serve_image_from_reddit(images: List[Dict]) -> requests.Response:
    image = random.choice(images)
    resp = requests.get(image['data']['url'], stream=True)

    resp.headers['User-Agent'] = REDDIT_USER_AGENT
    resp.headers['Content-Disposition'] = 'attachment; filename="image.png"'
    resp.headers['Cache-Control'] = 'no-store'

    return Response(resp.content, headers=dict(resp.headers))
