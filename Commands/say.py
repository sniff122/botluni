import discord
from discord.ext import commands
import asyncio, random, os
import urllib.parse
import time


class SayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langto = {"seon": "en_au", "bitluni": "de", "lewis": "en_gb"}

    @commands.command(name="lang")
    async def __lang_command(self, ctx, lang: str = None):
        try:
            lang = self.langto[lang]
        except:
            pass
        await self.bot.db.execute("INSERT INTO userlangs (userid, lang) VALUES ($1, $2) ON CONFLICT ON CONSTRAINT userlangs_pkey DO UPDATE SET lang=$2", ctx.author.id, lang)
        return await ctx.message.add_reaction("👍")


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

        if voice_client.is_playing():
            await message.edit(content="I'm already speaking! Wait until im finished!")
            return

        urlencodedtext = urllib.parse.quote(text, safe='')

        userlang = await self.bot.db.fetch("SELECT * FROM userlangs WHERE userid=$1", ctx.author.id)
        if len(userlang) == 0:
            lang = "it"
        else:
            lang = userlang[0]["lang"]

        TTSURL = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={urlencodedtext}"

        await asyncio.sleep(0.5)

        audio_source = discord.FFmpegPCMAudio(TTSURL)
        await message.edit(content="**huhr**")

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else: 
            return

        start = time.time()

        while True:
            if not voice_client.is_playing():
                await asyncio.sleep(0.5)
                await voice_client.disconnect()
                return
            else:
                cur = time.time()
                if cur-start > 10:
                    await message.edit(content="I've been speaking for too long! I need a rest! <:bitlunisleepy:912806551742464020>")
                    await voice_client.disconnect()
                await asyncio.sleep(0.1)
                continue



def setup(bot):
    bot.add_cog(SayCommand(bot))
