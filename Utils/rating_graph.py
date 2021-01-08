from requests_html import HTMLSession
import json
from matplotlib import pyplot as plt
import discord
import datetime as dt
from cycler import cycler
import time,os
from collections import namedtuple
import seaborn as sns
from .constants import TEMP_DIR
import io

Rank = namedtuple('Rank', 'low high title title_abbr color_graph color_embed')

RATED_RANKS = (
	Rank(-10 ** 9, 1400, '1Star', 'N', '#7F7F7F', 0x808080),
	Rank(1400, 1600, '2Star', 'P', '#37963B', 0x008000),
	Rank(1600, 1800, '3Star', 'S', '#4C7FE5', 0x03a89e),
	Rank(1800, 2000, '4Star', 'E', '#684273', 0x0000ff),
	Rank(2000, 2200, '5Star', 'CM', '#FFD819', 0xaa00aa),
	Rank(2200, 2500, '6Star', 'M', '#FF9819', 0xff8c00),
	Rank(2500, 3000, '7Star', 'IM', '#E91A34', 0xf57500),
	Rank(3000, 10 ** 9, '7Star2', 'LGM', '#E91A34', 0xcc0000)
)

rating_color_cycler = cycler('color', ['#5d4dff', '#009ccc', '#00ba6a', '#b99d27', '#cb2aff'])

def getRatingHistory(handle):
	temp = "https://www.codechef.com/users/{}".format(handle)
	session = HTMLSession()
	r = session.get(temp)
	r = r.content
	r = str(r)
	idx = r.find("date_versus_rating")
	new_r = r[idx-1:]
	idx = new_r.find("}]")
	new_r = new_r[:-(len(new_r)-idx)-1]
	new_r = "{" + new_r + "\"}]}}"
	new_r.replace("null","\"null\"")
	new_r = new_r.replace("\\",'')
	new_r = new_r.replace("\'",'')
	data = json.loads(new_r)
	return data


def get_current_figure_as_file():
	filename = os.path.join(TEMP_DIR, f'tempplot_{time.time()}.png')
	plt.savefig(filename, facecolor=plt.gca().get_facecolor(), bbox_inches='tight', pad_inches=0.25)

	with open(filename, 'rb') as file:
		discord_file = discord.File(io.BytesIO(file.read()), filename='plot.png')
	os.remove(filename)
	return discord_file


def plot_rating_bg(ranks):
	ymin, ymax = plt.gca().get_ylim()
	bgcolor = plt.gca().get_facecolor()
	for rank in ranks:
		plt.axhspan(rank.low, rank.high, facecolor=rank.color_graph, alpha=0.5, edgecolor=bgcolor, linewidth=0.5)

	locs, labels = plt.xticks()
	for loc in locs:
		plt.axvline(loc, color=bgcolor, linewidth=0.5)
	plt.ylim(ymin, ymax)


def getRatingGraph(handle):
	data = getRatingHistory(handle)
	ratings = []
	times = []
	for d in data['date_versus_rating']['all']:
		times.append(dt.datetime.strptime(d['end_date'],'%Y-%m-%d %H:%M:%S'))
		ratings.append(int(d['rating']))
	plt.clf()
	plt.axes().set_prop_cycle(rating_color_cycler)
	plt.plot(times,ratings,linestyle='-',marker='o',markersize=6,markerfacecolor='white',markeredgewidth=0.5)
	plot_rating_bg(RATED_RANKS)
	plt.gcf().autofmt_xdate()
	return get_current_figure_as_file()