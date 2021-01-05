import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
import Utils.rating_graph



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
			discord_graph_file = Utils.rating_graph.getRatingGraph(username)
			colour = random.choice([discord.Colour.purple(),discord.Colour.green(),discord.Colour.blue(),discord.Colour.orange()])
			embed = discord.Embed(title='Rating graph on Codechef')
			embed.set_image(url=f'attachment://{discord_graph_file.filename}')
			embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed,file=discord_graph_file)	
def setup(client):
	client.add_cog(Plot(client))