from discord.ext.commands import Cog, command, has_permissions, MemberConverter
import discord
import logging
from typing import Optional
from random import choice

def get_rules_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Hazzah's Server Rules",
        description="We have a small but strict set of rules on our server. Please read over them and take them on board. If you don't understand a rule or need to report an incident, please send a direct message to @admin",
        colour=discord.Colour.blue()
    )
    embed.add_field(name="Rule 1", value="Follow the [Discord Community Guidelines](https://discordapp.com/guidelines) and [Terms of Service](https://discordapp.com/terms)", inline=False)
    embed.add_field(name="Rule 2", value="Respect staff members and listen to their instructions.", inline=False)
    embed.add_field(name="Rule 3", value="Use English to the best of your ability. Be polite if someone speaks English imperfectly.", inline=False)
    embed.add_field(name="Rule 4", value="Do not provide or request help on projects that may break laws, breach terms of services, or are malicious or inappropriate.", inline=False)
    embed.add_field(name="Rule 5", value="Do not post unapproved advertising.", inline=False)
    embed.add_field(name="Rule 6", value="Keep discussions relevant to the channel topic. Each channel's description tells you the topic.", inline=False)
    embed.add_field(name="Rule 7", value="Do not help with ongoing exams. When helping with homework, help people learn how to do the assignment without doing it for them.", inline=False)
    embed.add_field(name="Rule 8", value="Do not offer or ask for paid work of any kind.", inline=False)
    return embed

def get_name_policy_embed() -> discord.Embed:
    embed = discord.Embed(
        title = "Name & Profile Policy",
        description="In order to keep things pleasant and workable for both users and staff members, we enforce the following requirements regarding your name, avatar, and profile. Staff reserve the right to change any nickname we judge to be violating these requirements. \n\nWe also reserve the right to enforce compliance of hateful or otherwise inappropriate usernames and profiles regardless of the server-specific nickname or profile.",
        colour=discord.Colour.blue()
    )
    embed.add_field(name="Rule 1", value="No blank or 'invisible' names.", inline=False)
    embed.add_field(name="Rule 2", value="No slurs or other offensive sentiments or imagery.", inline=False)
    embed.add_field(name="Rule 3", value="No noisy unicode characters (for example z̯̯͡a̧͎̺l̡͓̫g̹̲o̡̼̘) or rapidly flashing avatars.", inline=False)
    return embed

class Server(Cog, name='Server'):
    """Basic server commands and events"""
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        logging.info('Bot is ready')
        rules_channel = self.bot.get_channel(1071989982924910683) 
        await rules_channel.purge()
        message = await rules_channel.send(embed=get_rules_embed())
        await rules_channel.send(embed=get_name_policy_embed())
        await message.add_reaction('✅')

    @Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
        logging.info(f'{member} joined the server')
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to my Discord server!')

    @Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            logging.info(f'{message.author} said {message.content}')
    
    @command(name='setprefix', help='Sets the bot\'s prefix', hidden=True)
    async def setprefix(self, ctx, prefix):
        self.bot.command_prefix = prefix
        await ctx.send("Prefixes set!")

    @command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: list):
        """Chooses between multiple choices."""
        await ctx.send("I choose '{}'".format(''.join(choice(choices))))

    @command(name='kick', help='Kicks a member from the server', hidden=True)
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: MemberConverter, *, reason: Optional[str] = None):
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

    @command(name='ban', help='Bans a member from the server', hidden=True)
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberConverter, *, reason: Optional[str] = None):
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