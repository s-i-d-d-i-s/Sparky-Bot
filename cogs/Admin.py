import discord
from discord.ext import commands
from .Utils import database,cc_commons
import asyncio
import random
from discord.utils import get
import os
import pickle



class Admin(commands.Cog):
	"""docstring for Admin"""
	def __init__(self, client):
		self.client = client
		self.db = database.DB()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Admin is online")

	@commands.group(brief='Commands related to Admin',invoke_without_command=True)
	async def admin(self, ctx):
		"""Commands related to handles"""
		await ctx.send_help('admin')


	@admin.command(brief='Display handle data')
	async def get_handle_data(self,ctx,username):
		"""Display handle data"""
		data = self.db.fetch_cc_user(username)
		print(data)
		if(len(str(data))<1990):
			await ctx.send(f"```{str(data)}```")
		else:
			await ctx.send(f"```Data length too big```")
		
		
	@admin.command(brief='Update Handle Data')
	async def update_handle_data(self,ctx,username):
		"""Update Handle Data"""
		data = cc_commons.getUserData(username)
		if data['status']:
			self.db.update_cc_user(username, data['name'], data['profile_pic'], data['rating'], data['rating_data'])
			await ctx.send("```User Data Updated.```")
		else:
			await ctx.send("```Please check the username or try again later```")
			

def setup(client):
	client.add_cog(Admin(client))