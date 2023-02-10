from discord.ext.commands import Cog, check
import logging
from discord.utils import get
import discord
if __name__ != '__main__':
    from bot.constants import EXTRA_ROLES, ROLES, REACTION_CHANNELS

async def is_appropriate_channel(ctx: discord.ext.commands.Context) -> bool:
    """Check if the channel is the react or rule channel"""
    if ctx.channel.id in REACTION_CHANNELS:
        return True
    return False

class ReactionRoles(Cog, name='Reaction Roles'):
    """Manages the addition and removal of reaction roles"""
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    @check(is_appropriate_channel)
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Add role when reaction added"""
        if user.bot: return
        if reaction.emoji in ROLES.keys():
            logging.info(f'{user} reacted to {ROLES[reaction.emoji]} role')
            role = get(user.guild.roles, name=ROLES[reaction.emoji])
            try:
                await user.add_roles(role)
            except AttributeError as e:
                logging.error(e)
                logging.error(f"Check '{ROLES[reaction.emoji]}' role exists in server")
                exit()

    @Cog.listener()
    @check(is_appropriate_channel)
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        """Remove role if reaction removed"""
        if user.bot: return
        if reaction.emoji in ROLES.keys():
            logging.info(f'{user} removed reaction to {ROLES[reaction.emoji]} role')
            role = get(user.guild.roles, name=ROLES[reaction.emoji])
            await user.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))