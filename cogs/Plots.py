import discord
from discord.ext import commands
from .Utils import contests,database,rating_graph,discord_commons,cc_commons
import asyncio
import random
from discord.utils import get
import os,json
import pickle



class Plots(commands.Cog):
	"""docstring for Plots"""
	def __init__(self, client):
		self.client = client
		self.db = database.DB()
		self.dataset = json.loads(open('Data/dataset.json').read())
		self.dataset2 = {}
		for y in self.dataset:
			for x in self.dataset[y]:
				self.dataset2[(x['problemCode'])]=y

	@commands.Cog.listener()
	async def on_ready(self):
		print("Plots is online")

	@commands.group(brief='Commands related to plots',invoke_without_command=True)
	async def plot(self, ctx):
		"""Commands related to handles"""
		await ctx.send_help('plot')

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
				if cc_commons.isUserRated(x) == True:
					handles.append(x)
				
		if len(handles) > 3:
			await ctx.send("```Enter at max 3 handles```")
			return 
		if len(args)==0:
			username = self.db.get_user_by_discord_id(ctx.author.id,ctx.message.guild.id)
			if username!=None:
				handles.append(username)
			
		if len(handles)==0:
			await ctx.send("```No Rated Handles Given```")
		else:
			try:
				discord_graph_file=""
				if peak == False:
					discord_graph_file = rating_graph.getRatingGraph(handles,self.db)
				else:
					discord_graph_file = rating_graph.getPeakRatingGraph(handles,self.db)
				username = ""
				for x in handles:
					username+=f"[{x}](https://www.codechef.com/users/{x}), "
				username=username[:-2]
				colour = discord_commons.getRandomColour()
				embed = discord.Embed(description=f'**Rating graph of {username}**',colour=colour)
				embed.set_image(url=f'attachment://{discord_graph_file.filename}')
				embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed,file=discord_graph_file)	
			except Exception as e:
				print("Error at =rating",e)
				import traceback
				traceback.print_exc()
				await ctx.send("```Unable to Plot, check username or try again later!```")	


	@plot.command(brief='Display histogram of problem solved', usage='[+noob,+easy,+hard,+medium,+extcont,+challenge]')
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
		if len(args)==0:
			username = self.db.get_user_by_discord_id(ctx.author.id,ctx.message.guild.id)
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
					solvedCodes = rating_graph.getSolvedCodes(x,self.db)
				except Exception as e:
					print("Error in =plot solved",e)
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
			colour = discord_commons.getRandomColour()
			embed = discord.Embed(description=f'**Histogram of {username}**',colour=colour)
			embed.set_image(url=f'attachment://{discord_graph_file.filename}')
			embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed,file=discord_graph_file)	

def setup(client):
	client.add_cog(Plots(client))