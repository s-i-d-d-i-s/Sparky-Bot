import discord
from discord.ext import commands
from .Utils import contests,discord_commons, cc_api,database,table
import asyncio
import random
from discord.utils import get
import time
import json
import os
import pickle

COOLDOWN = 30
CACHE_TL = 300
class Ranklist(commands.Cog):
	"""docstring for Ranklist"""
	def __init__(self, client):
		self.client = client
		self.cooldown = {}
		self.db = database.DB()
		self.api = cc_api.CodechefAPI(self.db)
		self.cache = {}

	@commands.Cog.listener()
	async def on_ready(self):
		print("Ranklist is online")


	@commands.command(brief='Clear Ranklist Cache')
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def clear(self,ctx):
		self.cache = {}

	@commands.command(brief='Display ranklist for a contests')
	@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def ranklist(self,ctx,contest_id=None):
		"""Get Ranklist for a contest"""
		if contest_id == None:
			await ctx.send('```Please enter a contest code to get the ranklist```')
			return
		cur_time = int(time.time())
		ranklist = []
		data = None
		print(cur_time)
		if contest_id in self.cache and self.cache[contest_id][0]+CACHE_TL>cur_time:
			print("Using Cache")
			data = json.loads(self.cache[contest_id][1])
		else:
			print("Fetching New")	
			data = self.api.getRanklistContest(contest_id)
			print("Data Fetched")
			self.cache[contest_id] = [cur_time,json.dumps(data)]


		guild_users = self.db.fetch_guild_users(ctx.message.guild.id)
		handles = set()
		for x in guild_users:
			handles.add(x['cchandle'])
		print(handles)
		for i in range(len(data)):
			if data[i]['username'] in handles:
				ranklist.append(data[i])
		print(ranklist)	
			
		
		print(ranklist)
		style = table.Style('{:>}  {:<}  {:<}  {:<}')
		t = table.Table(style)
		t += table.Header('#', 'Handle', 'Score','Penalty')
		t += table.Line()
		for i in range(len(ranklist)):
			t += table.Data(ranklist[i]['rank'], ranklist[i]['username'], ranklist[i]['totalScore'], ranklist[i]['penalty'])

		ranklist = '```\n'+str(t)+'\n```'
		embed = discord.Embed(title=f'Ranklist for {contest_id}',description=ranklist,color=discord_commons.getRandomColour())
		await ctx.send(embed=embed)



	
	

	@ranklist.error
	async def ranklist_error(self,ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f'```This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds```')
			
def setup(client):
	client.add_cog(Ranklist(client))