import requests
import discord
import random
import json
import time
from . import constants

## Return Webpage Content
def getWebpage(url):
    return requests.get(url).content

def valid_username(username):
    return True


def isCooled(cooldown,userid,typ=None):

    if typ !=None:
        if str(userid) in cooldown.keys():
            print(userid,cooldown[str(userid)])
            if time.time()<= cooldown[str(userid)]+constants.RANKLIST_COOLDOWN:
                return False
        return True
    elif typ == 1:
        if str(userid) in cooldown.keys():
            print(userid,cooldown[str(userid)])
            if time.time()<= cooldown[str(userid)]+constants.ORG_RANKLIST_COOLDOWN:
                return False
        return True


def get_ranklist(guild_id,db):
    """Get a Organization Ranklist to the Server"""
    data = db.fetch_college_data(guild_id)
    return data

def get_user_by_discord_id(userid,guildid,db):
    data = db.fetch_user_data(str(userid),str(guildid))
    if len(data)==0:
        data=None
    else:
        if data[0][3] != 'NULL':
            data=data[0][3]
        else:
            data=None
    return data
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
 


## Get Random Colour
def getRandomColour():
    colour = random.choice([discord.Colour.purple(),discord.Colour.green(),discord.Colour.blue(),discord.Colour.orange()])
    return colour

## Convert rating to stars
def getStars(rating):
    rating = int(rating)
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

def isUserRated(username,apiObj):
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