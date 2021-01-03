import discord
from discord.ext import commands
import asyncio
from Utils.database import db, User
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

	@commands.command(brief='Prints Database in SSV')
	@commands.has_role('Admin')
	async def getDB(self,ctx):
		data = User.select()
		res = "```"
		for d in data.tuples().iterator():
			temp = str(d)
			temp = temp[1:-1].replace('\'','')
			temp = temp.replace(' ','')
			res += temp
			res += "**"
		res += "```"
		await ctx.send(res)

	@commands.command(brief='Sets Database from CSV')
	@commands.has_role('Admin')
	async def setDB(self,ctx,data=None):
		if data == None:
			return 
		data = data.split("**")
		data = data[:-1]
		for d in data:
			cur_data = d.split(',')
			cur_usern = User(username=str(cur_data[1]),discordid=int(cur_data[2]),rating=int(cur_data[3]),guild=int(cur_data[4]))
			cur_usern.save()
		await ctx.send("```Database Updated```")

	@commands.command(brief='Sparky Version')
	async def version(self,ctx):
		desc = "**Sparky Version: {} | Created by [s59_60r](https://www.codechef.com/users/s59_60r)**".format(VERSION)
		embed = discord.Embed(description=desc, color=discord.Colour.red())
		embed.add_field(name='Github', value=f"[Project]({GITHUB})", inline=True)
		embed.set_thumbnail(url=BOTIMAGE)
		embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Information(client))