import requests
import discord
import random

## Return Webpage Content
def getWebpage(url):
    return requests.get(url).content



## Get discord colour based on rating
def getDiscordColourByRating(rating):
    colour = discord.Colour.light_gray()
    if rating >=2500:
        colour = discord.Colour.red()
    elif rating >=2200:
        colour = discord.Colour.orange()
    elif rating >=2000:
        colour = discord.Colour(0xffff00)
    elif rating >= 1800:
        colour = discord.Colour.purple()
    elif rating >= 1600:
        colour = discord.Colour.blue()
    elif rating >=1200:
        colour = discord.Colour.green()
    return colour


## Verdict Image to Verdict

def verdict_img_to_verdict(img):
    verd = "WA"
    if img.find("tick-icon")!=-1:
        verd = "AC"
    elif img.find("clock_error")!=-1:
        verd = "TLE"
    elif img.find("alert-icon")!=-1:
        verd = "CE"
    elif img.find("runtime")!=-1:
        verd = "RE"
    return verd

def verdict_img_to_full(verd):
    if verd == "AC":
        return "Accepted"
    elif verd == "WA":
        return "Wrong Answer"
    elif verd == "CE":
        return "Compilation Error"
    elif verd == "TLE":
        return "Time Limit Exceed"
    elif verd == "RE":
        return "Runtime Error"    


## Get Random Colour
def getRandomColour():
    colour = random.choice([discord.Colour.purple(),discord.Colour.green(),discord.Colour.blue(),discord.Colour.orange()])
    return colour

## Convert rating to stars
def getStars(rating):
	if rating <1400:
		return "1★"
	elif rating <1600:
		return "2★"
	elif rating <1800:
		return "3★"
	elif rating <2000:
		return "4★"
	elif rating <2200:
		return "5★"
	elif rating <2500:
		return "6★"
	else:
		return "7★"

def isUserRated(username):
    url = "https://www.codechef.com/recent/user?page=0&user_handle={}".format(username)
    data = json.loads(getWebpage(url))
    if data['max_page'] != 0:
        return True
    return False


def scale_username(a,ln):
	a=str(a)
	while(len(a)<ln):
		a=a+" "
	longer = False
	if len(a)>ln:
		longer = True
	while len(a)>ln:
		a = a[:-1]
	if longer:
		a = a[:-3]
		a += "..."
	return a