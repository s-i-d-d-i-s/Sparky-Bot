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


def getRatingGraph(handles,apiObj):
	plt.clf()
	plt.axes().set_prop_cycle(rating_color_cycler)
	labels=[]
	for i in range(len(handles)):
		handle = handles[i]
		data = user.getRatingHistory(handle,apiObj)
		ratings = []
		times = []
		cur_rating=0
		for d in data['date_versus_rating']['all']:
			times.append(dt.datetime.strptime(d['end_date'],'%Y-%m-%d %H:%M:%S'))
			ratings.append(int(d['rating']))	
			cur_rating=int(d['rating'])
		plt.plot(times,ratings,linestyle='-',marker='o',markersize=6,markerfacecolor='white',markeredgewidth=0.5)
		labels.append(f"{handle} : {cur_rating}")
	plot_rating_bg(constants.RATED_RANKS)
	plt.gcf().autofmt_xdate()
	plt.legend(labels, loc='upper left')
	return get_current_figure_as_file()


def getPeakRatingGraph(handles,apiObj):
	plt.clf()
	plt.axes().set_prop_cycle(rating_color_cycler)
	labels=[]
	for i in range(len(handles)):
		handle = handles[i]
		data = user.getRatingHistory(handle,apiObj)
		ratings = []
		times = []
		last = -9999
		cur_rating=0
		for d in data['date_versus_rating']['all']:
			if int(d['rating']) > last:
				times.append(dt.datetime.strptime(d['end_date'],'%Y-%m-%d %H:%M:%S'))
				ratings.append(int(d['rating']))	
				cur_rating=int(d['rating'])
				last = cur_rating
		plt.plot(times,ratings,linestyle='-',marker='o',markersize=6,markerfacecolor='white',markeredgewidth=0.5)
		labels.append(f"{handle} : {cur_rating}")
	plot_rating_bg(constants.RATED_RANKS)
	plt.gcf().autofmt_xdate()
	plt.legend(labels, loc='upper left')
	return get_current_figure_as_file()

def getSolvedHistogram(handles,datalist):
	plt.clf()
	plt.xlabel('Problem Levels')
	plt.ylabel('Number solved')
	labels = []
	for i in range(len(handles)):
		labels.append(f"{handles[i]} : {len(datalist[i])}")
	plt.hist(datalist, bins=[0,1,2,3,4,5,6],align='left')
	plt.legend(labels, loc='upper right')
	return get_current_figure_as_file()