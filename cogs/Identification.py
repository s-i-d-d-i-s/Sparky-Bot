import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import random
# from .Utils

VERTIFICATION_TIME = 60



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
		await ctx.send(f"```This command has been deactivated, due to current shortage of resources.\nIt will be enabled in future```")

	# @commands.command(brief='Indentify Users')
	# async def identify(self,ctx,handle=None):
	# 	"""Indentify Users by their Codechef handles"""
	# 	serverid = int(ctx.message.guild.id)
	# 	if handle==None:
	# 		await ctx.send("```You need to provide your handle !```")
	# 	else:
	# 		hashString = user.getUserNameHash()
	# 		await ctx.send(f"`Indentifying {handle}`.\n```md\nSet your Codechef Name to '{hashString}' in 60 Seconds.```")	
	# 		await asyncio.sleep(VERTIFICATION_TIME)
	# 		server = ctx.message.guild
	# 		member = server.get_member(ctx.author.id)
	# 		try:
	# 		data = Utils.user.getUserData(handle,member)
	# 		if data['Status']==1:
	# 			await ctx.send(f"```Handle not set!```")	
	# 		else:
	# 			if DEBUG or data['Name'].strip() == hashString:
	# 				roles = member.roles
	# 				cur_usern = User(username=handle,discordid=ctx.author.id,rating=data['Rating'],guild=serverid)
	# 				cur_usern.save()
	# 				if exists:
	# 					cur_user.delete_instance()
	# 				for r in roles:
	# 					role = get(server.roles, name=r.name)
	# 					if str(role).find("★")!=-1:
	# 						print("Removing Role ",role)
	# 						await member.remove_roles(role)	
	# 				role = get(server.roles, name=data['Stars'].strip())
	# 				await member.add_roles(role)
	# 				await ctx.send(embed=data['embed'])	
	# 			else:
	# 				await ctx.send("```Handle not set ! Hash Not Matched ! Try again.```")
	# 	except:
	# 		await ctx.send("```Handle not set ! Try again.```")


	# @commands.command(brief='Set an handle')
	# @commands.has_role('Admin')
	# async def set(self,ctx,discord_user=None,handle=None):
	# 	"""Set Codechef handles
	# 	   =set @discord_user handle
	# 	"""
	# 	serverid = int(ctx.message.guild.id)
	# 	if handle==None:
	# 		await ctx.send("```You need to provide a Codechef handle !```")
	# 	elif discord_user==None:
	# 		await ctx.send("```You need to provide a Dicord Username !```")
	# 	else:
	# 		try:
	# 			user_discordid = discord_user[3:-1]
	# 			cur_user = User.select().where(User.discordid == user_discordid,User.guild == serverid)
	# 			exists = False
	# 			if len(cur_user) >0:
	# 				cur_user = cur_user.get()
	# 				exists = True
	# 				try:
	# 					server = ctx.message.guild
	# 					member = server.get_member(cur_user.discordid)
	# 					roles = member.roles
	# 					for r in roles:
	# 						role = get(server.roles, name=r.name)
	# 						if str(role).find("★")!=-1:
	# 							print("Removing Role ",role)
	# 							await member.remove_roles(role)	
	# 					cur_user.delete_instance()
	# 					exists = False
	# 				except:
	# 					pass
	# 			if exists == False:
	# 				server = ctx.message.guild
	# 				member = server.get_member(int(user_discordid))
	# 				try:
	# 					data = Utils.user.getUserData(handle,member)
	# 					if data['Status']==1:
	# 						await ctx.send(f"Handle not set!")	
	# 					else:
	# 						roles = member.roles
	# 						cur_user_new = User(username=handle,discordid=user_discordid,rating=data['Rating'],guild=serverid)
	# 						cur_user_new.save()
	# 						if exists:
	# 							cur_user.delete_instance()
	# 						for r in roles:
	# 							role = get(server.roles, name=r.name)
	# 							if str(role).find("★")!=-1:
	# 								print("Removing Role ",role)
	# 								await member.remove_roles(role)	
	# 						role = get(server.roles, name=data['Stars'].strip())
	# 						await member.add_roles(role)
	# 						await ctx.send(embed=data['embed'])	
	# 				except:
	# 					await ctx.send("```Handle not set ! Try again.```")
	# 		except:
	# 			await ctx.send("```Handle not set ! Check help for instructions```")


	

def setup(client):
	client.add_cog(Identification(client))