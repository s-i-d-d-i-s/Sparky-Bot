import discord
from discord.ext import commands
import asyncio
import json
import requests
import bs4
import random
import re
import time
from .Utils import cc_commons, user, cc_api


class Features(commands.Cog):

	dataset = {}
	"""docstring for Features"""
	def __init__(self, client):
		self.client = client
		self.dataset = json.loads(open('Data/dataset.json').read())
		self.apiObj = cc_api.CodechefAPI()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Features is online")
	

	@commands.command(brief='Display recent solves by a user')
	async def stalk(self,ctx,username=None):
		"""Display recent solves by a user"""
		if username==None:
			username = cc_commons.get_user_by_discord_id(ctx.author.id,ctx.message.guild.id,self.apiObj.db)

		if username==None:
			await ctx.send("```Enter the handle !```")
		else:
			try:
				colour = cc_commons.getRandomColour()
				embed = discord.Embed(description="**These are the recent submissions from [{}](https://codechef.com/users/{}).**".format(username,username),color=colour)
				data =  user.getSubmission(username,self.apiObj)
				for d in data:
					embed.add_field(name=f'{d[0]}', value=d[1], inline=False)
				embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
			except Exception as e:
				print(e)
				await ctx.send("```Please try again !```")


	@commands.command(brief='Get insights of a Codechef User')
	async def scan(self,ctx,username=None):
		"""Analysis of a codechef profile"""
		await ctx.send("```Under Construction...```")
		return
		
		if username==None:
			username = cc_commons.get_user_by_discord_id(ctx.author.id,ctx.message.guild.id,self.apiObj.db)
		if username==None:
			await ctx.send("```Enter the handle !```")
		else:
			await ctx.send(f"```Scanning {username}...Please Wait```")
			try:
				data = user.scan_util(username,self.apiObj)
			except Exception as e:
				print(e)
				await ctx.send(f"```Something went wrong... Check the username or try again in sometime.```")
				return 
			feedback_fav = user.get_feedback_for_fav(data['long_contest'],data['short_contest'],username)
			feedback_rr = user.get_feedback_for_real_ratio(data['real_ratio'],username)
			
			if data['real_ratio'] == "INF":
				feedback_rr =  "Mega orz... No long challenges, what a legend !"
				data['real_ratio'] = "Infinity"
			else:
				data['real_ratio'] = round(data['real_ratio'],3)

			analysis = user.getAnalysis(username,data,feedback_rr,feedback_fav)
			desc=f"**Analysis of [{username}](https://www.codechef.com/users/{username}) **"
			embed = discord.Embed(description=desc, color=cc_commons.getDiscordColourByRating(int(data['current_rating'])))
			embed.add_field(name=f'**Result**', value=analysis, inline=False)
			embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

	# @commands.command(brief='Get a random unsolved problem')
	# async def gimme(self,ctx,username=None,level=None):
	# 	"""level = ['noob','easy','medium','hard']"""
	# 	if username==None:
	# 		await ctx.send("```Enter the handle !```")
	# 	else:
	# 		if level == None:
	# 			level = random.choice(['noob','easy','medium'])
	# 		if level not in ['noob','easy','medium','hard']:
	# 			await ctx.send("```Enter a valid level : ['noob','easy','medium','hard']```")
	# 		else:
	# 			try:
	# 				cur_time = int(time.time())
	# 				if username not in self.lastUpdated.keys():
	# 					self.lastUpdated[username]=0
	# 				if (cur_time - self.lastUpdated[username] ) > 1800:
	# 					self.lastUpdated[username]=cur_time
	# 					self.solvedCodes[username] = user.getSolvedCodes(username,self.driver)
	# 				solved = self.solvedCodes[username]
	# 				problems = self.dataset[level]
	# 				tries = 10
	# 				found=False
	# 				while tries>0:
	# 					cur_prob = random.choice(problems)
	# 					if cur_prob['problemCode'] not in solved.keys():
	# 						found=True
	# 						title = '{}'.format(cur_prob['problemCode'])
	# 						desc = cur_prob['problemName']
	# 						embed = discord.Embed(title=title, url=cur_prob['link'], description=desc)
	# 						embed.add_field(name='Level', value=level.capitalize())
	# 						embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
	# 						await ctx.send(f'Recommended problem for `{username}`', embed=embed)
	# 						break
	# 					tries-=1
	# 				if found == False:
	# 					await ctx.send(f"```Unable to find a matching problem, try again later!```")
	# 			except Exception as e:
	# 				print(e)
	# 				await ctx.send(f"```Something went wrong, check username or try again```")



def setup(client):
	client.add_cog(Features(client))