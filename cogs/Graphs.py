import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
import time
from .Utils import rating_graph,cc_commons

class Graphs(commands.Cog):
	solvedCodes = {}
	lastUpdated = {}
	def __init__(self, client):
		self.client = client
		self.driver = cc_commons.setup_webdriver()

	@commands.group(brief='Graphs for analyzing Codechef activity',invoke_without_command=True)
	async def plot(self, ctx):
		"""Plot various graphs."""
		await ctx.send_help('plot')
		
	@commands.Cog.listener()
	async def on_ready(self):
		print("Plot is online")

	@plot.command(brief='Display rating graph of a user', usage='[+peak]')
	async def rating(self,ctx,username=None,f1=None):
		"""Display rating graph of a user"""
		if username!=None and username.find('+')!=-1:
			await ctx.send("```That's not a valid handle```")
			return
		peak = False
		args =['+peak']
		if f1 not in args and f1!=None:
			await ctx.send("```Some invalid flags were passed, ignoring them..```")

		if f1=='+peak':
			peak=True


		if username==None:
			await ctx.send("```Enter the handle !```")
		else:
			if cc_commons.isUserRated(username):
				try:
					cur_time = int(time.time())
					if username not in self.lastUpdated.keys():
						self.lastUpdated[username]=0
					discord_graph_file=""
					if (cur_time - self.lastUpdated[username] ) > 1800:
						if peak == False:
							rating_data = rating_graph.getRatingGraph(username,self.driver)
							discord_graph_file = rating_data[0]
							self.lastUpdated[username]=cur_time
							self.solvedCodes[username] = rating_data[1]
						else:
							rating_data = rating_graph.getPeakRatingGraph(username,self.driver)
							discord_graph_file = rating_data[0]
							self.lastUpdated[username]=cur_time
							self.solvedCodes[username] = rating_data[1]
					else:
						if peak == False:
							rating_data = rating_graph.getRatingGraph(username,self.driver,self.solvedCodes[username])
							discord_graph_file = rating_data[0]
						else:
							rating_data = rating_graph.getPeakRatingGraph(username,self.driver,self.solvedCodes[username])
							discord_graph_file = rating_data[0]

					colour = cc_commons.getRandomColour()
					embed = discord.Embed(title=f'Rating graph of {username}',colour=colour)
					embed.set_image(url=f'attachment://{discord_graph_file.filename}')
					embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
					await ctx.send(embed=embed,file=discord_graph_file)	
				except Exception as e:
					print(e)
					await ctx.send("```Unable to Plot, check username or try again later!```")	
			else:
				await ctx.send("```User is not rated```")	


def setup(client):
	client.add_cog(Graphs(client))