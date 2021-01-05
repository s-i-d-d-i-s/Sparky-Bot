import discord
from discord.ext import commands
import Utils.user
from Utils.database import db, User
import asyncio
from discord.utils import get
import random
from Utils.constants import OWNER,NON_OWNER_MSG

VERTIFICATION_TIME = 60
UPDATE_SLEEP = 2
DEBUG = False

def scale(a,ln):
	a=str(a)
	while(len(a)<ln):
		a=a+" "
	longer = False
	if len(a)>ln:
		longer = True
	while len(a)>ln:
		a = a[:-1]
	if longer:
		a = a[:-3]
		a += "..."
	return a

class Identification(commands.Cog):
	"""docstring for Identification"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Identification is online")

	@commands.command(brief='Check Users in Server')
	async def handles(self,ctx,handle=None):
		"""Check Users in Server'"""
		No=1
		serverid = int(ctx.message.guild.id)
		if handle==None:
			res = "```"
			h1 = scale("Discord User",20)
			h2 = scale("CC Username",15)
			res+=(f"No . {h1}|{h2}|Rating\n\n")
			for cur_user in User.select().where(User.guild == f'{serverid}').order_by(User.rating)[::-1]:
				userno = scale(No,3)
				discorduser = scale(self.client.get_user(int(cur_user.discordid)),20)
				username = scale(cur_user.username,15)
				rating = scale(cur_user.rating,6)
				res+=(f"{userno}. {discorduser}|{username}|{rating}\n")
				No+=1
			res+="```"
			await ctx.send(res)
		else:
			cur_user = User.select().where(User.username == f'{handle}')
			if len(cur_user) >0:
				cur_user = cur_user.get()
				await ctx.send(f"`The handle \"{handle}\" is assigned to `\t<@!{cur_user.discordid}>")
			else:
				await ctx.send(f"`User Not Found !`")
			

	@commands.command(brief='Indentify Users')
	async def identify(self,ctx,handle=None):
		"""Indentify Users by their Codechef handles"""
		serverid = int(ctx.message.guild.id)
		if handle==None:
			await ctx.send("```You need to provide your handle !```")
		else:
			cur_user = User.select().where(User.discordid == ctx.author.id,User.guild == serverid)
			exists = False
			if len(cur_user) >0:
				cur_user = cur_user.get()
				exists = True
				await ctx.send(f"`Handle currently set as : {cur_user.username}\n`")
				await ctx.send(f"```Ask an admin to reset your handle if you wish to change```")
			if exists == False:
				hashString = Utils.user.getUserNameHash()
				await ctx.send(f"`Indentifying {handle}`.\n```md\nSet your Codechef Name to '{hashString}' in 60 Seconds.```")	
				await asyncio.sleep(VERTIFICATION_TIME)
				server = ctx.message.guild
				member = server.get_member(ctx.author.id)
				try:
					data = Utils.user.getUserData(handle,member)
					if data['Status']==1:
						await ctx.send(f"```Handle not set!```")	
					else:
						if DEBUG or data['Name'].strip() == hashString:
							roles = member.roles
							cur_usern = User(username=handle,discordid=ctx.author.id,rating=data['Rating'],guild=serverid)
							cur_usern.save()
							if exists:
								cur_user.delete_instance()
							for r in roles:
								role = get(server.roles, name=r.name)
								if str(role).find("★")!=-1:
									print("Removing Role ",role)
									await member.remove_roles(role)	
							role = get(server.roles, name=data['Stars'].strip())
							await member.add_roles(role)
							await ctx.send(embed=data['embed'])	
						else:
							await ctx.send("```Handle not set ! Hash Not Matched ! Try again.```")
				except:
					await ctx.send("```Handle not set ! Try again.```")


	@commands.command(brief='Reset an handle')
	@commands.has_role('Admin')
	async def reset(self,ctx,handle=None):
		"""Reset Codechef handles"""
		serverid = int(ctx.message.guild.id)
		if handle==None:
			await ctx.send("```You need to provide a Codechef handle !```")
		else:
			cur_user = User.select().where(User.username == f'{handle}',User.guild == serverid)
			exists = True
			if len(cur_user) ==0:
				exists = False
				await ctx.send(f"```Handle not found in the server```")
			else:
				cur_user = cur_user.get()
			if exists == True:
				server = ctx.message.guild
				member = server.get_member(cur_user.discordid)
				roles = member.roles
				for r in roles:
					role = get(server.roles, name=r.name)
					if str(role).find("★")!=-1:
						print("Removing Role ",role)
						await member.remove_roles(role)	
				cur_user.delete_instance()
				await ctx.send(f"```Handle removed !```")




	@commands.command(brief='Set an handle')
	@commands.has_role('Admin')
	async def set(self,ctx,discord_user=None,handle=None):
		"""Set Codechef handles
		   =set @discord_user handle
		"""
		serverid = int(ctx.message.guild.id)
		if handle==None:
			await ctx.send("```You need to provide a Codechef handle !```")
		elif discord_user==None:
			await ctx.send("```You need to provide a Dicord Username !```")
		else:
			try:
				user_discordid = discord_user[3:-1]
				cur_user = User.select().where(User.discordid == user_discordid,User.guild == serverid)
				exists = False
				if len(cur_user) >0:
					cur_user = cur_user.get()
					exists = True
					await ctx.send(f"`Handle currently set as : {cur_user.username}\n`")
					await ctx.send(f"```Reset the handle first if you wish to change```")
				if exists == False:
					server = ctx.message.guild
					member = server.get_member(int(user_discordid))
					try:
						data = Utils.user.getUserData(handle,member)
						if data['Status']==1:
							await ctx.send(f"Handle not set!")	
						else:
							roles = member.roles
							cur_usern = User(username=handle,discordid=user_discordid,rating=data['Rating'],guild=serverid)
							cur_usern.save()
							if exists:
								cur_user.delete_instance()
							for r in roles:
								role = get(server.roles, name=r.name)
								if str(role).find("★")!=-1:
									print("Removing Role ",role)
									await member.remove_roles(role)	
							role = get(server.roles, name=data['Stars'].strip())
							await member.add_roles(role)
							await ctx.send(embed=data['embed'])	
					except:
						await ctx.send("```Handle not set ! Try again.```")
			except:
				await ctx.send("```Handle not set ! Check help for instructions```")

	@commands.command(brief='Set an handle using ID')
	@commands.has_role('Admin')
	async def set_by_id(self,ctx,user_discordid=None,handle=None):
		"""Set Codechef handles by Discord ID
		   =set discord_user_id handle
		"""
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			serverid = int(ctx.message.guild.id)
			if handle==None:
				await ctx.send("```You need to provide a Codechef handle !```")
			elif user_discordid==None:
				await ctx.send("```You need to provide a Dicord Username !```")
			else:
				cur_user = User.select().where(User.discordid == user_discordid,User.guild == serverid)
				exists = False
				if len(cur_user) >0:
					cur_user = cur_user.get()
					exists = True
					await ctx.send(f"`Handle currently set as : {cur_user.username}\n`")
					await ctx.send(f"```Reset the handle first if you wish to change```")
				if exists == False:
					server = ctx.message.guild
					member = server.get_member(int(user_discordid))
					try:
						data = Utils.user.getUserData(handle,member)
						if data['Status']==1:
							await ctx.send(f"Handle not set!")	
						else:
							roles = member.roles
							cur_usern = User(username=handle,discordid=user_discordid,rating=data['Rating'],guild=serverid)
							cur_usern.save()
							if exists:
								cur_user.delete_instance()
							for r in roles:
								role = get(server.roles, name=r.name)
								if str(role).find("★")!=-1:
									print("Removing Role ",role)
									await member.remove_roles(role)	
							role = get(server.roles, name=data['Stars'].strip())
							await member.add_roles(role)
							await ctx.send(embed=data['embed'])	
					except:
						await ctx.send("```Handle not set ! Try again.```")


	@commands.command(brief='Update User Roles')
	@commands.has_role('Admin')
	async def roleupdate(self,ctx):
		"""Update user roles, don't use it too frequently"""
		if str(ctx.author.id) != str(OWNER):
			await ctx.send(NON_OWNER_MSG)
		else:
			await ctx.send("`Please wait while all roles are being updated`")	
			serverid = int(ctx.message.guild.id)
			server_users = User.select().where(User.guild == f'{serverid}')
			res = "```\n"
			try:
				for s in server_users:
					user = s
					cur_data = Utils.user.updateData(user.username)
					oldstar = Utils.user.getStars(user.rating)
					delta = int(cur_data['Rating']) - int(user.rating)
					delta = str(delta)
					if delta[0]!='-':
						delta = "+"+delta
					newstar = cur_data["Stars"]
					updateinfo = f"{user.username} moved from {oldstar} to {newstar}"
					updateinfo = scale(updateinfo,40)
					res += "{}\n".format(f"{updateinfo} | Delta = {delta}")
					user.rating = cur_data['Rating']
					user.save()
					await asyncio.sleep(UPDATE_SLEEP)
				res+="```"
				await ctx.send(res)	
			except:
				await ctx.send("Error While Updating Roles")
		
	
	

def setup(client):
	client.add_cog(Identification(client))