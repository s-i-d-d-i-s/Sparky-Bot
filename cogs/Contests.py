import discord
from discord.ext import commands
from .Utils import contests
import asyncio
import random
from discord.utils import get
import os
import pickle



class Contests(commands.Cog):
	"""docstring for Contests"""
	def __init__(self, client):
		self.client = client
		self.future_contests = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("Contests is online")

	@commands.command(brief='Display future contests')
	async def future(self,ctx):
		"""Get Upcoming Contests on Codechef"""
		try:
			data = contests.getFutureContest()
			data.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=data)
		except:
			await ctx.send("```API Limit Exhausted !```")



def setup(client):
	client.add_cog(Contests(client))