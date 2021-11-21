import discord
from discord.ext import commands
import asyncio, random, os


def get_luni_image():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("media/Images"):
        filenames.extend(filename)
        break
    return filenames


class ImageCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="image")
    async def __send_scream_command(self, ctx):
        try:
            path = str(f"media/Images/{str(random.choice(get_luni_image()))}")
            file = discord.File(path, filename="luni.png")
            embed = discord.Embed(title="BitLuni being a luni", colour=0x4287f5)
            embed.set_image(url="attachment://luni.png")
            await ctx.send(file=file, embed=embed)
        except discord.errors.Forbidden:
            await ctx.send(f"An error occurred, please make sure the bot has `Embed Links` permissions")
        except Exception as e:
            await ctx.send(f"An error occurred, please report the problem below to <@176371068448145408>\n```\n{e}\n```")


def setup(bot):
    bot.add_cog(ImageCommand(bot))