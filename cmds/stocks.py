import discord
from discord.ext import commands

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Stocks(bot))