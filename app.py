import json
import requests
import random
import re
from flask import Flask, request, send_from_directory
from bs4 import BeautifulSoup
from pymongo import MongoClient

# database setup
mongo_client = MongoClient()
db = mongo_client['juxtaposition']
db_comments = db.comments
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
	print("Request for comment.")
	count = db_comments.count()
	return db_comments.find()[random.randrange(count)]['comment']

def grab_page_html(url): 
	""" Make HTTP request and feed HTML to scraper """
	resp = requests.get(url)
	if resp.ok:
		return BeautifulSoup(resp.text, 'html.parser')
	else:
		return None 

def grab_video_ids(page_soup): 
	""" Grab video id's from all front page videos """ 
	vid_titles = page_soup.findAll("li", {"class":"js-pop videoblock videoBox"})
	return [vid['_vkey'] for vid in vid_titles if vid['_vkey'][:2] == "ph"]

def scrape_video_comments(vid_id): 
	""" Grab the comments for a video """
	vid_url = "https://www.pornhub.com/view_video.php?viewkey={}".format(vid_id)
	try:
		page = requests.get(vid_url)
		cmt_html = BeautifulSoup(page.text, 'html.parser')
		full_comments = cmt_html.findAll("div",{"class":"commentMessage"})
		stripped = [c.find("span").text.strip() for c in full_comments]
		return [re.sub(r'[^\x00-\x7f]', r'', s) for s in stripped if is_valid_comment(s)]
	except Exception: 
		return None

def is_valid_comment(comment_text): 
	""" Makes sure the comment is not spam, is not just asking for who it is, does not contain link, and is somewhat long """ 
	return (comment_text != "[[commentMessage]]") and (comment_text.find("who") == -1) and (comment_text.find("Who") == -1) and (comment_text.find("http") == -1) and (len(comment_text) > 15)

def populate_db():
	# Fetch and parse HTML
	print("Building comment database...")
	front_page = grab_page_html("https://www.pornhub.com/")

	videos = grab_video_ids(front_page)
	chosen_vids = random.sample(videos, 10)
	
	for vid in chosen_vids:
		print("Grabbing video ID: %s" % vid)
		scraped_comments = scrape_video_comments(vid)
		if scraped_comments:
			db_comments.insert_many([{'comment': comment} for comment in scraped_comments])
			print("Added comments to DB.")
		else:
			print("No comments for %s" % vid)


if __name__ == '__main__':
	populate_db()
	app.run()






