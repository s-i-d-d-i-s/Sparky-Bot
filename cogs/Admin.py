import discord
from discord.ext import commands
from .Utils import database,cc_commons,cc_api
import asyncio
import random
from discord.utils import get
import os
import pickle
from .Utils import constants
import json,requests
import io


class Admin(commands.Cog):
	"""docstring for Admin"""
	def __init__(self, client):
		self.client = client
		self.db = database.DB()
		self.cc_api = cc_api.CodechefAPI(self.db)

	@commands.Cog.listener()
	async def on_ready(self):
		print("Admin is online")

	@commands.group(brief='Commands related to Admin',invoke_without_command=True)
	async def admin(self, ctx):
		"""Commands related to handles"""
		await ctx.send_help('admin')


	@admin.command(brief='Display handle data')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def get_handle_data(self,ctx,username):
		"""Display handle data"""
		data = self.db.fetch_cc_user(username)
		print(data)
		if(len(str(data))<1990):
			await ctx.send(f"```{str(data)}```")
		else:
			await ctx.send(f"```Data length too big```")
		
		
	@admin.command(brief='Update Handle Data')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def update_handle_data(self,ctx,username):
		"""Update Handle Data"""
		data = cc_commons.getUserData(username)
		if data['status']:
			self.db.update_cc_user(username, data['name'], data['profile_pic'], data['rating'], data['rating_data'])
			await ctx.send("```User Data Updated.```")
		else:
			await ctx.send("```Please check the username or try again later```")
			
	@admin.command(brief='Kills Sparky')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def kill(self,ctx):
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			await ctx.send('```Killing Sparky...```')
			os._exit(0)

	@admin.command(brief='Update Presence')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def upd_status(self,ctx):
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			cnt = 0
			for g in self.client.guilds:
				cnt += len(g.members)
			await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{cnt} members and {len(self.client.guilds)} servers !"))

	@commands.command(brief='Sparky Version')
	async def version(self,ctx):		
		desc = "**Sparky Version: {} | Created by [s59_60r](https://www.codechef.com/users/s59_60r)**".format(constants.VERSION)
		embed = discord.Embed(description=desc, color=discord.Colour.red())
		embed.add_field(name='Github', value=f"[Project]({constants.GITHUB})", inline=True)
		embed.set_thumbnail(url=constants.BOTIMAGE)
		embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@admin.command(brief='Where is Sparky?')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def where(self,ctx):
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			res = ""
			for g in self.client.guilds:
				cur = f"Name :{g.name}\nServerID:{g.id}\n"
				res +=cur
				res += "\n"
			await ctx.send(f'```{res}```')

	@admin.command(brief='Leave A Server')
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def leave(self,ctx,server_id=None):
		"""
			=leave [server_id]
		"""
		if server_id==None:
			await ctx.send("```Give a Server ID```")
			return
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			try:
				toleave = self.client.get_guild(int(server_id))
				await toleave.leave()
				await ctx.send(f'```Server {toleave.name} left !```')
			except Exception as e:
				await ctx.send(f'```{e}```')

	@admin.command(brief='Refresh API Tokens')
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def refresh_tokens(self,ctx):
		"""
			=refresh_tokens [server_id]
		"""
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			try:
				data = self.cc_api.getAccessToken()
				self.db.update_api_data(data['access_token'],data['expires_after'])
			except Exception as e:
				await ctx.send(f'```{e}```')


	@admin.command(brief='Load data from database')
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def db_load(self,ctx,url=None):
		"""
			=db_load [url]
		"""
		if url == None:
			await ctx.send("```Enter DB Dump\'s URL ```")
			return 
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			data = json.loads(requests.get(url).content)
			self.db.drop_tables()
			self.db.create_tables()
			try:
				data = json.loads(requests.get(url).content)
				done = set()
				msg = await ctx.send("```Filling in Database```")
				idx=1
				total=len(data['users'])
				for x in data['users']:
					userid = x[1]
					guildid = x[2]
					handle = x[3]
					if handle!="NULL":
						try:
							self.db.add_user_to_guild(userid, guildid, handle)
							cc_commons.getUserData_easy(handle,self.db)
							print(userid,guildid,handle)
						except Exception as e:
							await ctx.send(f"Error with user {handle}")
					await msg.edit(content=f"```{idx}/{total}```")
					idx+=1
			except Exception as e:
				await ctx.send(f'```{e}```')
	

	@admin.command(brief='Dump data from database')
	@commands.has_role('Developer')
	@commands.has_role('Admin')
	async def db_dump(self,ctx):
		"""
			=db_load [url]
		"""
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
		else:
			data = self.db.data_dump()
			res = []
			for x in data:
				res.append([x[0],x[1],x[2]])
			filename = os.path.join(constants.TEMP_DIR, 'db_dump.json')
			with open(filename,'w') as f:
				f.write(json.dumps(res))
			with open(filename, 'rb') as file:
				discord_file = discord.File(io.BytesIO(file.read()), filename='db_dump.json')
			await ctx.send(file=discord_file)

def setup(client):
	client.add_cog(Admin(client))