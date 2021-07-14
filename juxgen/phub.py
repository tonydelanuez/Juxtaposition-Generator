import re
import requests

from juxgen.util import is_valid_comment
from bs4 import BeautifulSoup


def grab_page_html(url):
    """ Make HTTP request and feed HTML to scraper """
    resp = requests.get(url)
    if resp.ok:
        return BeautifulSoup(resp.text, 'html.parser')
    else:
        return None


def grab_video_ids(page_soup):
    """ Grab video id's from all front page videos """
    vid_titles = page_soup.findAll("li", {"class": "pcVideoListItem"})
    return [vid['data-video-vkey']
            for vid in vid_titles if vid['data-video-vkey'][:2] == "ph"]


def scrape_video_comments(vid_id):
    """ Grab the comments for a video """
    vid_url = "https://www.pornhub.com/view_video.php?viewkey={}".format(
        vid_id)
    try:
        page = requests.get(vid_url)
        cmt_html = BeautifulSoup(page.text, 'html.parser')
        full_comments = cmt_html.findAll("div", {"class": "commentMessage"})
        stripped = [c.find("span").text.strip() for c in full_comments]
        return [re.sub(r'[^\x00-\x7f]', r'', s)
                for s in stripped if is_valid_comment(s)]
    except requests.exceptions.HTTPError:
        return None
