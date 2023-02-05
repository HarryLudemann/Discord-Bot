import logging
from discord.ext.commands import Bot
import discord
if __name__ != '__main__':
    from bot.constants import REACTION_ROLE_CHANNEL_ID, ROLES

def add_on_reaction_add(bot: Bot) -> None:
    @bot.event
    async def on_reaction_add(reaction, user):
        channel = bot.get_channel(REACTION_ROLE_CHANNEL_ID)
        if reaction.message.channel.id != channel.id:
            return
        if user.bot:
            return
        # check if emoji is in roles, if so add role
        if reaction.emoji in ROLES.keys():
            logging.info(f'{user} reacted to {ROLES[reaction.emoji]} role')
            role = discord.utils.get(user.guild.roles, name=ROLES[reaction.emoji])
            try:
                await user.add_roles(role)
            except AttributeError as e:
                logging.error(e)
                logging.error(f"Check '{ROLES[reaction.emoji]}' role exists in server")
                exit()