import discord
from discord.ext import commands
import asyncio, random, os

class onreadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready and online. :-)')
        print('Bot User Name: ' + self.bot.user.name)
        print('Bot ID: ' + str(self.bot.user.id))
        await self.bot.change_presence(activity=discord.Game(name='BotLuni hä', type=0))

        for command in self.bot.config["disabled commands"]:
            print(f"Disabling command '{command}'")
            cmd = self.bot.get_command(command)
            cmd.enabled = False


def setup(bot):
    bot.add_cog(onreadyEvent(bot))
