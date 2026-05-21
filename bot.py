# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys
import glob
import importlib
import logging
import logging.config
import pytz
import asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import idle
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from Script import script
from datetime import date, datetime
from aiohttp import web
from plugins import web_server
from plugins.clone import restart_bots

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
loop = asyncio.get_event_loop()

required_vars = {
    "BOT_TOKEN": BOT_TOKEN,
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "DATABASE_URI": DATABASE_URI,
    "LOG_CHANNEL": LOG_CHANNEL
}

missing_vars = [key for key, value in required_vars.items() if not value]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


async def load_plugins():
    for name in files:
        try:
            with open(name):
                patt = Path(name)
                plugin_name = patt.stem.replace('.py', '')
                plugins_dir = Path(f"plugins/{plugin_name}.py")
                import_path = f"plugins.{plugin_name}"

                spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
                load = importlib.util.module_from_spec(spec)

                if spec and spec.loader:
                    spec.loader.exec_module(load)
                    sys.modules[f"plugins.{plugin_name}"] = load
                    logging.info(f"Imported Plugin => {plugin_name}")

        except Exception as e:
            logging.error(f"Failed loading plugin {name}: {e}")


async def start():
    print('\n')
    print('Initializing Your Bot')

    await TechVJBot.start()

    try:
        bot_info = await TechVJBot.get_me()
        logging.info(f"Logged in as {bot_info.first_name}")
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
        return

    await initialize_clients()
    await load_plugins()

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    try:
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
    except Exception as e:
        logging.error(f"Failed loading banned users/chats: {e}")

    try:
        await Media.ensure_indexes()
    except Exception as e:
        logging.error(f"Mongo index creation failed: {e}")

    me = await TechVJBot.get_me()

    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    logging.info(LOG_STR)
    logging.info(script.LOGO)

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    try:
        await TechVJBot.send_message(
            chat_id=LOG_CHANNEL,
            text=script.RESTART_TXT.format(today, time)
        )
    except Exception as e:
        logging.error(f"Failed sending restart message: {e}")

    if CLONE_MODE:
        try:
            logging.info("Restarting All Clone Bots.......")
            await restart_bots()
            logging.info("Restarted All Clone Bots.")
        except Exception as e:
            logging.error(f"Clone bot restart failed: {e}")

    try:
        web_app = web.AppRunner(await web_server())
        await web_app.setup()
        bind_address = '0.0.0.0'
        await web.TCPSite(web_app, bind_address, PORT).start()
        logging.info(f"Web server started on port {PORT}")
    except Exception as e:
        logging.error(f"Web server failed: {e}")

    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
