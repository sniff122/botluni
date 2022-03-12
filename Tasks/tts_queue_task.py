import urllib.parse
import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks

import logging

logger = logging.getLogger("Botluni.TTSQueue")
logger.setLevel(logging.INFO)


class TTSQueueTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db
        self.do_tts_queue.start()

    def cog_unload(self):
        self.do_tts_queue.cancel()

    @tasks.loop(seconds=1)
    async def do_tts_queue(self):
        logger.debug("Running task")
        if len(self.bot.tts_queue) == 0:
            logger.debug("TTS queue is empty")
            return
        logger.debug("TTS queue has something")
        if self.bot.tts_vc is None:
            logger.debug("Bot VC is none")
            return
        logger.debug("Bot is in VC")
        voice_client: discord.VoiceClient = self.bot.tts_vc.guild.voice_client
        if voice_client is None:
            logger.debug("Bot somehow has no voice client?")
            return

        for message in self.bot.tts_queue:
            logger.debug(message)
            self.bot.tts_queue.remove(message)
            urlencodedtext = urllib.parse.quote(message["message"], safe='')
            audio_source = discord.FFmpegPCMAudio(f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={message['lang']}&q={urlencodedtext}")
            logger.debug("Playing message")
            voice_client.play(audio_source)

            while voice_client.is_playing():
                await asyncio.sleep(0.1)
            logger.debug("Message played")


    @do_tts_queue.before_loop
    async def before_tts_queue(self):
        logger.info("Waiting until bot is ready to start task")
        await self.bot.wait_until_ready()
        logger.info("Bot ready, starting task...")


def setup(bot):
    bot.add_cog(TTSQueueTask(bot))