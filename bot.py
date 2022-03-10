import discord
from discord.ext import commands
from discord import opus
import asyncio
import json
import os
import traceback
import asyncpg
import logging

os.system("pwd")
os.system("ls")

logger = logging.getLogger('BotLuni')
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')

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
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True, intents=intents)
bot.remove_command("help")
bot.config = config
bot.save_config = save_config
bot.cmds = cmds
bot.db = bot.loop.run_until_complete(create_db())


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


@bot.command(name="reloadall")
@commands.check(check_if_correct_user)
async def __reload_all_command(ctx):
    msg = await ctx.send("Please wait, reloading all commands and events")
    await asyncio.sleep(1)
    for extension in [f.replace('.py', '') for f in os.listdir(cmds_dir) if os.path.isfile(os.path.join(cmds_dir, f))]:
        try:
            bot.unload_extension(cmds_dir + "." + extension)
            bot.load_extension(cmds_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError) as e:
            print(f'Failed to load extension {extension}.')
            await msg.edit(content=f"**Failed to load extension {extension}**\n```\n{e}\n```")
            traceback.print_exc()
            return

    for extension in [f.replace('.py', '') for f in os.listdir(events_dir) if os.path.isfile(os.path.join(events_dir, f))]:
        try:
            bot.unload_extension(events_dir + "." + extension)
            bot.load_extension(events_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError) as e:
            print(f'Failed to load extension {extension}.')
            await msg.edit(content=f"**Failed to load extension {extension}**\n```\n{e}\n```")
            traceback.print_exc()
            return

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
