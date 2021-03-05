import discord
from discord.ext import commands
import asyncio
import json,ujson
import requests
import bs4
import random
from discord.utils import find
import re
import time
from .Utils import cc_commons, user, cc_api, constants,table


class Ranklist(commands.Cog):

	dataset = {}
	"""docstring for Features"""
	def __init__(self, client):
		self.client = client
		self.apiObj = cc_api.CodechefAPI()
		self.cooldown = {}

	@commands.Cog.listener()
	async def on_ready(self):
		print("Features is online")
	
	def gen_list_contest(self,contest_name,college_name):
		"""Check Users in Server'"""
		jsondata = self.apiObj.getCollegeRanklistContest(college_name,contest_name)
		if jsondata==None:
			return None,None
		style = table.Style('{:>} {:<} {:<}  {:<}  {:<} ')
		t = table.Table(style)
		t += table.Header('No','Rank', 'Handle', 'Rating','Score')
		t += table.Line()
		idx = 1
		for x in jsondata:
			t += table.Data(idx,x['rank'], x['username'], x['cur_rating'], x['score'])
			idx+=1
		ranklist = '```yaml\n'+str(t)+'\n```'
		embed = discord.Embed(title=f'College Ranklist - {contest_name}',description=ranklist,color=cc_commons.getRandomColour())
		return embed,ranklist

	def gen_list(self,college_name):
		"""Check Users in Server'"""
		jsondata = self.apiObj.getCollegeRanklist(college_name)
		
		if len(jsondata)==0:
			return None
		style = table.Style('{:>}  {:<}  {:<}  {:<}  {:<}')
		t = table.Table(style)
		t += table.Header('#', 'Name', 'Handle', 'Rating','Stars')
		t += table.Line()
		
		for x in jsondata:
			t += table.Data(x['college_rank'], x['name'], x['handle'], x['rating'],cc_commons.getStars(x['rating']))
		ranklist = '```\n'+str(t)+'\n```'
		embed = discord.Embed(title=f'Ranklist of {college_name}',description=ranklist,color=cc_commons.getRandomColour())
		return embed,ranklist

	@commands.command(brief='Add a Organization Ranklist to the Server')
	@commands.has_role('Admin')
	async def add_ranklist(self,ctx,*args: str):
		"""Add a Organization Ranklist to the Server"""
		guild_id = str(ctx.message.guild.id)
		chan_id = str(ctx.message.channel.id)
		collegeName = ' '.join(args)
		print(collegeName)
		## Check for cooldown
		if cc_commons.isCooled(self.cooldown,ctx.author.id) == False:
			await ctx.send(f"```Cool down ! You can make next request in {self.cooldown[str(ctx.author.id)]+constants.RANKLIST_COOLDOWN-int(time.time())} seconds```")
			return
		else:
			self.cooldown[str(ctx.author.id)]=int(time.time())

		
		data = cc_commons.get_ranklist(str(ctx.message.guild.id),self.apiObj.db)
		if len(data) == 0:
			await ctx.send("```Setting up ranklist for "+str(ctx.message.guild.name)+"```")
			data,jsondata = self.gen_list(collegeName)
			if data==None:
				await ctx.send("```Either the college name is wrong or no rated handle exists in the organization```")
				return
			message = await ctx.send(embed=data)
			self.apiObj.db.add_college_data(guild_id,message.id,chan_id,collegeName,jsondata)
		else:
			await ctx.send("```Ranklist for "+str(ctx.message.guild.name)+" already exits, overwriting...```")
			data=data[0]
			last_updated = int(data[6])
			if  (str(ctx.author.id)!=constants.OWNER) and time.time() <= last_updated + constants.RANKLISTLIM:
				await ctx.send("```Ranklist for "+str(ctx.message.guild.name)+" was updated recently, try again after "+str(last_updated + constants.RANKLISTLIM-int(time.time()))+" seconds !```")
				return
			data,jsondata = self.gen_list(collegeName)
			if data==None:
				await ctx.send("```Either the college name is wrong or no rated handle exists in the organization```")
				return
			message = await ctx.send(embed=data)
			self.apiObj.db.update_college_data(guild_id,chan_id,message.id,collegeName,jsondata)

	@commands.command(brief='Update the Organization Ranklist in the Server')	
	@commands.has_role('Admin')
	async def update_ranklist(self,ctx):
		guild_id = str(ctx.message.guild.id)
		chan_id = str(ctx.message.channel.id)
		## Check for cooldown
		if cc_commons.isCooled(self.cooldown,ctx.author.id) == False:
			await ctx.send(f"```Cool down ! You can make next request in {self.cooldown[str(ctx.author.id)]+constants.RANKLIST_COOLDOWN-int(time.time())} seconds```")
			return
		else:
			self.cooldown[str(ctx.author.id)]=int(time.time())
		data = cc_commons.get_ranklist(str(ctx.message.guild.id),self.apiObj.db)
		if len(data) == 0:
			await ctx.send("```No ranklist exist for "+str(ctx.message.guild.name)+"```")
			return
		else:
			data=data[0]
			collegeName=data[4]
			last_updated = int(data[6])
			if (str(ctx.author.id)!=constants.OWNER) and time.time() <= last_updated + constants.RANKLISTLIM:
				await ctx.send("```Ranklist for "+str(ctx.message.guild.name)+" was updated recently, try again after "+str(last_updated + constants.RANKLISTLIM-int(time.time()))+" seconds !```")
				return
			chan_id = int(data[2])
			message_id = int(data[3])
			ranklist_channel = find(lambda x: x.id == chan_id,  ctx.message.guild.text_channels)
			message = await ranklist_channel.fetch_message(message_id)
			data,jsondata = self.gen_list(collegeName)
			if data==None:
				await ctx.send("```Either the college name is wrong or no rated handle exists in the organization```")
				return
			await message.edit(embed=data)
			self.apiObj.db.update_college_data(guild_id,chan_id,message.id,collegeName,jsondata)
	
	@commands.command(brief='Show the Organization Ranklist in the Server')	
	async def org_ratings(self,ctx):
		data = cc_commons.get_ranklist(str(ctx.message.guild.id),self.apiObj.db)
		if len(data) == 0:
			await ctx.send("```No ranklist exist for "+str(ctx.message.guild.name)+"```")
			return
		else:
			data=data[0]
			guild_id = int(data[1])
			chan_id = int(data[2])
			message_id = int(data[3])
			view_link = f"https://discord.com/channels/{guild_id}/{chan_id}/{message_id}"
			embed = discord.Embed(title=f'Ranklist of {data[4]}',description="[Go To Ranklist]({})".format(view_link),color=cc_commons.getRandomColour())
			await ctx.send(embed=embed)

	@commands.command(brief='Show the Ranklist for the Org for a contest')	
	async def org_ranklist(self,ctx,contest_code=None):
		
		if cc_commons.isCooled(self.cooldown,ctx.author.id,1) == False:
			await ctx.send(f"```Cool down ! You can make next request in {self.cooldown[str(ctx.author.id)]+constants.ORG_RANKLIST_COOLDOWN-int(time.time())} seconds```")
			return
		else:
			self.cooldown[str(ctx.author.id)]=int(time.time())

		if contest_code == None:
			await ctx.send("```You Need To Enter A Contest Code```")
			return
		data = cc_commons.get_ranklist(str(ctx.message.guild.id),self.apiObj.db)
		if len(data) == 0:
			await ctx.send("```No organization exist for "+str(ctx.message.guild.name)+"```")
			return
		
		data=data[0]
		org_name = data[4]
		data,jsondata = self.gen_list_contest(contest_code,org_name)
		if data == None:
			await ctx.send(f"```Unable to fetch ranklist for the contest {contest_code}```")
			return
		await ctx.send(embed=data)
		






def setup(client):
	client.add_cog(Ranklist(client))