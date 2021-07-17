import atexit
import datetime
import json
import logging
import os
import random
import sys

from juxgen.phub import grab_page_html, grab_video_ids, scrape_video_comments
from juxgen.reddit import get_top_images, serve_image_from_reddit

from apscheduler.schedulers.background import BackgroundScheduler
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

# flask setup
app = Flask(__name__, static_url_path='')


class DataStore:
    def __init__(self,
                 name,
                 data=None,
                 fetch_fn=(lambda: None)):
        self.name = name
        self.data = data or []
        self.upload_counter = 0
        self.upload_refresh_interval = 10
        self.last_updated = datetime.datetime.now(),
        self.fetch_fn = fetch_fn

comments = object()
photos = object()

@app.route('/')
def return_wallpaper():
    return send_from_directory('app', 'index.html')

# Serve static files - needed to get JS/CSS
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('app', path)

@app.route('/healthcheck')
def healthcheck():
    return {'status': 200, 'message': 'OK'}

@app.route('/get-comment')
def get_random_comment():
    logger.debug("Request for comment.")
    return random.choice(comments.data)

@app.route('/get-image')
def get_image():
    logger.info("Serving image.")
    return serve_image_from_reddit(photos.data)

def fetch_comments() -> List[str]:
    logger.info('Starting comment fetch...')
    front_page = grab_page_html("https://www.pornhub.com/")
    comment_data = []
    for vid in random.sample(grab_video_ids(front_page), 10):
        scraped_comments = scrape_video_comments(vid)
        if scraped_comments:
            comment_data.extend(scraped_comments)
            logger.info("Added {} comments to DB.".format(len(scraped_comments)))
        else:
            logger.info("No comments found for video ID {}".format(vid))
    return comment_data


def populate_data(model):
    logger.info('populate_data called with model: {}'.format(model.name))
    data = model.fetch_fn()

    if model.upload_counter > model.upload_refresh_interval:
        model.data = data
        model.upload_counter = 0
    else:
        model.data.extend(data)
        model.upload_counter += 1
    model.last_updated = datetime.datetime.now()
    if model.name == 'photos':
        logger.info("READ_______")
        logger.info(random.choice(model.data))

def populate_photos_hook():
    populate_data(photos)

def populate_comments_hook():
    populate_data(comments)

if __name__ == '__main__':
    # populate both databases
    # add scheduled tasks

    port = int(os.environ.get('PORT', 5000))

    comments = DataStore('comments', fetch_fn=fetch_comments)
    photos = DataStore('photos', fetch_fn=get_top_images)

    populate_comments_hook()
    populate_photos_hook()

    scheduler = BackgroundScheduler()
    scheduler.add_job(populate_comments_hook, trigger='interval', seconds=600)
    scheduler.add_job(populate_photos_hook, trigger='interval', seconds=600)

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run(host='0.0.0.0', port=port)

