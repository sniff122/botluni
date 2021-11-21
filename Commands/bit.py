import discord
from discord.ext import commands
import asyncio, random, os

def get_bitluni():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("media/Audio"):
        filenames.extend(filename)
        break
    return filenames

class BitCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bit")
    async def __bit_command__(self, ctx):
        message = await ctx.send("Joining voice channel")
        guild = ctx.guild
        author: discord.Member = ctx.author
        try:
            vc = author.voice.channel
        except:
            await message.edit(content="You are not in a voice channel!")
            return
        try:
            await vc.connect()
            voice_client: discord.VoiceClient = guild.voice_client
        except discord.errors.Forbidden:
            await message.edit(content="I do not have permission to join that voice channel")
            return
        except Exception as e:
            voice_client: discord.VoiceClient = guild.voice_client
            try:
                await voice_client.move_to(vc)
            except discord.errors.Forbidden:
                await message.edit(content="I do not have permission to join that voice channel")
                return
        audio_source = discord.FFmpegPCMAudio(str(f"media/Audio/{str(random.choice(get_bitluni()))}"))
        await message.edit(content="**hä**")
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else: 
            return
        while True:
            if not voice_client.is_playing():
                await voice_client.disconnect()
                return
            else:
                continue
            await asyncio.sleep(0.1)


def setup(bot):
    bot.add_cog(BitCommand(bot))
