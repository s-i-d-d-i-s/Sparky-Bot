import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
from .Utils import rating_graph,cc_commons

class Plot(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Plot is online")

	@commands.command(brief='Display rating graph of a user')
	async def rating(self,ctx,username=None):
		"""Display recent solves by a user"""
		if username==None:
			await ctx.send("```Enter the handle !```")
		else:
			if cc_commons.isUserRated(username):
				try:
					discord_graph_file = rating_graph.getRatingGraph(username)
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
	client.add_cog(Plot(client))