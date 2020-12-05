import os


# Enter Your Coding Profiles, If you don't have leave it blank
YOURCF = "s59_60r"
YOURCC = "s59_60r"
YOURATC = "s59_60r"
GITHUB = "https://github.com/s-i-d-d-i-s/Sparky-Bot"
BOTIMAGE = "https://s3.amazonaws.com/codechef_shared/sites/default/files/uploads/pictures/76a39c37b49f7b590c50e01bfc77b644.JPG"
VERSION = "1.0"

BASE_DIR = __file__
BASE_DIR = BASE_DIR[0:BASE_DIR.find("\\Utils")]

DATABASE_DIR = os.path.join(BASE_DIR,"Data/database.db")