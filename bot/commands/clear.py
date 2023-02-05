from discord.ext import commands
import logging

@commands.command(name='clear', help='Clears messages in channel')
async def clear(ctx):
    if not ctx.author.guild_permissions.administrator:
        return
    await ctx.channel.purge()
    logging.info(f'{ctx.author} cleared messages in {ctx.channel} channel')