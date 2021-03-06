import discord
from discord.ext import commands
from discord import opus
import asyncio
import json
import os
import traceback
import asyncpg
import logging
import quart


dlogger = logging.getLogger("discord")
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('BotLuni')
logger.setLevel(logging.DEBUG)


with open("config.json", "r") as f:
    config = json.load(f)

with open("commands.json", "r") as f:
    cmds = json.load(f)


async def create_db():
    creds = {
        "host": config["db"]["host"],
        "database": config["db"]["database"],
        "user": config["db"]["user"],
        "password": config["db"]["password"]
    }

    global db
    logger.info("Connecting to DB")
    try:
        db = await asyncpg.create_pool(**creds, max_size=20, min_size=2)
    except:
        logger.fatal(f"FAILED to connect to DB:")
        traceback.print_exc()
        os._exit(1)

    logger.info("Connected to DB")

    return db


def save_config(conf):
    with open("config.json", "w") as f:
        json.dump(conf, f, indent=4)


def load_opus_lib(opus_libs=['/bot/libopus.so.0']):
    if opus.is_loaded():
        return True
    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            raise
        raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))


def check_if_correct_user(ctx):
    if ctx.author.id in [176371068448145408, 478875507392380929]:
        return True
    else:
        return False


intents = discord.Intents.all()

prefix = config["prefix"]
cmds_dir = config["cmds_dir"]
events_dir = config["events_dir"]
tasks_dir = config["tasks_dir"]
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True, intents=intents)
bot.remove_command("help")
bot.config = config
bot.save_config = save_config
bot.cmds = cmds
bot.db = bot.loop.run_until_complete(create_db())

bot.tts_queue = []
bot.tts_vs = None

app = quart.Quart("botluni_http")


for extension in [f.replace('.py', '') for f in os.listdir(cmds_dir) if os.path.isfile(os.path.join(cmds_dir, f))]:
    try:
        print(f"COGMAN: LOADING: {cmds_dir}.{extension}")
        bot.load_extension(cmds_dir + "." + extension)
    except (discord.ClientException, ModuleNotFoundError):
        print(f'Failed to load extension {extension}.')
        traceback.print_exc()


for extension in [f.replace('.py', '') for f in os.listdir(events_dir) if os.path.isfile(os.path.join(events_dir, f))]:
    try:
        print(f"COGMAN: LOADING: {events_dir}.{extension}")
        bot.load_extension(events_dir + "." + extension)
    except (discord.ClientException, ModuleNotFoundError):
        print(f'Failed to load extension {extension}.')
        traceback.print_exc()

for extension in [f.replace('.py', '') for f in os.listdir(tasks_dir) if os.path.isfile(os.path.join(tasks_dir, f))]:
    try:
        print(f"COGMAN: LOADING: {tasks_dir}.{extension}")
        bot.load_extension(tasks_dir + "." + extension)
    except (discord.ClientException, ModuleNotFoundError):
        print(f'Failed to load extension {extension}.')
        traceback.print_exc()


@app.route("/", methods=["GET"])
async def main_route():
    return quart.redirect("https://sniff122.tech", 301)


@app.route("/tts_message", methods=["POST"])
async def handle_tts_messages_in():
    headers = quart.request.headers
    if headers["Authorization"] != "70d5bc2f37a53379f1c86209479f075a94023c857db2d2167233c6238e95b496":
        return {"status": 401, "message": "Unauthorised"}, 401

    body = await quart.request.json

    message_text = body["message"]
    message_lang = body["lang"]

    bot.tts_queue.append({"message": message_text, "lang": message_lang})
    return {"status": "200", "message": "OK"}, 200


@bot.group(name="tts")
@commands.has_role("admin")
async def __stream_tts_commands__(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        return await ctx.send("A valid tts subcommand is needed! see `botluni-help tts` for more info")

@__stream_tts_commands__.command(name="join")
@commands.has_role("admin")
async def __join_vc__(ctx: commands.Context, vc_id: discord.VoiceChannel = None):
    message = await ctx.send("Joining voice channel")
    guild = ctx.guild
    author: discord.Member = ctx.author
    if vc_id is None:
        try:
            vc_id = author.voice.channel
        except:
            await message.edit(content="You are not in a voice channel!")
            return
        try:
            await vc_id.connect()
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
    else:
        try:
            await vc_id.connect()
            voice_client: discord.VoiceClient = guild.voice_client
        except discord.errors.Forbidden:
            await message.edit(content="I do not have permission to join that voice channel")
            return
        except Exception as e:
            voice_client: discord.VoiceClient = guild.voice_client
            try:
                await voice_client.move_to(vc_id)
            except discord.errors.Forbidden:
                await message.edit(content="I do not have permission to join that voice channel")
                return
    print(vc_id)
    bot.tts_vc = vc_id
    print(bot.tts_vc)

@__stream_tts_commands__.command(name="leave")
@commands.has_role("admin")
async def __leave_vc__(ctx):
    guild = ctx.guild
    if guild.voice_client is None:
        return
    await guild.voice_client.disconnect()
    bot.tts_vc = None

@bot.event
async def on_ready():
    logger.info("""
 ___ _   _                                   ____        _   _             _ 
|_ _| |_( )___     __ _    _ __ ___   ___   | __ )  ___ | |_| |_   _ _ __ (_)
 | || __|// __|   / _` |  | '_ ` _ \ / _ \  |  _ \ / _ \| __| | | | | '_ \| |
 | || |_  \__ \  | (_| |  | | | | | |  __/  | |_) | (_) | |_| | |_| | | | | |
|___|\__| |___/   \__,_|  |_| |_| |_|\___|  |____/ \___/ \__|_|\__,_|_| |_|_|
""")
    bot.loop.create_task(app.run_task(host="0.0.0.0", port=9564, use_reloader=False))


@bot.command(name="reloadall")
@commands.check(check_if_correct_user)
async def __reload_all_command(ctx):
    msg = await ctx.send("Please wait, reloading all commands and events")
    await asyncio.sleep(1)
    for extension in [f.replace('.py', '') for f in os.listdir(cmds_dir) if os.path.isfile(os.path.join(cmds_dir, f))]:
        try:
            try:
                bot.unload_extension(cmds_dir + "." + extension)
            except:
                pass
            bot.load_extension(cmds_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError) as e:
            print(f'Failed to load extension {extension}.')
            await msg.edit(content=f"**Failed to load extension {extension}**\n```\n{e}\n```")
            traceback.print_exc()


    for extension in [f.replace('.py', '') for f in os.listdir(events_dir) if os.path.isfile(os.path.join(events_dir, f))]:
        try:
            try:
                bot.unload_extension(events_dir + "." + extension)
            except:
                pass
            bot.load_extension(events_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError) as e:
            print(f'Failed to load extension {extension}.')
            await msg.edit(content=f"**Failed to load extension {extension}**\n```\n{e}\n```")
            traceback.print_exc()


    for extension in [f.replace('.py', '') for f in os.listdir(tasks_dir) if os.path.isfile(os.path.join(tasks_dir, f))]:
        try:
            try:
                bot.unload_extension(tasks_dir + "." + extension)
            except:
                pass
            bot.load_extension(tasks_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError) as e:
            print(f'Failed to load extension {extension}.')
            await msg.edit(content=f"**Failed to load extension {extension}**\n```\n{e}\n```")
            traceback.print_exc()

    global config
    global cmds

    with open("config.json", "r") as f: 
        config = json.load(f)
    with open("commands.json", "r") as f:
        cmds = json.load(f)
        
    bot.config = config
    bot.cmds = cmds
    
    await msg.edit(content="Commands and events reload complete!")

#load_opus_lib()
bot.run(bot.config["token"])
