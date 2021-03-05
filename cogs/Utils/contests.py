import bs4
import requests
import discord
import json
import time
import datetime


def get_formatted_contest_desc(id_str, start, duration, url, max_duration_len):
    em = '\N{EN SPACE}'
    sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
    desc = (f'`{em}{id_str}{em}| {em}{start}{em}| {em}{duration.rjust(max_duration_len, em)}{em}|' f'{em}`[`link {sq}`]({url} "Link to contest page")')
    return desc


def getFutureContest():
	desc = "**These are the upcoming contests.**"
	embed = discord.Embed(description=desc, color=discord.Colour.gold())

	current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
	url = f"https://clist.by/api/v1/contest/?resource__id=2&start__gt={current_time}&order_by=start&username=s5960r&api_key=2e6046e37a8c58f5f13464bea345d4ef5b17acbe"

	data = json.loads(requests.get(url).content)['objects']

	def convert(seconds): 
		seconds = seconds % (24 * 3600) 
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d" % (hour, minutes) 

	for i in range(min(5,len(data))):
		con = data[i]
		duration = convert(int(con['duration']))
		name = con['event']
		url = con['href']
		start = con['start'].replace("T"," ")
		em = '\N{EN SPACE}'
		sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
		desc = (f'`{em}{start}{em}| {em}{duration.rjust(5, em)}{em}| {em}`[`link {sq}`]({url} "Link to contest page")')
		embed.add_field(name=f"{name}", value= desc  ,inline=False)
		
	return embed

def getPastContest():
	desc = "**These are the past contests.**"
	embed = discord.Embed(description=desc, color=discord.Colour.gold())

	current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
	url = f"https://clist.by/api/v1/contest/?resource__id=2&end__lt={current_time}&order_by=-start&username=s5960r&api_key=2e6046e37a8c58f5f13464bea345d4ef5b17acbe"

	data = json.loads(requests.get(url).content)['objects']

	def convert(seconds): 
		seconds = seconds % (24 * 3600) 
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d" % (hour, minutes) 

	for i in range(min(5,len(data))):
		con = data[i]
		duration = convert(int(con['duration']))
		name = con['event']
		url = con['href']
		start = con['start'].replace("T"," ")
		em = '\N{EN SPACE}'
		sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
		desc = (f'`{em}{start}{em}| {em}{duration.rjust(5, em)}{em}| {em}`[`link {sq}`]({url} "Link to contest page")')
		embed.add_field(name=f"{name}", value= desc  ,inline=False)
		
	return embed

def getPresentContest():
	desc = "**These are the running contests.**"
	embed = discord.Embed(description=desc, color=discord.Colour.gold())

	current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
	url = f"https://clist.by/api/v1/contest/?resource__id=2&end__gt={current_time}&start__lt={current_time}&order_by=-start&username=s5960r&api_key=2e6046e37a8c58f5f13464bea345d4ef5b17acbe"

	data = json.loads(requests.get(url).content)['objects']

	def convert(seconds): 
		seconds = seconds % (24 * 3600) 
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d" % (hour, minutes) 

	for i in range(min(5,len(data))):
		con = data[i]
		duration = convert(int(con['duration']))
		name = con['event']
		url = con['href']
		start = con['start'].replace("T"," ")
		em = '\N{EN SPACE}'
		sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
		desc = (f'`{em}{start}{em}| {em}{duration.rjust(5, em)}{em}| {em}`[`link {sq}`]({url} "Link to contest page")')
		embed.add_field(name=f"{name}", value= desc  ,inline=False)
		
	return embed