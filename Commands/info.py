import discord
from discord.ext import commands
import asyncio, random, os


def get_bitluni_audio():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("Audio"):
        filenames.extend(filename)
        break
    return filenames


def get_luni_image():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("Images"):
        filenames.extend(filename)
        break
    return filenames


class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def __info_command__(self, ctx):
        latency = self.bot.latency
        latency = round((latency*1000), 1)

        embed = discord.Embed(title="Botluni Information", colour=0x00ffff)
        embed.set_footer(text="BotLuni developed by @sniff122#6218")
        embed.add_field(name="Developer", value="<@176371068448145408>", inline=False)
        embed.add_field(name="Discord Version", value=discord.__version__, inline=False)
        embed.add_field(name="Websocket Latency", value=f"{latency}ms", inline=False)
        embed.add_field(name="Total Audio Clips", value=str(len(get_bitluni_audio())), inline=False)
        embed.add_field(name="Total Images", value=str(len(get_luni_image())), inline=False)

        try:
            await ctx.send(embed=embed)
        except:
            await ctx.send("Unable to send message, please make sure I have the permission to `Embed Links`")


def setup(bot):
    bot.add_cog(InfoCommand(bot))