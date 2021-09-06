import discord
from discord.ext import commands
from .Utils import contests,database,cc_commons,discord_commons
import asyncio
import random
from discord.utils import get
import os
import pickle
import json

def isLong(name):
	ls=[
		'January Challenge',
		'February Challenge',
		'March Challenge',
		'April Challenge',
		'May Challenge',
		'June Challenge',
		'July Challenge',
		'August Challenge',
		'September Challenge',
		'October Challenge',
		'November Challenge',
		'December Challenge',
	]
	for x in ls:
		if name.find(x)!=-1:
			return True
	return False


class Features(commands.Cog):
	"""docstring for Features"""
	def __init__(self, client):
		self.client = client
		self.db=database.DB()
	@commands.Cog.listener()
	async def on_ready(self):
		print("Features is online")

	@commands.command(brief='Scan a user')
	async def scan(self, ctx,username=None):
		"""Scan a user"""
		if username==None:
			await ctx.send('```Enter a username, e.g  " =scan s59_60r " ```')
			return 

		data=cc_commons.getUserData_easy(username,self.db)
		desc = f"** Scanning {data['name']} aka [{username}](https://www.codechef.com/users/{username})**"
		colour = discord_commons.getDiscordColourByRating(int(data['rating']))


		solved_problems = json.loads(data['solved_problems'])
		submission_stats = json.loads(data['submission_stats'])
		rating_data = json.loads(data['rating_data'])
		best_rating = max([int(x['rating']) for x in rating_data['date_versus_rating']['all']])
		best_star = discord_commons.getStars(best_rating)
		contest_part_in = len(rating_data['date_versus_rating']['all'])
		long_contest = sum([isLong(x['name']) for x in rating_data['date_versus_rating']['all']])
		short_contest = contest_part_in - long_contest
		best_rank = min([[int(x['rank']),x['name']] for x in rating_data['date_versus_rating']['all']],key = lambda t: t[0])

		embed = discord.Embed(description=desc, color=colour)
		embed.add_field(name='Rating', value=data['rating'], inline=True)
		embed.add_field(name='Stars', value=discord_commons.getStars(data['rating']), inline=True)
		embed.add_field(name='Total Contests', value=contest_part_in, inline=True)
		
		embed.add_field(name='Best Rating', value=best_rating, inline=True)
		embed.add_field(name='Best Star', value=best_star, inline=True)
		embed.add_field(name='Best Rank', value="{} in {}".format(best_rank[0],best_rank[1]), inline=True)


		embed.add_field(name='Long Contests', value=long_contest, inline=True)
		embed.add_field(name='Short Contests', value=short_contest, inline=True)
		embed.add_field(name='AC Solutions', value=str(int(submission_stats["solutions_accepted"])+int(submission_stats["solutions_partially_accepted"])), inline=True)

		embed.add_field(name='WA', value=submission_stats["wrong_answers"], inline=True)
		embed.add_field(name='TLE', value=submission_stats["time_limit_exceeded"], inline=True)
		embed.add_field(name='CE', value=submission_stats["compile_error"], inline=True)

		embed.set_thumbnail(url=data['profile_pic'])
		await ctx.send(embed=embed)

	
def setup(client):
	client.add_cog(Features(client))