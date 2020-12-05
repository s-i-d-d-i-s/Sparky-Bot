import discord
from discord.ext import commands
import asyncio
import random
import os
import Utils.tasks as tasks
## Setup Client
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix= '=', intents = intents)


## Source : https://github.com/cheran-senthil/TLE/blob/724adb4410dc28ad0d556b7c675316131139e3c2/tle/util/discord_common.py#L112
async def presence(bot):
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name='your commands'))
    await asyncio.sleep(60)

    @tasks.task(name='OrzUpdate', waiter=tasks.Waiter.fixed_delay(5*60))
    async def presence_task(_):
        while True:
            target = random.choice([
                member for member in bot.get_all_members()
            ])
            await bot.change_presence(activity=discord.Game(
                name=f'{target.display_name} orz'))
            await asyncio.sleep(10 * 60)
    presence_task.start()



## Load Cogs
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension("cogs.{}".format(filename.replace('.py','').strip()))


## On Ready
@client.event
async def on_ready():
	print("Bot is Ready")
	asyncio.create_task(presence(client))


## On Member Join
@client.event
async def on_member_join(member):
	print(f'{member} has joined our kitchen named {member.guild}!')



## On Member Remove
@client.event
async def on_member_remove(member):
	print(f'{member} has left our named {member.guild}!')


#Add Your Bot Token
token = ""


client.run(token)