import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import os
from Utils.constants import VERSION,GITHUB,YOURCF,YOURCC,YOURATC,BOTIMAGE


class Information(commands.Cog):
	"""docstring for Identification"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Information is online")

	@commands.command(brief='Kills Sparky')
	@commands.has_role('Admin')
	async def kill(self,ctx):
		await ctx.send('Killing Sparky...')
		os._exit(0)

	@commands.command(brief='Sparky Version')
	async def version(self,ctx):
		desc = "**Sparky Version: {} | Created by [s59_60r](https://www.codechef.com/users/s59_60r)**".format(VERSION)
		embed = discord.Embed(description=desc, color=discord.Colour.red())
		embed.add_field(name='Github', value=f"[Project]({GITHUB})", inline=True)
		embed.set_thumbnail(url=BOTIMAGE)
		
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Information(client))