import discord
from discord.ext import commands
import asyncio, random, os
import urllib.parse

def get_bitluni():
    filenames = []
    for (dirpath, dirname, filename) in os.walk("media/Audio"):
        filenames.extend(filename)
        break
    return filenames

class SayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    async def __say_command__(self, ctx, *, text: str = None):
        if text is None:
            return await ctx.send("You need some text to say!")
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

        urlencodedtext = urllib.parse.quote(text, safe='')

        TTSURL = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en_gb&q={urlencodedtext}"

        await asyncio.sleep(0.5)

        audio_source = discord.FFmpegPCMAudio(TTSURL)
        await message.edit(content="**huhr**")

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else: 
            return
        while True:
            if not voice_client.is_playing():
                await asyncio.sleep(0.5)
                await voice_client.disconnect()
                return
            else:
                await asyncio.sleep(0.1)
                continue



def setup(bot):
    bot.add_cog(SayCommand(bot))
