import discord
from discord.ext import commands
from .Utils import database,cc_commons, discord_commons,constants,table
import asyncio
import random
from discord.utils import get
import os
import time



class Users(commands.Cog):
	"""docstring for Users"""
	def __init__(self, client):
		self.client = client
		self.db = database.DB()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Users is online")

	@commands.group(brief='Commands related to users',invoke_without_command=True)
	async def handle(self, ctx):
		"""Commands related to handles"""
		await ctx.send_help('handle')



	## Identify users based on Hash Value checking
	@handle.command(brief='Identify yourself')
	async def identify(self,ctx,username=None):
		"""Identify a user"""

		if username==None:
			await ctx.send('```Enter a username, e.g  " =handle identify s59_60r " ```')
			return 
		guild_id = str(ctx.message.guild.id)
		user_id = str(ctx.author.id)

		current_user_data = self.db.get_user_to_guild(user_id,guild_id)
		if current_user_data == None:
			hashVal = discord_commons.getUserNameHash()
			await ctx.send(f"`Identifying {username}`.\n```md\nSet your Codechef Name to '{hashVal}' in 60 Seconds.```")
			if constants.DEBUG == False:
				await asyncio.sleep(constants.HANDLE_VERTIFICATION_TIME)
			else:
				await asyncio.sleep(15)
			data = cc_commons.getUserData(username)
			if data['status'] == True:
				if constants.DEBUG or data['name'] == hashVal:
					await self.identify_user(ctx,user_id,guild_id,username,data)
				else:
					await ctx.send(f"```Hash not matched !\nExpected: {hashVal}\nFound: {data['name']}```")
			else:
				ctx.send("```Please check the username or Try again !```")
		else:
			await ctx.send(f"```Your handle is already set to @{current_user_data['cchandle']}\nRequest an Admin to change it!```")
	




	## Identify users manually
	@handle.command(brief='Identify someone')
	@commands.has_role('Admin')
	async def set(self,ctx,userid=None,username=None):
		"""Identify a user manually"""
		if username==None or userid==None:
			await ctx.send('```Mention user followed by their handle, e.g  " =handle set @user s59_60r " ```')
			return 
		guild_id = str(ctx.message.guild.id)
		user_id = str(userid[3:-1])
		current_user_data = self.db.get_user_to_guild(user_id,guild_id)
		if current_user_data != None:
			await self.remove(ctx,userid)
		data = cc_commons.getUserData(username)
		if data['status'] == True:
			await self.identify_user(ctx,user_id,guild_id,username,data)			
		else:
			ctx.send("```Please check the username or Try again !```")



	## Remove a user from bot's database for the guild
	@handle.command(brief='Remove a user')
	@commands.has_role('Admin')
	async def remove(self,ctx,userid):
		"""Remove a user"""

		if userid==None:
			await ctx.send('```Mention a User, e.g  " =handle remove @user " ```')
			return 

		guild_id = str(ctx.message.guild.id)
		user_id = str(userid[3:-1])
		
		current_user_data = self.db.get_user_to_guild(user_id,guild_id)
		if current_user_data == None:
			await ctx.send(f"<@{user_id}> `has not been identified yet.`")
		else:
			self.db.remove_user_to_guild(user_id, guild_id)
			server = self.client.get_guild(int(guild_id))
			member = server.get_member(int(user_id))
			await self.clean_star_roles(member,server)
			await ctx.send(f"<@{user_id}> `has been removed.`")




	## Remove any kind of star roles
	async def clean_star_roles(self,member,server):
		roles = member.roles
		for r in roles:
			role = get(server.roles, name=r.name)
			if str(role).find("★")!=-1:
				await member.remove_roles(role)



	## Set a star role for a user
	async def set_star(self,member,server,rating):
		role = get(server.roles, name=discord_commons.getStars(rating))
		await member.add_roles(role)


	## Make an embed message for a indentified user
	def make_handle_embed(self,member,username,data):
		desc = f"**Handle for <@{member.id}> succesfully set to [{username}](https://www.codechef.com/users/{username})**"
		colour = discord_commons.getDiscordColourByRating(int(data['rating']))
		embed = discord.Embed(description=desc, color=colour)
		embed.add_field(name='Rating', value=data['rating'], inline=True)
		embed.add_field(name='Stars', value=discord_commons.getStars(data['rating']), inline=True)
		embed.set_thumbnail(url=data['profile_pic'])
		return embed


	## Add an identified user to database and send out embed confirmation
	async def identify_user(self,ctx,user_id,guild_id,username,data=None):
		if data == None:
			data = cc_commons.getUserData(username)
		self.db.add_user_to_guild(user_id, guild_id, username)
		if self.db.fetch_cc_user(username)==None:
			cc_commons.add_cc_user_easy(username, data, self.db)
		else:
			cc_commons.update_cc_user_easy(username, data, self.db)
		server = self.client.get_guild(int(guild_id))
		member = server.get_member(int(user_id))
		await self.clean_star_roles(member,server)
		await self.set_star(member,server,data['rating'])
		profile_embed= self.make_handle_embed(member,username,data)
		await ctx.send(embed=profile_embed)
		



	## List all users of a server
	@handle.command(brief='Check users in server')
	async def list(self,ctx):
		"""Check Users in Server'"""
		res = self.db.fetch_guild_users(str(ctx.message.guild.id))
		if res==None:
			await ctx.send("```No user has registered their handle```")
			return 

		print("res",res)
		res2 = []
		for x in res:
			try:
				res2.append([x,self.db.fetch_cc_user(x['cchandle'])['rating'],ctx.guild.get_member(int(x['user_id']))])
			except Exception as e:
				print(e)
				print(x)
		print("res2",res2)
		res=res2
		res= sorted(res, key = lambda x: x[1], reverse=True)

		style = table.Style('{:>}  {:<}  {:<}  {:<}  {:<}')
		t = table.Table(style)
		t += table.Header('#', 'Name', 'Handle', 'Rating','Stars')
		t += table.Line()
		idx=1
		for x in res:
			try:
				if(x[2]==None):
					continue
				if x[2].nick!=None:
					t += table.Data(idx, x[2].nick, x[0]['cchandle'], x[1],discord_commons.getStars(x[1]))
				else:
					t += table.Data(idx, x[2].name, x[0]['cchandle'], x[1],discord_commons.getStars(x[1]))
				idx+=1
			except Exception as e:
				print(e," at handle list")
			
		handle_list = '```\n'+str(t)+'\n```'
		embed = discord.Embed(title='Handles of server members',description=handle_list,color=discord_commons.getRandomColour())
		await ctx.send(embed=embed)




	## Role update
	
	@handle.command(brief='Check users in server')
	async def role_update(self,ctx):
		if str(ctx.author.id) != str(constants.OWNER):
			await ctx.send(constants.NON_OWNER_MSG)
			return 
		res = self.db.fetch_distinct_active_handles()
		if res==None:
			await ctx.send("```No users for role update```")
			return 
		current_time = int(time.time())
		for username in res:
			current_user_data = self.db.fetch_cc_user(username)
			expiry_time = int(current_user_data['lastupdated'])+constants.USERDATA_UPDATE_COOLDOWN
			if current_time > expiry_time:
				current_user_data = cc_commons.getUserData(username)
				self.db.update_cc_user(username, current_user_data['name'], current_user_data['profile_pic'], current_user_data['rating'], current_user_data['rating_data'],current_user_data['solved_problems'],current_user_data['submission_stats'])								
			else:
				print(f"Skipping {username}")
		res = self.db.fetch_active_handles()
		for x in res:
			guild_id = x['guild_id']
			user_id = x['user_id']
			username = x['username']
			rating = self.db.fetch_cc_user(username)['rating']
			server = self.client.get_guild(int(guild_id))
			member = server.get_member(int(user_id))
			await self.clean_star_roles(member,server)
			await self.set_star(member,server,rating)

		
def setup(client):
	client.add_cog(Users(client))