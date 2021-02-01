import discord
from discord.ext import commands, tasks
import json
import asyncio
import datetime
import os

# To get Variables for setting up RIRY
with open("data/BotSetup.json", 'r', encoding="utf8") as jsonf:
    BotSetup = json.load(jsonf)

# Setting up the bot prefix for server usage
bot = commands.Bot(command_prefix=BotSetup['PREFIX'])
 
# Setup 
@bot.event
async def on_ready():
    print(">> RIRY is now launched onto the Discord servers! <<")

    messages = BotSetup['STATUS']
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=messages[0], type=discord.ActivityType.watching))
        messages.append(messages.pop(0))
        await asyncio.sleep(10)

for file in os.listdir("cmds"):
    if file.endswith(".py"):
        bot.load_extension(f'cmds.{file[:-3]}')

if __name__ == "__main__":  
    # Use Token to run RIRY
    bot.run(BotSetup['TOKEN'])