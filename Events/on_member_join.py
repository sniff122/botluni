import discord
from discord.ext import commands
import asyncio, random, os


class onmemberjoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcomechannel = self.bot.get_channel(735572935082901514)

        await welcomechannel.send(f"Hey {member.mention}, welcome to {member.guild.name}!")


def setup(bot):
    bot.add_cog(onmemberjoinEvent(bot))
