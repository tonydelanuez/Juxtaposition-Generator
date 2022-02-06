import re
import requests
from bs4 import BeautifulSoup
from typing import List

from juxgen.util import CommentFilter


def grab_page_html(url):
    """Make HTTP request and feed HTML to scraper"""
    resp = requests.get(url)
    if resp.ok:
        return BeautifulSoup(resp.text, "html.parser")
    else:
        return None


def grab_video_ids(page_soup):
    """Grab video id's from all front page videos"""
    vid_titles = page_soup.findAll("li", {"class": "pcVideoListItem"})
    return [
        vid["data-video-vkey"]
        for vid in vid_titles
        if vid["data-video-vkey"][:2] == "ph"
    ]


def scrape_video_comments(vid_id) -> List:
    """Grab the comments for a video"""
    vid_url = f"https://www.pornhub.com/view_video.php?viewkey={vid_id}"
    try:
        page = requests.get(vid_url)
        cmt_html = BeautifulSoup(page.text, "html.parser")
        full_comments = cmt_html.findAll("div", {"class": "commentMessage"})
        stripped = [c.find("span").text.strip() for c in full_comments]
        return [
            re.sub(r"[^\x00-\x7f]", r"", s)
            for s in stripped
            if CommentFilter.is_valid_comment(s)
        ]
    except requests.exceptions.HTTPError:
        return []
