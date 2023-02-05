import logging
from discord.ext.commands import Bot

def add_on_member_join(bot: Bot) -> None:

    @bot.event
    async def on_member_join(member):
        logging.info(f'{member} joined the server')
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )
        