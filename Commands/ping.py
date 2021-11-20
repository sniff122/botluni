import discord
from discord.ext import commands
import asyncio, random, os

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        'Pings the bot to check Discord API latency'
        embed = discord.Embed(title='Ping', description='Ping results')
        embed.set_footer(text="BotLuni developed by @sniff122#6218")
        latency = self.bot.latency
        latency = round((latency*1000), 2)
        embed.add_field(name="Websocket Latency", value=f"{latency}ms")
        try:
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"Unable to send embed, please make sure I have the permission to `Embed Links`\nWebsocket Latency: {latency}ms")


def setup(bot):
    bot.add_cog(PingCommand(bot))