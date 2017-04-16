#Importing the required packages
import bs4
import random
import http.client
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


# URL to scrape
#scrape_url = "https://www.pornhub.com/view_video.php?viewkey=ph55ddb463aab3d"
scrape_url = "https://www.pornhub.com/"
#open up web request using short hand request earlier (urlopen)

try:
    uClient = uReq(scrape_url)
    page_html = uClient.read()
except http.client.IncompleteRead as e:
    page_html = e.partial
uClient.close()

#parse the HTML
page_soup = soup(page_html, "html.parser")

#Grab video id's from all front page videos
videos = [];
vid_titles = page_soup.findAll("li", {"class":"videoblock videoBox"})
for vid in vid_titles:
	ID = vid['_vkey']
	if ID[:2] == "ph":
		videos.append(ID)

video_bounds = len(videos) - 1
#print(video_bounds)
video_selected = random.randrange(video_bounds)
#print("SELECTED INDEX: " + str(video_selected))
player_id = "placeholder"
for i, val in enumerate(videos):
	#print(val)
	if i == video_selected:
		player_id = val
		#print("*****START******")
		#print(val)
		#print("CHECK: " + str(player_id))
		#print("*****FINISH******")

#print("Player ID: " + str(player_id))
video_scrape_url = "https://www.pornhub.com/view_video.php?viewkey="+player_id
#open up web request using short hand request earlier (urlopen)
#print(video_scrape_url)
comments = []
while(len(comments) == 0):
	try:
	    uClient = uReq(video_scrape_url)
	    cmt_html = uClient.read()
	except httplib.IncompleteRead as e:
	    cmt_html = e.partial

	uClient.close()

	cmt_soup = soup(cmt_html, "html.parser")
	comments = cmt_soup.findAll("div",{"class":"commentMessage"})

#open up a csv file to write to 
filename = "comments.csv"
f = open(filename, "w")
headers = "comment\n"
f.write(headers)


#print("about to print comments")

for comment in comments:
	theText = comment.find("span").text
	theText.replace(",", " ")
	theText.replace("\n", " ")
	filter_check = (theText.find("who") == -1) and (theText.find("Who") == -1) and (theText.find("http") == -1)
	if(theText != "[[commentMessage]]" and len(theText) > 15 and filter_check):f.write(theText + ",")

f.close()





