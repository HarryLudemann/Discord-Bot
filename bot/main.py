import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
if __name__ != '__main__':
    import bot.commands as custom_commands
    import bot.events as custom_events

def __setup_logging():
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

def start():
    """load environment variables, setup logging and initialize bot"""
    # load environment variables and setup logging
    load_dotenv()
    __setup_logging()
    # initialize
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    intents.reactions = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='#', intents=intents)
    # add each function in custom_events
    for event in custom_events.__all__:
        getattr(custom_events, event)(bot)
    # add each custom commands
    for command in custom_commands.__all__:
        bot.add_command(getattr(custom_commands, command))
    # start
    bot.run(os.getenv('TOKEN'))