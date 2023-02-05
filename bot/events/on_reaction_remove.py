import logging
from discord.ext.commands import Bot
import discord
if __name__ != '__main__':
    from bot.constants import REACTION_ROLE_CHANNEL_ID, ROLES

def add_on_reaction_remove(bot: Bot) -> None:
    @bot.event
    async def on_reaction_remove(reaction, user):
        channel = bot.get_channel(REACTION_ROLE_CHANNEL_ID)
        if reaction.message.channel.id != channel.id:
            return
        # check if emoji is in roles, if so add role
        if reaction.emoji in ROLES.keys():
            logging.info(f'{user} removed reaction to {ROLES[reaction.emoji]} role')
            role = discord.utils.get(user.guild.roles, name=ROLES[reaction.emoji])
            await user.remove_roles(role)