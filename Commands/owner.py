import discord
from discord.ext import commands
import asyncio, random, os


def check_if_correct_user(ctx):
    if ctx.author.id in [176371068448145408, 478875507392380929]:
        return True
    else:
        return False


class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.check(check_if_correct_user)
    async def owner(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Owner Command Passed')

    @owner.command()
    @commands.check(check_if_correct_user)
    async def restart(self, ctx):
        await ctx.send("Restarting bot, please wait")
        await self.bot.change_presence(activity=discord.Game(status=discord.Status.dnd, name='Restarting Bot, Please Wait'))
        os._exit(1)

    @owner.command()
    @commands.check(check_if_correct_user)
    async def shutdown(self, ctx):
        print("Shutting down")
        await ctx.send("Shutting down bot")
        print("Exiting")
        os._exit(0)

    @owner.group()
    @commands.is_owner()
    async def cogmanager(self, ctx):
        'Bot Cog/Extention Manager'
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Cog Manager Command Passed')

    @cogmanager.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f':warning: **`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(':white_check_mark: **`SUCCESS`**, loaded `{}`'.format(cog))

    @cogmanager.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f':warning: **`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(':white_check_mark: **`SUCCESS`**, unloaded `{}`'.format(cog))

    @cogmanager.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f':warning: **`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(':white_check_mark: **`SUCCESS`**, reloaded `{}`'.format(cog))


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
