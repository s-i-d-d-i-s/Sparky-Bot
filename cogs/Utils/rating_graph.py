from matplotlib import pyplot as plt
import discord
import datetime as dt
from cycler import cycler
import time,os
import seaborn as sns
from . import constants
from .import user
import io


rating_color_cycler = cycler('color', ['#5d4dff', '#009ccc', '#00ba6a', '#b99d27', '#cb2aff'])



def get_current_figure_as_file():
	filename = os.path.join(constants.TEMP_DIR, f'tempplot_{time.time()}.png')
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
	data = user.getRatingHistory(handle)
	ratings = []
	times = []
	for d in data['date_versus_rating']['all']:
		times.append(dt.datetime.strptime(d['end_date'],'%Y-%m-%d %H:%M:%S'))
		ratings.append(int(d['rating']))
	plt.clf()
	plt.axes().set_prop_cycle(rating_color_cycler)
	plt.plot(times,ratings,linestyle='-',marker='o',markersize=6,markerfacecolor='white',markeredgewidth=0.5)
	plot_rating_bg(constants.RATED_RANKS)
	plt.gcf().autofmt_xdate()
	return get_current_figure_as_file()