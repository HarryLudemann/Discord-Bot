from discord.ext.commands import Cog, check
import logging
from discord.utils import get
import discord
if __name__ != '__main__':
    from bot.constants import REACTION_ROLE_CHANNEL_ID, EXTRA_ROLES, RULES_CHANNEL_ID, ROLES


def react_role_embed() -> discord.Embed:
    """Returns embed of formatted reaction roles"""
    embed = discord.Embed(
        title="Reaction Roles",
        description="React to this message to get a role",
        colour=discord.Colour.blue()
    )
    embed.set_footer(text="React to this message to get a role")
    text= ""
    for role in EXTRA_ROLES.keys():
        if role != 'Verified':
            text += f"{role} {EXTRA_ROLES[role]}\n"
    embed.add_field(name="Roles", value=text, inline=False)
    return embed

async def is_appropriate_channel(ctx: discord.ext.commands.Context) -> bool:
    """Check if the channel is the react or rule channel"""
    if ctx.channel.id == REACTION_ROLE_CHANNEL_ID: return True
    elif ctx.channel.id == RULES_CHANNEL_ID: return True
    return False

class ReactionRoles(Cog, name='Reaction Roles'):
    """Manages the addition and removal of reaction roles"""
    def __init__(self, bot):
        self.bot = bot

    # @Cog.listener()
    # async def on_ready(self):
    #     """Reset react role message"""
    #     channel = self.bot.get_channel(REACTION_ROLE_CHANNEL_ID)
    #     await channel.purge()
    #     message = await channel.send(embed= react_role_embed())
    #     for emoji in EXTRA_ROLES.keys():
    #         await message.add_reaction(emoji)
    
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