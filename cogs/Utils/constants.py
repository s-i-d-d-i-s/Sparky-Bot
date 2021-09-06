import os
from collections import namedtuple
import pathlib

GITHUB = "https://github.com/s-i-d-d-i-s/Sparky-Bot"
BOTIMAGE = "https://i.ibb.co/hC725X4/SPARKY-2.png"
OWNER = "762226757864390666"
NON_OWNER_MSG = "```You can't run these commands, this instance of Sparky is owned by someone else.\nYou can set your own instance of bot to run these commands, as these commands can mess up a lot of stuff.```"
VERSION = "4.0"
BASE_DIR ="/app"


HANDLE_VERTIFICATION_TIME = 60
USERDATA_UPDATE_COOLDOWN = 3600


TOKEN = os.getenv('TOKEN', 'NO_TOKEN')
DEBUG= TOKEN == 'NO_TOKEN'
if DEBUG==True:
	print("Debug Mode")
	BASE_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()


# DATABASE_DIR = os.path.join(BASE_DIR,"Data/database.db")
TEMP_DIR = os.path.join(BASE_DIR,"Data")

Rank = namedtuple('Rank', 'low high title title_abbr color_graph color_embed')
RATED_RANKS = (
	Rank(-10 ** 9, 1400, '1Star', 'N', '#7F7F7F', 0x808080),
	Rank(1400, 1600, '2Star', 'P', '#37963B', 0x008000),
	Rank(1600, 1800, '3Star', 'S', '#4C7FE5', 0x03a89e),
	Rank(1800, 2000, '4Star', 'E', '#684273', 0x0000ff),
	Rank(2000, 2200, '5Star', 'CM', '#FFD819', 0xaa00aa),
	Rank(2200, 2500, '6Star', 'M', '#FF9819', 0xff8c00),
	Rank(2500, 3000, '7Star', 'IM', '#E91A34', 0xf57500),
)
