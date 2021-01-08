import os


# Enter Your Coding Profiles, If you don't have leave it blank
GITHUB = "https://github.com/s-i-d-d-i-s/Sparky-Bot"

BOTIMAGE = "https://i.ibb.co/YpTJHzh/Sparky-Logo.png"

OWNER = "762226757864390666"

NON_OWNER_MSG = "```You can't run these commands, this instance of Sparky is owned by someone else.\nYou can set your own instance of bot to run these commands, as these commands can mess up a lot of stuff.```"

VERSION = "1.4"

DEBUG = False
BASE_DIR ="/app"

if DEBUG == True:
	BASE_DIR = "C:\\Users\\Siddharth-Dev\\Documents\\Github\\Sparky-Deploy\\sparky-bot-cc"

DATABASE_DIR = os.path.join(BASE_DIR,"Data/database.db")

TEMP_DIR = os.path.join(BASE_DIR,"Data")