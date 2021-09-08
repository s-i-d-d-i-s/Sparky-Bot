import discord
from discord.ext import commands
from .Utils import contests,discord_commons
import asyncio
import random
from discord.utils import get
import os
import pickle

COOLDOWN = 5

class Contests(commands.Cog):
	"""docstring for Contests"""
	def __init__(self, client):
		self.client = client
		self.cooldown = {}

	@commands.Cog.listener()
	async def on_ready(self):
		print("Contests is online")

	
	@commands.group(brief='Commands related to contests',invoke_without_command=True)
	
	async def contest(self, ctx):
		"""Commands related to contests"""
		await ctx.send_help('contest')

	
	
			
	@contest.command(brief='Display future contests')
	@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
	async def future(self,ctx):
		"""Get Upcoming Contests on Codechef"""
		try:
			data = contests.getFutureContest()
			data.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=data)
		except:
			await ctx.send("```API Limit Exhausted !```")

	
	
	@contest.command(brief='Display past contests')
	@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
	async def past(self,ctx):
		"""Get Past Contests on Codechef"""
		try:
			data = contests.getPastContest()
			data.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=data)
		except:
			await ctx.send("```API Limit Exhausted !```")

	@contest.command(brief='Display present contests')
	@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
	async def present(self,ctx):
		"""Get Running Contests on Codechef"""
		try:
			data = contests.getPresentContest()
			data.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=data)
		except:
			await ctx.send("```API Limit Exhausted !```")


	@future.error
	@past.error
	@present.error
	async def contest_error(self,ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f'```This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds```')
			
def setup(client):
	client.add_cog(Contests(client))