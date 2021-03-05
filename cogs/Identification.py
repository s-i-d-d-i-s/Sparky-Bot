import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import random
from .Utils import user, constants, cc_commons, cc_api, rating_graph,database,table
VERTIFICATION_TIME = 60



class Identification(commands.Cog):
	"""docstring for Identification"""
	def __init__(self, client):
		self.client = client
		self.apiObj = cc_api.CodechefAPI()
		self.db = database.DB()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Identification is online")


	@commands.group(brief='Commands related to handles',invoke_without_command=True)
	async def handle(self, ctx):
		"""Commands related to handles"""
		await ctx.send_help('handle')

	@handle.command(brief='Check users in server')
	async def list(self,ctx,handle=None):
		"""Check Users in Server'"""
		res = self.db.fetch_guild_users(str(ctx.message.guild.id))
		users = []
		for r in res:
			if r[3]!='NULL':
				users.append([ctx.guild.get_member(int(r[1])), r[3], r[4]])
		if len(users)==0:
			await ctx.send("```No user has registered their handle```")
			return 
		users= sorted(users, key = lambda x: x[2], reverse=True)

		style = table.Style('{:>}  {:<}  {:<}  {:<}  {:<}')
		t = table.Table(style)
		t += table.Header('#', 'Name', 'Handle', 'Rating','Stars')
		t += table.Line()
		idx=1
		for x in users:
			try:
				if(x[0]==None):
					continue
				if x[0].nick!=None:
					t += table.Data(idx, x[0].nick, x[1], x[2],cc_commons.getStars(x[2]))
				else:
					t += table.Data(idx, x[0].name, x[1], x[2],cc_commons.getStars(x[2]))
				idx+=1
			except Exception as e:
				print(e," at handle list")
			
		handle_list = '```\n'+str(t)+'\n```'
		embed = discord.Embed(title='Handles of server members',description=handle_list,color=cc_commons.getRandomColour())
		await ctx.send(embed=embed)

	@handle.command(brief='Identify users')
	async def identify(self,ctx,handle=None):
		"""Indentify users by their Codechef handles"""
		server = ctx.message.guild
		member = server.get_member(ctx.author.id)
		old_user_data = self.db.fetch_user_data(str(ctx.author.id),str(server.id))
		if len(old_user_data)>0 and old_user_data[0][3]!='NULL':
			await ctx.send(f"```Your handle is already set to {old_user_data[0][3]}\nRequest an Admin to change it!```")
			return
	
		if handle==None:
			await ctx.send("```You need to provide your handle !```")
		else:
			hashString = user.getUserNameHash()
			await ctx.send(f"`Indentifying {handle}`.\n```md\nSet your Codechef Name to '{hashString}' in 60 Seconds.```")	
			if constants.DEBUG == '1':
				await asyncio.sleep(5)
			else:
				await asyncio.sleep(VERTIFICATION_TIME)
			try:
				user_data = user.fetchUserData(handle,self.apiObj)
				if user_data['status']==1:
					await ctx.send(f"```Handle not set!```")	
				else:
					if constants.DEBUG == '1' or user_data['name'].strip() == hashString:
						old_user_data = self.db.fetch_user_data(str(ctx.author.id),str(server.id))
						if len(old_user_data)>0:
							self.db.update_user_data(str(ctx.author.id),str(server.id),str(handle),int(user_data['rating']))
						else:
							self.db.add_user_data(str(ctx.author.id),str(server.id),str(handle),int(user_data['rating']))
						roles = member.roles
						for r in roles:
							role = get(server.roles, name=r.name)
							if str(role).find("★")!=-1:
								await member.remove_roles(role)	
						role = get(server.roles, name=user_data['stars'].strip())
						await member.add_roles(role)
						desc = "**Handle for <@{}> succesfully set to [{}](https://www.codechef.com/users/{})**".format(member.id,handle,handle)
						discord_graph_file = rating_graph.getRatingGraph([handle],self.apiObj)
						colour = cc_commons.getDiscordColourByRating(user_data['rating'])
						embed = discord.Embed(description=desc, color=colour)
						embed.add_field(name='Rating', value=user_data['rating'], inline=True)
						embed.add_field(name='Stars', value=user_data['stars'], inline=True)
						embed.add_field(name = chr(173), value = chr(173),inline=False)
						embed.add_field(name='CookOff', value=user_data['short_rating'], inline=True)
						embed.add_field(name='Lunchtime', value=user_data['ltime_rating'], inline=True)
						embed.set_image(url=f'attachment://{discord_graph_file.filename}')
						embed.set_thumbnail(url=user_data['profilePicture'])
						await ctx.send(embed=embed,file=discord_graph_file)	
					else:
						await ctx.send("```Handle not set ! Hash Not Matched ! Try again.```")
			except Exception as e:
				print(e)
				await ctx.send("```Handle not set ! Try again.```")


	@handle.command(brief='Set an handle')
	@commands.has_role('Admin')
	async def set(self,ctx,discord_user=None,handle=None):
		"""Set Codechef handles
		   =handle set @discord_user handle
		"""
		server = ctx.message.guild
		if handle==None:
			await ctx.send("```You need to provide a Codechef handle !```")
		elif discord_user==None:
			await ctx.send("```You need to provide a Dicord Username !```")
		else:
			user_discordid = discord_user[3:-1]
			member = server.get_member(int(user_discordid))
			try:
				user_data = user.fetchUserData(handle,self.apiObj)
				if user_data['status']==1:
					await ctx.send(f"```Handle not set!```")	
				else:
					old_user_data = self.db.fetch_user_data(str(user_discordid),str(server.id))
					if len(old_user_data)>0:
						self.db.update_user_data(str(user_discordid),str(server.id),str(handle),int(user_data['rating']))
					else:
						self.db.add_user_data(str(user_discordid),str(server.id),str(handle),int(user_data['rating']))
					roles = member.roles
					for r in roles:
						role = get(server.roles, name=r.name)
						if str(role).find("★")!=-1:
							await member.remove_roles(role)	
					role = get(server.roles, name=user_data['stars'].strip())
					await member.add_roles(role)
					desc = "**Handle for <@{}> succesfully set to [{}](https://www.codechef.com/users/{})**".format(member.id,handle,handle)
					discord_graph_file = rating_graph.getRatingGraph([handle],self.apiObj)
					colour = cc_commons.getDiscordColourByRating(user_data['rating'])
					embed = discord.Embed(description=desc, color=colour)
					embed.add_field(name='Rating', value=user_data['rating'], inline=True)
					embed.add_field(name='Stars', value=user_data['stars'], inline=True)
					embed.add_field(name = chr(173), value = chr(173),inline=False)
					embed.add_field(name='CookOff', value=user_data['short_rating'], inline=True)
					embed.add_field(name='Lunchtime', value=user_data['ltime_rating'], inline=True)
					embed.set_image(url=f'attachment://{discord_graph_file.filename}')
					embed.set_thumbnail(url=user_data['profilePicture'])
					await ctx.send(embed=embed,file=discord_graph_file)	
			except Exception as e:
				print(e)
				await ctx.send("```Handle not set ! Try again.```")

	@handle.command(brief='Set an handle by userid')
	@commands.has_role('Admin')
	@commands.has_role('Developer')
	async def set_by_id(self,ctx,user_discordid=None,handle=None):
		"""Set Codechef handles
		   =handle set discord_user_id handle
		"""
		server = ctx.message.guild
		if handle==None:
			await ctx.send("```You need to provide a Codechef handle !```")
		elif user_discordid==None:
			await ctx.send("```You need to provide a Dicord userid !```")
		else:
			member = server.get_member(int(user_discordid))
			try:
				user_data = user.fetchUserData(handle,self.apiObj)
				if user_data['status']==1:
					await ctx.send(f"```Handle not set!```")	
				else:
					old_user_data = self.db.fetch_user_data(str(user_discordid),str(server.id))
					if len(old_user_data)>0:
						self.db.update_user_data(str(user_discordid),str(server.id),str(handle),int(user_data['rating']))
					else:
						self.db.add_user_data(str(user_discordid),str(server.id),str(handle),int(user_data['rating']))
					roles = member.roles
					for r in roles:
						role = get(server.roles, name=r.name)
						if str(role).find("★")!=-1:
							await member.remove_roles(role)	
					role = get(server.roles, name=user_data['stars'].strip())
					await member.add_roles(role)
					desc = "**Handle for <@{}> succesfully set to [{}](https://www.codechef.com/users/{})**".format(member.id,handle,handle)
					discord_graph_file = rating_graph.getRatingGraph([handle],self.apiObj)
					colour = cc_commons.getDiscordColourByRating(user_data['rating'])
					embed = discord.Embed(description=desc, color=colour)
					embed.add_field(name='Rating', value=user_data['rating'], inline=True)
					embed.add_field(name='Stars', value=user_data['stars'], inline=True)
					embed.add_field(name = chr(173), value = chr(173),inline=False)
					embed.add_field(name='CookOff', value=user_data['short_rating'], inline=True)
					embed.add_field(name='Lunchtime', value=user_data['ltime_rating'], inline=True)
					embed.set_image(url=f'attachment://{discord_graph_file.filename}')
					embed.set_thumbnail(url=user_data['profilePicture'])
					await ctx.send(embed=embed,file=discord_graph_file)	
			except Exception as e:
				print(e)
				await ctx.send("```Handle not set ! Try again.```")

	@handle.command(brief='Remove an handle')
	@commands.has_role('Admin')
	async def remove(self,ctx,discord_user=None):
		"""Removes Codechef handles
		   =handle remove @discord_user 
		"""
		server = ctx.message.guild
		if discord_user==None:
			await ctx.send("```You need to provide a Dicord Username @<user>!```")
		else:
			user_discordid = discord_user[3:-1]
			member = server.get_member(int(user_discordid))
			try:				
				old_user_data = self.db.fetch_user_data(str(user_discordid),str(server.id))
				print(old_user_data)
				if len(old_user_data)>0 and old_user_data[0][3]!='NULL':
					self.db.update_user_data(str(user_discordid),str(server.id),"NULL",0)
				
				roles = member.roles
				for r in roles:
					role = get(server.roles, name=r.name)
					if str(role).find("★")!=-1:
						await member.remove_roles(role)	
				await ctx.send("```Handle removed!```")
			except Exception as e:
				print(e)
				await ctx.send("```Some Error Occured ! Try again.```")
	
	@handle.command(brief='Reverse look a user')
	async def rget(self,ctx,discord_user=None):
		user_discordid = discord_user[3:-1]
		username = cc_commons.get_user_by_discord_id(user_discordid,ctx.message.guild.id,self.apiObj.db)
		if username == None:
			print("```User not registered```")
			return 
		try:
			data = self.apiObj.getUserData(username)
			rating = data['data']['content']['ratings']['allContest']
			stars = user.rating_to_stars(rating)
			image = data['profile_image']
			desc = "**Handle for <@{}> succesfully set to [{}](https://www.codechef.com/users/{})**".format(user_discordid,username,username)
			colour = cc_commons.getDiscordColourByRating(rating)
			embed = discord.Embed(description=desc, color=colour)
			embed.add_field(name='Rating', value=rating, inline=True)
			embed.add_field(name='Stars', value=stars, inline=True)
			embed.set_thumbnail(url=image)
			await ctx.send(embed=embed)
		except Exception as e:
			print(e," at rget")
	
	@handle.command(brief='Role Update')
	@commands.has_role('Admin')
	async def role_update(self,ctx):
		await ctx.send("```Under Construction ... ```")
def setup(client):
	client.add_cog(Identification(client))