from discord.ext.commands import Cog, command
import logging
from discord.utils import get
import discord
if __name__ != '__main__':
    from bot.database import ReactionRoleDatabase


class ReactionRoles(Cog, name='Reaction Roles'):
    """Manages the addition and removal of reaction roles"""
    def __init__(self, bot):
        self.bot = bot
        self.__database = ReactionRoleDatabase()

    async def reaction_check(self, guild_id, channel_id, emoji, user):
        """Add role when reaction added"""
        if user.bot:
            return
        role_id = self.__database.check_reaction_role(
            guild_id=str(guild_id),
            channel_id=str(channel_id),
            emoji=str(emoji))
        logging.info(f'Role ID: {role_id}')
        if role_id is not None:
            role = get(self.bot.get_guild(guild_id).roles, id=int(role_id))
            User = self.bot.get_guild(guild_id).get_member(user.id)
            await User.add_roles(role)
            logging.info(f'Added role {role.name} to {user.name}')

    async def reaction_remove_check(self, guild_id, channel_id, emoji, user):
        """Remove role when reaction removed"""
        if user.bot:
            return
        role_id = self.__database.check_reaction_role(
            guild_id=str(guild_id),
            channel_id=str(channel_id),
            emoji=str(emoji))
        if role_id is not None:
            role = get(self.bot.get_guild(guild_id).roles, id=int(role_id))
            User = self.bot.get_guild(guild_id).get_member(user.id)
            await User.remove_roles(role)
            logging.info(f'Removed role {role.name} from {user.name}')

    @Cog.listener()
    async def on_reaction_add(
            self, reaction: discord.Reaction, user: discord.User):
        """On reaction add check if reaction is a reaction role
            and in correct channel, if so add"""
        await self.reaction_check(
            reaction.message.guild.id,
            reaction.message.channel.id,
            reaction.emoji, user)

    @Cog.listener()
    async def on_raw_reaction_add(
            self, payload: discord.RawReactionActionEvent):
        """On raw reaction add check if reaction is a reaction
            role and in correct channel, if so add"""
        await self.reaction_check(
            payload.guild_id,
            payload.channel_id,
            payload.emoji,
            self.bot.get_user(payload.user_id))

    @Cog.listener()
    async def on_reaction_remove(
            self, reaction: discord.Reaction, user: discord.User):
        """On reaction remove check if reaction is a reaction
            role and in correct channel, if so remove"""
        await self.reaction_remove_check(
            reaction.message.guild.id,
            reaction.message.channel.id,
            reaction.emoji, user)

    @Cog.listener()
    async def on_raw_reaction_remove(
            self, payload: discord.RawReactionActionEvent):
        """On raw reaction remove check if reaction is a
            reaction role and in correct channel, if so remove"""
        await self.reaction_remove_check(
            payload.guild_id,
            payload.channel_id,
            payload.emoji,
            self.bot.get_user(payload.user_id))

    @command(name='reactionroles', aliases=['rr'], hidden=True)
    async def list_reaction_roles(self, ctx):
        """List all reaction roles available in server"""
        for role in self.__database.get_reaction_roles(ctx.guild.id):
            logging.info(role)

    @command(name='addreaction', hidden=True)
    async def add_reaction_role(self, ctx, emoji: str, role: discord.Role):
        """Add a reaction role"""
        self.__database.add_reaction_role(
            guild_id=str(ctx.guild.id),
            channel_id=str(ctx.channel.id),
            emoji=emoji,
            role_id=str(role.id))
        logging.info(f'Added reaction role {emoji} {role.name}')
        await ctx.send(f'Added reaction role {emoji} {role.name}')

    @command(name='removereaction', hidden=True)
    async def remove_reaction_role(
            self, ctx, emoji: str, role: discord.Role):
        """Remove a reaction role"""
        self.__database.remove_reaction_role(
            guild_id=str(ctx.guild.id),
            channel_id=str(ctx.channel.id),
            emoji=emoji,
            role_id=str(role.id))
        logging.info(f'Removed reaction role {emoji} {role.name}')
        await ctx.send(f'Removed reaction role {emoji} {role.name}')


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
