from discord.ext import commands
import logging
from typing import Optional
from random import choice

class Server(commands.Cog, name='Server'):
    """Basic server commands and events"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
        logging.info(f'{member} joined the server')
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Goodbye {member.mention}.')
        logging.info(f'{member} left the server')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            logging.info(f'{message.author} said {message.content}')
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Bot is ready')

    
    @commands.command(name='setprefix', help='Sets the bot\'s prefix', hidden=True)
    async def setprefix(self, ctx, prefix):
        self.bot.command_prefix = prefix
        await ctx.send("Prefixes set!")

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(choice(choices))

    @commands.command(name='kick', help='Kicks a member from the server', hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason: Optional[str] = None):
        """Kicks a member from the server, must have kick_members permission.

        Parameters
        ----------
        member : commands.MemberConverter
            Member to kick
        reason : Optional[str]
            Reason for kicking member
        """
        await member.kick(reason=reason)
        logging.info(f'{ctx.author} kicked {member} from the server')
        await ctx.send(f'{member} was kicked from the server')

    @commands.command(name='ban', help='Bans a member from the server', hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason: Optional[str] = None):
        """Bans a member from the server, must have ban_members permission.

        Parameters
        ----------
        member : commands.MemberConverter
            Member to ban
        reason : Optional[str]
            Reason for banning member
        """
        await member.ban(reason=reason)
        logging.info(f'{ctx.author} banned {member} from the server')
        await ctx.send(f'{member} was banned from the server')

async def setup(bot):
    await bot.add_cog(Server(bot))