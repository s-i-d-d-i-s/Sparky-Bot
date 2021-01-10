import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
import re
from .Utils import cc_commons, user

class Features(commands.Cog):
	"""docstring for Features"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Features is online")
	
	@commands.command(brief='Display recent solves by a user')
	async def stalk(self,ctx,username=None):
		"""Display recent solves by a user"""
		if username==None:
			await ctx.send("```Enter the handle !```")
		else:
			try:
				colour = cc_commons.getRandomColour()
				embed = discord.Embed(description="**These are the recent submissions from [{}](https://codechef.com/users/{}).**".format(username,username),color=colour)
				data =  user.getSubmission(username)
				for d in data:
					embed.add_field(name=f'{d[0]}', value=d[1], inline=False)
				embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
			except Exception as e:
				print(e)
				await ctx.send("Please try again !")

def setup(client):
	client.add_cog(Features(client))