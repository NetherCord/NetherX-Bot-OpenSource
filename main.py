import os
os.environ["NETHERX_BASE_DIR"] = os.path.dirname(__file__)

import cacher
cacher.initialize_cache_path()

from bot import bot
from operations.config import get_from_config


@bot.event
async def on_disconnect():
    cacher.clear_cache()


try:
    bot.run(get_from_config("discord_token"))
except Exception as e:
    # logs.send(e)
    print(e)
