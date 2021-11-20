import discord
from discord.ext import commands
import asyncio, random, os

class oncommanderrorEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(content='The command you entered is correct but you have not provided enough arguments, you must have not provided a required argument')
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.channel.send(content='This command can only be used in Direct Messages')
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.channel.send(content='A permission error occured, please make sure the bot has permission to perform what you are doing')
        elif isinstance(error, commands.CheckFailure):
            await ctx.channel.send(content="The check for the command failed, you probably don't have the correct permissions to execute the command")
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.channel.send(content="Command not found, please check `botluni-help` for a list of commands")
            return
        raise error


def setup(bot):
    bot.add_cog(oncommanderrorEvent(bot))
