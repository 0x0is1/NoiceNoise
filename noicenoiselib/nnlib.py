from bs4 import BeautifulSoup as soup
import requests, pytz, base64
from datetime import datetime

BASEURL1 = base64.b64decode("aHR0cHM6Ly93dy5hcGkuaWhlYXJ0LmNvbS9hcGkvdjMvcG9kY2FzdC8=").decode(f"utf-{7+1}")
BASEURL2 = base64.b64decode("aHR0cHM6Ly93ZWJhcGkucmFkaW9lZGl0LmloZWFydC5jb20vZ3JhcGhxbD9xdWVyeT0=").decode(f"utf-{7+1}")

ist = pytz.timezone("Asia/Kolkata")

class urls:
    getPodcasts = BASEURL2
    podcastById = BASEURL1 + "podcasts/"
    episodesByPid = "/episodes?newEnabled=false&limit=15&sortBy=startDate-desc"
    episodeByEid = BASEURL1 + "episodes/"
    categoryByCid = BASEURL1 + "categories/"

class podcastOpts:
    featured = "Featured"
    popular = "Popular"

def getPodcastslist(ptype):
    podcasts = []
    query = f"query%20{ptype}Podcasts%28%24query%3A%20QueryInput%21%2C%20%24locale%3A%20String%29%20%7B%20{ptype}_podcasts%3A%20leads%28query%3A%20%24query%2C%20locale%3A%20%24locale%29%20%7B%20subtitle%2C%20title%2C%20img_uri%2C%20link%20%7B%20urls%20%7B%20web%20%7D%20%7D%2C%20catalog%20%7B%20id%20%7D%20%7D%20%7D%20&variables=%7B%22locale%22%3A%22en-WW%22%2C%22query%22%3A%7B%22subscription%22%3A%7B%22tags%22%3A%5B%22collections%2Fpopular-podcasts%22%2C%22countries%2FWW%22%5D%7D%7D%7D"
    response = requests.get(url=f"{urls.getPodcasts}{query}").json()
    for i in response["data"][f"{ptype}_podcasts"]:
        podcasts.append((i["catalog"]["id"], i["subtitle"], i["title"], i["img_uri"]))
    return podcasts

def getPodcastInfo(pid):
    response = requests.get(url=f"{urls.podcastById}{pid}").json()
    podcast = [response["id"], response["title"], response["description"], response["imageUrl"]]
    for i in response["socialMediaLinks"]:
        name = i["name"].split("_")[0].capitalize()
        link = i["link"]
        if "Twitter" in name: link=f"https://twitter.com/{link}"
        if "Instagram" in name: link=f"https://instagram.com/{link}"
        podcast.append((name, link))
    return podcast

def getEpisodesInfo(pid):
    podcast = []
    response = requests.get(url=f"{urls.podcastById}{pid}{urls.episodesByPid}").json()   
    for i in response["data"]:
        eid = i["id"]
        pid = i["podcastId"]
        title = i["title"]
        duration = f'{int(i["duration"]/60)} mins'
        description = i["description"].split("\n")[0]
        startDate = datetime.fromtimestamp(i["startDate"]/1000, ist).ctime()
        podcast.append((eid, pid, title, duration, description, startDate))
    return podcast

def getEpisode(eid):
    podcast = []
    response = requests.get(url=f"{urls.episodeByEid}{eid}").json()
    i = response["episode"]
    eid = i["id"]
    pid = i["podcastId"]
    title = i["title"]
    duration = f'{int(i["duration"]/60)} mins'
    description = soup(i["description"], 'html.parser').text.split("\n")[0]
    startDate = datetime.fromtimestamp(i["startDate"]/1000, ist).ctime()
    imageUrl = i["imageUrl"]
    mediaUrl = i["mediaUrl"]
    podcast.append((eid, pid, title, duration, description, startDate, imageUrl, mediaUrl))
    return podcast

def getCategoriesList():
    podcasts = []
    query = f"%20query%20Topics%28%24query%3A%20QueryInput%21%2C%20%24locale%3A%20String%29%20%7B%20topics%3A%20leads%28query%3A%20%24query%2C%20locale%3A%20%24locale%29%20%7B%20img_uri%2C%20title%2C%20link%20%7B%20urls%20%7B%20web%2C%20device%20%7D%20%7D%20%7D%20%7D%20&variables=%7B%22locale%22%3A%22en-WW%22%2C%22query%22%3A%7B%22subscription%22%3A%7B%22tags%22%3A%5B%22collections%2Fpodcast-directory%22%2C%22countries%2FWW%22%5D%7D%7D%7D"
    response = requests.get(url=f"{urls.getPodcasts}{query}").json()
    for i in response["data"]["topics"]:
        podcasts.append((i["title"], i["img_uri"], i["link"]["urls"]["device"].replace("ihr://goto/podcast/category/", "")))
    return podcasts

def getCategory(cid):
    podcasts = []
    response = requests.get(url=f"{urls.categoryByCid}{cid}").json()
    podcasts.append(response["name"])
    for i in response["podcasts"]:
        startDate = datetime.fromtimestamp(i["lastUpdated"]/1000, ist).ctime()
        podcasts.append((i["id"], i["title"], i["description"], i["imageUrl"], startDate))
    return podcasts
