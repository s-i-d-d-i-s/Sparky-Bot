import requests
import discord
import random
import string
import json
import time
from . import constants

## Get a random colour
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


## Generate a hash for user verfication
def getUserNameHash():
	length = 10
	result_str = ''.join(random.choice(string.ascii_uppercase) for i in range(length))
	return result_str