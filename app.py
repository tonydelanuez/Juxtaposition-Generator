import logging
import os
import random
import sys

from juxgen.phub import grab_page_html, grab_video_ids, scrape_video_comments
from juxgen.reddit import get_top_images, serve_image_from_reddit

from flask import Flask, request, send_from_directory
from typing import List


logger = logging.getLogger('juxgen')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

comments = []

# flask setup
app = Flask(__name__, static_url_path='')

# Main route


@app.route('/')
def return_wallpaper():
    return send_from_directory('app', 'index.html')

# Serve static files - needed to get JS/CSS


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('app', path)

# Testing comment


@app.route('/healthcheck')
def healthcheck():
    return {'status': 200, 'message': 'OK'}


@app.route('/get-comment')
def get_random_comment():
    logger.debug("Request for comment.")
    return random.choice(comments)


@app.route('/get-image')
def get_image():
    logger.info("Serving image.")
    return serve_image_from_reddit(get_top_images())


@app.route('/populate-db')
def populate_db() -> List[str]:
    # Fetch and parse HTML
    logger.info("Building comment database...")
    front_page = grab_page_html("https://www.pornhub.com/")

    videos = grab_video_ids(front_page)
    chosen_vids = random.sample(videos, 10)

    for vid in chosen_vids:
        logger.info("Grabbing video ID: %s" % vid)
        scraped_comments = scrape_video_comments(vid)
        if scraped_comments:
            comments.extend(scraped_comments)
            logger.info(
                "Added {} comments to DB.".format(
                    len(scraped_comments)))
        else:
            logger.info("No comments for {}".format(vid))
    return comments


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    populate_db()
    app.run(host='0.0.0.0', port=port)
