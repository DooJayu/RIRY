import discord
from discord.ext import commands
import datetime
import requests
import random
import datetime
import json

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("test/BotSetup.json", 'r', encoding="utf8") as jsonf:
            self.api = json.load(jsonf)

    @commands.command(name="stocknews", aliases=["news", "snews"])
    async def stock_news(self, ctx):
        r = requests.get(f'https://finnhub.io/api/v1/news?category=general&token={self.api["FINNHUB_API"]}')
        news = r.json()
        article = news[int(random.randint(0, len(news)+1))]
        news_embed = discord.Embed(
            title=(f"{article['headline']}"),
            description=(f"{article['summary']} | [Click here for article]({article['url']})"),
            timestamp=datetime.datetime.utcnow()
        )
        news_embed.set_image(url=f"{article['image']}")
        news_embed.set_footer(text=(f"article from {article['source']}"), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=news_embed)

    @commands.command(name="headlines", aliases=["sheadlines"])
    async def stock_headlines(self, ctx):
        r = requests.get(f'https://finnhub.io/api/v1/news?category=general&token={self.api["FINNHUB_API"]}')
        news = r.json()
        embed = discord.Embed(
            title=f"Top headlines for {datetime.datetime.now().date()}",
            timestamp=datetime.datetime.utcnow()
        )
        for article in range(0, 5):
            embed.add_field(name=f"{news[article]['headline']}", value=f"{news[article]['summary']} | [Click here for article]({news[article]['url']})", inline=False)
        embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/business-and-finance-monochrome-hand-drawn-free-se/100/newspaper-512.png")
        embed.set_footer(text=f"Have a good day!", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="cryptonews", aliases=["cnews"])
    async def crypto_news(self, ctx):
        r = requests.get(f'https://finnhub.io/api/v1/news?category=crypto&token={self.api["FINNHUB_API"]}')
        news = r.json()
        article = news[int(random.randint(0, len(news)+1))]
        news_embed = discord.Embed(
            title=(f"{article['headline']}"),
            description=(f"{article['summary']} | [Click here for article]({article['url']})"),
            timestamp=datetime.datetime.utcnow()
        )
        news_embed.set_image(url=f"{article['image']}")
        news_embed.set_footer(text=(f"article from {article['source']}"), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=news_embed)

    @commands.command(name="cryptoheadlines", aliases=["cheadlines"])
    async def crypto_headlines(self, ctx):
        r = requests.get(f'https://finnhub.io/api/v1/news?category=crypto&token={self.api["FINNHUB_API"]}')
        news = r.json()
        embed = discord.Embed(
            title=f"Top crypto headlines for {datetime.datetime.now().date()}",
            timestamp=datetime.datetime.utcnow()
        )
        for article in range(0, 5):
            embed.add_field(name=f"{news[article]['headline']}", value=f"{news[article]['summary']} | [Click here for article]({news[article]['url']})", inline=False)
        embed.set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/crypto-news-2360844-1970145.png")
        embed.set_footer(text=f"Have a good day!", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(News(bot))