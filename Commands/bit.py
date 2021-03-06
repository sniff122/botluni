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
    async def __bit_command__(self, ctx, num: int = 1):
        if num > 10:
            num = 10
        if self.bot.tts_vc is not None:
            return await ctx.send(f"I'm currently handling stream TTS! Why don't you join {self.bot.tts_vc}!")
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

        if voice_client.is_playing():
            await message.edit(content="I'm already speaking! Wait until im finished!")
            return

        await message.edit(content="**hä**")

        played_audio = []

        for i in range(0, num):
            audio_file = random.choice(get_bitluni())
            while audio_file in played_audio:
                audio_file = random.choice(get_bitluni())
            played_audio.append(audio_file)
            audio_source = discord.FFmpegPCMAudio(str(f"media/Audio/{str(audio_file)}"))
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)
            else:
                return
            while voice_client.is_playing():
                await asyncio.sleep(0.1)
                continue
        await asyncio.sleep(0.5)
        await voice_client.disconnect()



def setup(bot):
    bot.add_cog(BitCommand(bot))
