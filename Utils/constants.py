import os


# Enter Your Coding Profiles, If you don't have leave it blank
YOURCF = "s59_60r"
YOURCC = "s59_60r"
YOURATC = "s59_60r"
GITHUB = "https://github.com/s-i-d-d-i-s/Sparky-Bot"
BOTIMAGE = "https://i.ibb.co/YpTJHzh/Sparky-Logo.png"
VERSION = "1.0"
DEBUG = False
BASE_DIR ="/app"
if DEBUG == True:
	BASE_DIR = "C:\\Users\\Siddharth-Dev\\Documents\\Github\\Sparky-Deploy\\sparky-bot-cc"

DATABASE_DIR = os.path.join(BASE_DIR,"Data/database.db")