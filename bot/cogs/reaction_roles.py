from discord.ext import commands
import logging
from discord.utils import get

if __name__ != '__main__':
    from bot.constants import REACTION_ROLE_CHANNEL_ID, ROLES, POLL_OPTIONS

class ReactionRoles(commands.Cog, name='Reaction Roles'):
    """Manages the addition and removal of reaction roles"""
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     """Add message and reactions to react role channel on bot startup"""
    #     async def add_reaction_roles(bot) -> None:
    #         channel = bot.get_channel(REACTION_ROLE_CHANNEL_ID)
            # await channel.purge() # clear channel
            # text= "Reaction Roles:\n\n"
            # for role in ROLES.keys():
            #     text += f"{role}: {ROLES[role]}\n"
            # message = await channel.send(text)
            # for emoji in ROLES.keys():
            #     await message.add_reaction(emoji)

        # await add_reaction_roles(self.bot)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """When a reaction is added to a message in the react role channel, add role to user"""
        # if message not within react role chat or use is bot return
        channel = self.bot.get_channel(REACTION_ROLE_CHANNEL_ID)
        if reaction.message.channel.id != channel.id:
            return
        if user.bot:
            return
        # check if emoji is in roles, if so add role
        if reaction.emoji in ROLES.keys():
            logging.info(f'{user} reacted to {ROLES[reaction.emoji]} role')
            role = get(user.guild.roles, name=ROLES[reaction.emoji])
            try:
                await user.add_roles(role)
            except AttributeError as e:
                logging.error(e)
                logging.error(f"Check '{ROLES[reaction.emoji]}' role exists in server")
                exit()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """When a reaction is removed from a message in the react role channel, remove role from user"""
        channel = self.bot.get_channel(REACTION_ROLE_CHANNEL_ID)
        if reaction.message.channel.id != channel.id:
            return
        # check if emoji is in roles, if so add role
        if reaction.emoji in ROLES.keys():
            logging.info(f'{user} removed reaction to {ROLES[reaction.emoji]} role')
            role = get(user.guild.roles, name=ROLES[reaction.emoji])
            await user.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))