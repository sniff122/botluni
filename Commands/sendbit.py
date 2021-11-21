import discord
from discord.ext import commands
import asyncio, random, os

def get_luni():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("media/Audio"):
        filenames.extend(filename)
        break
    return filenames

class SendBitCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sendbit")
    async def __send_bit_command(self, ctx):
        try:
            path = str(f"media/Audio/{str(random.choice(get_luni()))}")
            await ctx.send(content="**hä**", file=discord.File(path, filename="luni.mp3"))
        except Exception as e:
            await ctx.send(f"An error occurred, please report the problem below to <@176371068448145408>\n```\n{e}\n```")


def setup(bot):
    bot.add_cog(SendBitCommand(bot))