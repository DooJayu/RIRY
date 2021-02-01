import discord
from discord.ext import commands
import urllib.request
import datetime
import json
import asyncio
class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/PortfolioData.json", "r", encoding='utf8') as f:
                self.user = json.load(f)  

    @commands.command()
    async def crypto(self, ctx, coin: str):
        with open("data/crypto.json", "r", encoding='utf8') as f:
                stats = json.load(f) 
        for currency in stats:
            if currency["id"] == coin.lower():
                crypto_data = currency
                break
        embed = discord.Embed(
            title="{0} ({1})".format(crypto_data["name"], crypto_data["symbol"].upper()),
            timestamp=datetime.datetime.utcnow()
        )
        # Current Price ($USD):
        embed.add_field(name="Current Price ($USD):", value=f'${crypto_data["current_price"]} per 1 {crypto_data["symbol"].upper()}',inline=False)
        # embed.add_field(name="24H Price Change Percentage:", value=f'{str(round(crypto_data["price_change_percentage_24h"], 2))}%',inline=False)
        embed.add_field(name="24H Price Change ($USD):", value=f'{str(round(crypto_data["price_change_percentage_24h"], 2))}% (${crypto_data["price_change_24h"]})',inline=False)
        embed.set_thumbnail(url=str(crypto_data["image"]))
        embed.set_footer(text="Powered by CoinGecko", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="portfolio", aliases=["p", "port"])
    async def _portfolio(self, ctx):
        if ctx.invoked_subcommand is None:
            author_id = ctx.message.author.id
            if not str(author_id) in self.user:
                await ctx.invoke(self.bot.get_command('portfolio help'))
            if str(author_id) in self.user:
                portfolio_embed = discord.Embed(
                    title=f"{ctx.message.author.name}'s Portfolio",
                    description="Portfolio to track cryptocurrencies for a user. user `r!portfolio set` to set amount of cryptocurrency.",
                    timestamp=datetime.datetime.utcnow()
                )
                total_value = 0
                for currency in self.user[str(author_id)]:
                    with open("data/crypto.json", "r", encoding='utf8') as f:
                        stats = json.load(f) 
                        for name in stats:
                            if name["id"] == currency:
                                crypto_data = name
                                portfolio_embed.add_field(name=f"{currency}", 
                                value=f"`{self.user[str(author_id)][currency]} {str(crypto_data['symbol']).upper()}` @ ${round(float(self.user[str(author_id)][currency]) * crypto_data['current_price'], 2)}")
                                total_value = total_value + (round(float(self.user[str(author_id)][currency]) * crypto_data['current_price'], 2))
                portfolio_embed.set_footer(text=f"Total value: ${str(total_value)}", icon_url=ctx.message.author.avatar_url)
                portfolio_embed.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.send(embed=portfolio_embed)

    @_portfolio.group(name="set")
    async def _set(self, ctx, crypto_name: str, value): 
        try:
            float(value)
        except ValueError:
            await ctx.send("Please enter a valid value")
        author_id = ctx.message.author.id
        if not str(author_id) in self.user:
                await ctx.invoke(self.bot.get_command('portfolio help'))
        if str(author_id) in self.user:
            with open("data/crypto.json", "r", encoding='utf8') as f:
                stats = json.load(f) 
                for currency in stats:
                    if currency["id"] == crypto_name.lower():
                        crypto_data = currency
                        break
                if crypto_data is None:
                    await ctx.send("Please use our supported cryptocurrency `r!portfolio help`")
                else:
                    if crypto_data['circulating_supply'] < float(value):
                        await ctx.send(f"The value you entered is over the current circulating supply for {crypto_data['name']}")
                    else:                   
                        if "," in value:
                            value.replace(",", "")
                        with open("data/PortfolioData.json", "w", encoding='utf8') as f:
                            if crypto_data["id"] in self.user[str(author_id)] and value == "0":
                                del self.user[str(author_id)][crypto_data["id"]]
                                await ctx.send(f"{crypto_data['name']} has been removed from portfolio.")
                            else:
                                self.user[str(author_id)][crypto_data['id']] = float(value)
                                json.dump(self.user, f, indent=4)
                                await ctx.send(f"`{float(value)}` of  `{crypto_data['name']}` has now been set in your portfolio!")
        

    @_portfolio.group(name="init")
    async def _portfolio_init(self, ctx):
        author_id = ctx.message.author.id
        if str(author_id) in self.user:
            await ctx.send("You already have a portfolio initialized. Use `r!portfolio help` for more info.")
        if not str(author_id) in self.user:
            def check(reaction, user):
                return str(reaction) == "✔️" or "❌" and user.id == author_id
            msg = await ctx.send("NOTICE: All of your cryptocurrency amounts and value will be displayed to other users if it is invoked.\nIn addition, prices are updated every 1 minutes due to API restrictions.\nReact to '✔️' to accept this, or '❌' to deny and cancel the intialization.")
            await msg.add_reaction("✔️")
            await msg.add_reaction("❌")
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                if str(reaction.emoji) == "✔️":
                    with open("data/PortfolioData.json", "w", encoding='utf8') as f:
                        await ctx.send("Initializing...")
                        self.user[str(author_id)] = {}
                        json.dump(self.user, f, indent=4)
                        await ctx.send("Done, use `r!portfolio set` to continue. For more info, use `r!portfolio help`")
                if str(reaction.emoji) == "❌":
                    await ctx.send("Initialization canceled.")
            except asyncio.TimeoutError:
                print("Timeout")

    @_portfolio.group(name="help")
    async def _portfolio_help(self, ctx):
        embed = discord.Embed(
            title="Portfolio/Crypto Command Hub",
            description="Portfolio command is a command where you can set your amount you have in crypto into one place. This can help as you don't need to log into your wallet to quickly check the current value of your crypto. You can look up specific crypto prices aswell."
        ) 
        embed.add_field(name="Subcommands:", value="`portfolio` - Shows your portfolio after initialization\n`portfolio set [currency] [amount]` - Sets amount of currency you specify into portfolio\n`portfolio init` - Initializes portfolio for new users\n`crypto [currency]` - Look up current prices for a currency\n\n**FAQ:**\n`Will people see my portfolio?`\nYes, you are warned of this if you initialize one.\n`When will you register (insert currency) to the bot?`\nI'll add more if there is demand/popularity for it.\n`When does the price update?`\nIt updates every 1 minutes.", inline=True)
        embed.set_thumbnail(url="https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/icon/generic.png")
        embed.set_footer(text="Developed by Kacper#7865", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Crypto(bot))