import bs4
import http.client
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import random
import webbrowser

scrape_url = "https://www.pornhub.com/video"

def grab_page_html(url): 
	""" Make HTTP request and feed HTML to scraper """ 
	try:
		uClient = uReq(url)
		page_html = uClient.read()
	except http.client.IncompleteRead as e:
		page_html = e.partial
	finally: 
		uClient.close()
		return page_html

def grab_video_ids(page_soup): 
	""" Grab video id's from all front page videos """ 
	videos = []
	vid_titles = page_soup.findAll("li", {"class":"js-pop videoblock videoBox"})
	for vid in vid_titles:
		ID = vid['_vkey']
		if ID[:2] == "ph":
			videos.append(ID)
	return videos

def scrape_video_comments(url): 
	""" Grab the comments for a video """ 
	comments = []
	while not comments:
		try:
			uClient = uReq(url)
			cmt_html = uClient.read()
		except:
			cmt_html = e.partial
		finally: 
			uClient.close()
			cmt_soup = soup(cmt_html, "html.parser")
			comments = cmt_soup.findAll("div",{"class":"commentMessage"})
	return comments

def is_valid_comment(comment_text): 
	""" Makes sure the comment is not spam, is not just asking for who it is, does not contain link, and is somewhat long """ 
	return (comment_text != "[[commentMessage]]") and (comment_text.find("who") == -1) and (comment_text.find("Who") == -1) and (comment_text.find("http") == -1) and (len(comment_text) > 15)

def main(): 
	# Fetch and parse HTML
	page_html = grab_page_html(scrape_url)
	page_soup = soup(page_html, "html.parser")

	videos = grab_video_ids(page_soup)
	player_id = random.choice(videos)
	
	print("Grabbing video ID: %s" % player_id)
	video_scrape_url = "https://www.pornhub.com/view_video.php?viewkey="+player_id

	print("Grabbing comments for video")
	comments = scrape_video_comments(video_scrape_url)

	#open up a csv file to write to 
	filename = "comments.csv"
	f = open(filename, "w")
	headers = "comment\n"
	f.write(headers)

	for comment in comments:
		comment_text = comment.find("span").text.strip()
		print(comment_text)
		if is_valid_comment(comment_text): 
			print("is valid")
			f.write(comment_text + ",")
	f.close()

if __name__ == '__main__': 
	main()






