import logging
import random
import requests
from typing import List
from flask import Blueprint

from juxgen.reddit import get_top_images
from juxgen.phub import grab_page_html, grab_video_ids, scrape_video_comments

logger = logging.getLogger("juxgen")
cmds = Blueprint("manage", __name__)


@cmds.cli.command("init_db")
def init_db():
    from app import db
    from juxgen.models import Comment, GeneratedCombo, Wallpaper

    print("Initializing db")
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("DB Initialized")


@cmds.cli.command("seed_comments")
def fetch_comments() -> List[str]:
    from app import db
    from juxgen.models import Comment

    logger.info("Starting comment fetch...")
    front_page = grab_page_html("https://www.pornhub.com/")
    comment_data = []
    for vid in random.sample(grab_video_ids(front_page), 9):
        scraped_comments = scrape_video_comments(vid)
        if scraped_comments:
            for comment in scraped_comments:
                c = Comment(text=comment)
                db.session.add(c)
            logger.info("Added {} comments to DB.".format(len(scraped_comments)))
        else:
            logger.info("No comments found for video ID {}".format(vid))
        db.session.commit()
    return comment_data


@cmds.cli.command("seed_images")
def fetch_images():
    from app import db
    from juxgen.models import Wallpaper

    image_urls = get_top_images()
    logger.info(f"Found {len(image_urls)}")
    for url in image_urls:
        resp = requests.get(url, stream=True)
        wallpaper = Wallpaper(raw=resp.content)
        db.session.add(wallpaper)
    db.session.commit()
    logger.info(f"Added {len(image_urls)} images to DB")
