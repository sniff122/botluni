import discord
from discord.ext import commands
import asyncio, random, os


def get_luni_gif():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("media/GIFs"):
        filenames.extend(filename)
        break
    return filenames


class GIFCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gif")
    async def __send_gif_command(self, ctx):
        try:
            path = str(f"media/GIFs/{str(random.choice(get_luni_gif()))}")
            file = discord.File(path, filename="luni.gif")
            embed = discord.Embed(title="What is Bitluni up to? Being a luni of course!", colour=0x4287f5)
            embed.set_image(url="attachment://luni.gif")
            await ctx.send(file=file, embed=embed)
        except discord.errors.Forbidden:
            await ctx.send(f"An error occurred, please make sure the bot has `Embed Links` permissions")
        except Exception as e:
            await ctx.send(f"An error occurred, please report the problem below to <@176371068448145408>\n```\n{e}\n```")


def setup(bot):
    bot.add_cog(GIFCommand(bot))
