import discord
from discord.ext import commands, tasks
import datetime
import json
import codecs
import urllib.request

class Background_Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.price_task = self.update_crypto_price.start()
        
    @tasks.loop(minutes=1)
    async def update_crypto_price(self):
        link = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
        with open("data/crypto.json", "r") as jsonFile:
            url_get = urllib.request.urlopen(f'{link}').read().decode()
            data = json.loads(url_get)
            with open("data/crypto.json", "w") as jsonFile:
                json.dump(data, jsonFile, ensure_ascii=False, indent=4)

    
    @update_crypto_price.before_loop
    async def before_update_crypto_price(self):
        await self.bot.wait_until_ready()
    

def setup(bot):
    bot.add_cog(Background_Tasks(bot))