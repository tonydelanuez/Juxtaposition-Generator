import logging
import random
from flask import Blueprint, send_from_directory

from juxgen.util import serve_image

routes = Blueprint("juxgen", __name__)
logger = logging.getLogger("juxgen")


@routes.route("/")
def return_wallpaper():
    return send_from_directory("frontend", "index.html")


# Serve static files - needed to get JS/CSS
@routes.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("frontend", path)


@routes.route("/healthcheck")
def healthcheck():
    return {"status": 200, "message": "OK"}


@routes.route("/get-comment")
def get_random_comment():
    from app import db
    from juxgen.models import Comment

    logger.debug("Request for comment.")
    comment = db.session.query(Comment).get_random()
    return comment.text


@routes.route("/get-image")
def get_image():
    from app import db
    from juxgen.models import Wallpaper

    logger.debug("Request for wallpaper")
    wallpaper = db.session.query(Wallpaper).get_random()
    return serve_image(wallpaper.raw)
