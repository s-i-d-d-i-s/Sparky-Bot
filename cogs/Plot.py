import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random




class Plot(commands.Cog):
	"""docstring for FunStuff"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Plot is online")

	

def setup(client):
	client.add_cog(Plot(client))