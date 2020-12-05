import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
import re



class Features(commands.Cog):
	"""docstring for Features"""
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print("Features is online")
	
	@commands.command(brief='Display recent solves by a user')
	async def stalk(self,ctx,username=None):
		"""Display recent solves by a user"""
		if username==None:
			await ctx.send("```Enter the handle !```")
		else:
			try:
				url = "https://www.codechef.com/recent/user?page=1&user_handle={}".format(username)
				data = json.loads(requests.get(url).content)
				data = data['content']
				data = bs4.BeautifulSoup(data)
				subs = data.findAll('a')[:-2]
				subs = [x.text for x in subs]
				imgs = data.findAll('img')[:-2]
				pts = data.findAll('span')
				imgs = ["https://s3.amazonaws.com/codechef_shared"+x.attrs['src'] for x in imgs]
				colour = random.choice([discord.Colour.purple(),discord.Colour.green(),discord.Colour.blue(),discord.Colour.orange()])
				embed = discord.Embed(description="**These are the recent submissions from [{}](https://codechef.com/users/{}).**".format(username,username),color=colour)
				for i in range(min(len(imgs),5)):
					verd = "WA"
					if imgs[i].find("tick-icon")!=-1:
						verd = "AC"
					elif imgs[i].find("clock_error")!=-1:
						verd = "TLE"
					elif imgs[i].find("alert-icon")!=-1:
						verd = "CE"
					elif imgs[i].find("runtime")!=-1:
						verd = "RE"
					pts2 = re.findall("\[.*\]",pts[i].text)
					if len(pts2)==0:
						if verd == "AC":
							pts2 = "Accepted"
						elif verd == "WA":
							pts2 = "Wrong Answer"
						elif verd == "CE":
							pts2 = "Compilation Error"
						elif verd == "TLE":
							pts2 = "Time Limit Exceed"
						elif verd == "RE":
							pts2 = "Runtime Error"
					else:
						pts2="{}".format(pts2[0])

					em = '\N{EN SPACE}'
					sq = '\N{WHITE SQUARE WITH UPPER RIGHT QUADRANT}'
					desc = f'`{em}{verd}{em}| {em}{pts2}{em}`'
					embed.add_field(name=f'{subs[i]}', value=desc, inline=False)
				
				await ctx.send(embed=embed)
			except:
				await ctx.send("Please try again !")

def setup(client):
	client.add_cog(Features(client))