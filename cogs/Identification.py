import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import random
from .Utils import user, constants, cc_commons

VERTIFICATION_TIME = 60



class Identification(commands.Cog):
	"""docstring for Identification"""
	def __init__(self, client):
		self.client = client
		self.driver = cc_commons.setup_webdriver()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Identification is online")

	@commands.command(brief='Check users in server [Disabled]')
	async def handles(self,ctx,handle=None):
		"""Check Users in Server'"""
		await ctx.send(f"```This command has been deactivated, due to current shortage of resources.\nIt will be enabled in future```")

	@commands.command(brief='Identify users')
	async def identify(self,ctx,handle=None):
		"""Indentify users by their Codechef handles"""
		serverid = int(ctx.message.guild.id)
		if handle==None:
			await ctx.send("```You need to provide your handle !```")
		else:
			hashString = user.getUserNameHash()
			await ctx.send(f"`Indentifying {handle}`.\n```md\nSet your Codechef Name to '{hashString}' in 60 Seconds.```")	
			if constants.DEBUG == '1':
				await asyncio.sleep(5)
			else:
				await asyncio.sleep(VERTIFICATION_TIME)
			server = ctx.message.guild
			member = server.get_member(ctx.author.id)
			try:
				user_data = user.fetchUserData(handle,self.driver)
				if user_data['status']==1:
					await ctx.send(f"```Handle not set!```")	
				else:
					if constants.DEBUG == '1' or user_data['name'].strip() == hashString:
						roles = member.roles
						for r in roles:
							role = get(server.roles, name=r.name)
							if str(role).find("★")!=-1:
								await member.remove_roles(role)	
						role = get(server.roles, name=user_data['stars'].strip())
						await member.add_roles(role)
						desc = "**Handle for <@{}> succesfully set to [{}](https://www.codechef.com/users/{})**".format(member.id,handle,handle)
						colour = cc_commons.getDiscordColourByRating(user_data['rating'])
						embed = discord.Embed(description=desc, color=colour)
						embed.add_field(name='Rating', value=user_data['rating'], inline=True)
						embed.add_field(name='Stars', value=user_data['stars'], inline=True)
						embed.set_thumbnail(url=user_data['profilePicture'])
						await ctx.send(embed=embed)	
					else:
						await ctx.send("```Handle not set ! Hash Not Matched ! Try again.```")
			except Exception as e:
				print(e)
				await ctx.send("```Handle not set ! Try again.```")


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
			serverid = int(ctx.message.guild.id)
			user_discordid = discord_user[3:-1]
			hashString = user.getUserNameHash()
			server = ctx.message.guild
			member = server.get_member(int(user_discordid))
			try:
				user_data = user.fetchUserData(handle)
				if user_data['status']==1:
					await ctx.send(f"```Handle not set!```")	
				else:
					if constants.DEBUG or user_data['name'].strip() == hashString:
						roles = member.roles
						for r in roles:
							role = get(server.roles, name=r.name)
							if str(role).find("★")!=-1:
								await member.remove_roles(role)	
						role = get(server.roles, name=user_data['stars'].strip())
						await member.add_roles(role)
						desc = "**Handle for <@{}> succesfully set to [{}](https://www.codechef.com/users/{})**".format(member.id,handle,handle)
						colour = cc_commons.getDiscordColourByRating(user_data['rating'])
						embed = discord.Embed(description=desc, color=colour)
						embed.add_field(name='Rating', value=user_data['rating'], inline=True)
						embed.add_field(name='Stars', value=user_data['stars'], inline=True)
						embed.set_thumbnail(url=user_data['profilePicture'])
						await ctx.send(embed=embed)	
					else:
						await ctx.send("```Handle not set ! Hash Not Matched ! Try again.```")
			except Exception as e:
				print(e)
				await ctx.send("```Handle not set ! Try again.```")


	

def setup(client):
	client.add_cog(Identification(client))