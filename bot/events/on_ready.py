import logging
from discord.ext.commands import Bot
if __name__ != '__main__':
    from bot.constants import REACTION_ROLE_CHANNEL_ID, ROLES

def add_on_ready(bot: Bot) -> None:
    async def add_reaction_roles(bot: Bot) -> None:
        channel = bot.get_channel(REACTION_ROLE_CHANNEL_ID)
        await channel.purge() # clear channel
        text= "Reaction Roles:\n\n"
        for role in ROLES.keys():
            text += f"{role}: {ROLES[role]}\n"
        message = await channel.send(text)
        for emoji in ROLES.keys():
            await message.add_reaction(emoji)

    @bot.event
    async def on_ready():
        logging.info('Bot is ready')
        await add_reaction_roles(bot)