import discord
from discord.ext import commands
import os
import logging
import asyncio
import nest_asyncio
if __name__ != '__main__':
    from bot.constants import BOT_TOKEN

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def load_extensions(self):
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name and load extension
                await self.load_extension(f"bot.cogs.{filename[:-3]}")

def setup_logging():
    """Setup logging to file and console"""
    # clear log file
    with open('bot.log', 'w') as f:
        f.write('')
    # set logging preferences
    formatter = logging.Formatter('%(asctime)s %(levelname)s     %(message)s', '%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # add console logging to file
    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # add logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

async def main():
    setup_logging()
    async with Bot(command_prefix='#', intents=discord.Intents.all()) as bot:
        await bot.load_extensions()
        bot.run(BOT_TOKEN)

def start():
    nest_asyncio.apply()
    asyncio.run(main())

