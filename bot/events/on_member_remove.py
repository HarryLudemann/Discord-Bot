import logging
from discord.ext.commands import Bot

def add_on_member_remove(bot: Bot) -> None:

    @bot.event
    async def on_member_remove(member):
        logging.info(f'{member} left the server')