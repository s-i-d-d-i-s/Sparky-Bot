import discord
from discord.ext import commands
import asyncio
from Utils.database import db, User
from discord.utils import get
import os
from Utils.constants import VERSION,GITHUB,BOTIMAGE,OWNER,NON_OWNER_MSG
from Utils.constants import TEMP_DIR
import time
import requests
class Information(commands.Cog):
	"""docstring for Identification"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Information is online")

	@commands.command(brief='Kills Sparky')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def kill(self,ctx):
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			await ctx.send('```Killing Sparky...```')
			os._exit(0)

	@commands.command(brief='Update Presence')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def upd_status(self,ctx):
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			cnt = 0
			for g in self.client.guilds:
				cnt += len(g.members)
			await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{cnt} members and {len(self.client.guilds)} servers !"))
		

	@commands.command(brief='Where is Sparky?')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def where(self,ctx):
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			res = ""
			for g in self.client.guilds:
				cur = f"Name :{g.name}\nServerID:{g.id}\n"
				res +=cur
				res += "\n"
			
			await ctx.send(f'```{res}```')

	@commands.command(brief='Leave A Server')
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def leave(self,ctx,server_id=None):
		"""
			=leave [server_id]
		"""
		if server_id==None:
			await ctx.send("```Give a Server ID```")
			return
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			try:
				toleave = self.client.get_guild(int(server_id))
				await toleave.leave()
				await ctx.send(f'```Server {toleave.name} left !```')
			except Exception as e:
				await ctx.send(f'```{e}```')

	@commands.command(brief='Prints Database in SSV')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def getDB(self,ctx):
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			data = User.select()
			res=""
			for d in data.tuples().iterator():
				temp = str(d)
				temp = temp[1:-1].replace('\'','')
				temp = temp.replace(' ','')
				res += temp
				res += "|s|"
			res += ""
			filename = os.path.join(TEMP_DIR, f'dbdump_{time.time()}.txt')
			with open(filename, 'w') as file:
				file.write(res)
			
			discord_file = discord.File(filename, filename='dbdump.txt')
			os.remove(filename)
			await ctx.send(file=discord_file)

	@commands.command(brief='Sets Database from SSV')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def setDB(self,ctx,data=None):
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			if data == None:
				return 
			data = requests.get(data).content.decode()
			data = data.split("|s|")
			data = data[:-1]
			logg = ""
			for d in data:
				cur_data = d.split(',')
				cur_usern = User(username=str(cur_data[1]),discordid=int(cur_data[2]),rating=int(cur_data[3]),guild=int(cur_data[4]))
				logg += f"{str(cur_data[1])}, {int(cur_data[2])}, {int(cur_data[3])}, {int(cur_data[4])}"
				logg +="\n"
				cur_usern.save()
			await ctx.send(f"```{logg}```")
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