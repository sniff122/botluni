import discord
from discord.ext import commands
import asyncio, random, os

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def _help_command_(self, ctx, command:str=None):
        embed = discord.Embed(name="Bot Help", description="Help for the bot", colour=0xffffff)
        embed.set_footer(text="BotLuni developed by @sniff122#6218")

        if command == None:
            for command in self.bot.cmds:
                if command not in self.bot.config["disabled commands"]:
                    embed.add_field(name=command, value=self.bot.cmds[command]["description"], inline=False)
                else:
                    commanddescrip = self.bot.cmds[command]["description"]
                    embed.add_field(name=command, value=f"[DISABLED] - {commanddescrip}", inline=False)
        else:
            if command not in self.bot.cmds:
                embed.add_field(name="That command was not found", value="Please check your spelling or run the help command without an argument to see all commands", inline=False)
            else:
                if command not in self.bot.config["disabled commands"]:
                    embed.add_field(name=command, value=self.bot.cmds[command]["description"], inline=False)
                    embed.add_field(name="Command Arguments", value="`[Argument]` indicates a required argument, `<Argument>` indicates an optional argument", inline=False)
                    for argument in self.bot.cmds[command]["args"]:
                        if len(self.bot.cmds[command]["args"]) == 1:
                            embed.add_field(name=argument, value="** **", inline=False)
                        else:
                            embed.add_field(name=argument, value="─────────────", inline=False)
                else:
                    embed.add_field(name=command, value=self.bot.cmds[command]["description"], inline=False)
                    embed.add_field(name="This command is disabled", value="This means that it can not be used", inline=False)
                    embed.add_field(name="Command Arguments", value="`[Argument]` indicates a required argument, `<Argument>` indicates an optional argument", inline=False)
                    for argument in self.bot.cmds[command]["args"]:
                        if len(self.bot.cmds[command]["args"]) == 1:
                            embed.add_field(name=argument, value="** **", inline=False)
                        else:
                            embed.add_field(name=argument, value="─────────────", inline=False)
        
        try:
            await ctx.send(embed=embed)
        except:
            await ctx.send("Unable to send message, please make sure I have the permission to `Embed Links`")


def setup(bot):
    bot.add_cog(HelpCommand(bot))
