import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
import time
from .Utils import rating_graph,cc_commons,user,cc_api

class Graphs(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.dataset = json.loads(open('Data/dataset.json').read())
		self.dataset2 = {}
		self.apiObj = cc_api.CodechefAPI()
		for y in self.dataset:
			for x in self.dataset[y]:
				self.dataset2[(x['problemCode'])]=y

	@commands.group(brief='Graphs for analyzing Codechef activity',invoke_without_command=True)
	async def plot(self, ctx):
		"""Plot various graphs."""
		await ctx.send_help('plot')
		
	@commands.Cog.listener()
	async def on_ready(self):
		print("Plot is online")

	@plot.command(brief='Display rating graph of a user', usage='[+peak]')
	async def rating(self,ctx, *args: str):
		""" Display rating graph of a user
			Filters = [+peak]
		"""
		handles = []
		peak = False
		
		for x in args:
			if x == "+peak":
				peak=True
			else:
				try:
					if cc_commons.isUserRated(x,self.apiObj) == True:
						handles.append(x)
				except:
					pass

		if len(handles) > 3:
			await ctx.send("```Enter at max 3 handles```")
			return 
		if len(handles)==0:
			username = cc_commons.get_user_by_discord_id(ctx.author.id,ctx.message.guild.id,self.apiObj.db)
			if username!=None:
				handles.append(username)
		if len(handles)==0:
			await ctx.send("```No Rated Handles Given```")
		else:
			try:
				cur_time = int(time.time())
				discord_graph_file=""
				rating_data = ""
				if peak == False:
					rating_data = rating_graph.getRatingGraph(handles,self.apiObj)
				else:
					rating_data = rating_graph.getPeakRatingGraph(handles,self.apiObj)

				discord_graph_file = rating_data
				username = ""
				for x in handles:
					username+=f"[{x}](https://www.codechef.com/users/{x}), "
				username=username[:-2]
				colour = cc_commons.getRandomColour()
				embed = discord.Embed(description=f'**Rating graph of {username}**',colour=colour)
				embed.set_image(url=f'attachment://{discord_graph_file.filename}')
				embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed,file=discord_graph_file)	
			except Exception as e:
				print(e)
				await ctx.send("```Unable to Plot, check username or try again later!```")	
			
	@plot.command(brief='Display histogram of problem sovled', usage='[+noob,+easy,+hard,+medium,+extcont,+challenge]')
	async def solved(self,ctx, *args: str):
		"""Display histogram of problem sovled
		   Filters = [+noob,+easy,+hard,+medium,+extcont,+challenge]
		"""
		handles = []
		filters = False
		noob,easy,med,hard,ext,chalen = False,False,False,False,False,False

		for x in args:
			if x == "+noob":
				filters=True
				noob=True
			elif x == "+easy":
				filters=True
				easy=True
			elif x == "+medium":
				filters=True
				med=True
			elif x == "+hard":
				filters=True
				hard=True
			elif x == "+challenge":
				filters=True
				chalen=True
			elif x == "+extcont":
				filters=True
				ext=True
			else:
				if cc_commons.valid_username(x):
					handles.append(x)

		if filters == True:
			filters = {'noob':noob,'easy':easy,'medium':med,'hard':hard,'challenge':chalen,'extcontest':ext}
		else:
			filters = None

		if len(handles) > 3:
			await ctx.send("```Enter at max 3 handles```")
			return 
		if len(handles)==0:
			username = cc_commons.get_user_by_discord_id(ctx.author.id,ctx.message.guild.id,self.apiObj.db)
			if username!=None:
				handles.append(username)
				
		if len(handles)==0:
			await ctx.send("```No Valid Handles Given```")
		else:
			data = []
			for x in handles:
				cur = []
				error = False
				solvedCodes = {}
				try:
					solvedCodes = user.getSolvedCodes(x,self.apiObj)
				except Exception as e:
					await ctx.send(str(e))
					error=True
				
				if error:
					continue
				for y in solvedCodes:
					try:
						if filters!=None:
							if filters[self.dataset2[y]] == True:
								cur.append(self.dataset2[y].capitalize())
						else:
							cur.append(self.dataset2[y].capitalize())
					except:
						pass
				data.append(cur)

			discord_graph_file = rating_graph.getSolvedHistogram(handles,data)

			username = ""
			for x in handles:
				username+=f"[{x}](https://www.codechef.com/users/{x}), "
			username=username[:-2]
			colour = cc_commons.getRandomColour()
			embed = discord.Embed(description=f'**Histogram of {username}**',colour=colour)
			embed.set_image(url=f'attachment://{discord_graph_file.filename}')
			embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed,file=discord_graph_file)	



def setup(client):
	client.add_cog(Graphs(client))