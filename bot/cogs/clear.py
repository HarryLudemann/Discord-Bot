from discord.ext.commands import Cog, command
import logging
from typing import Optional

class Clear(Cog, name='Clear'):
    """Clear messages in channel command"""
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases = ["cls"], help="Clears messages in channel, only for administrators")
    async def clear(self, ctx, *args):
        """Clears messages in channel, only for administrators.

        Parameters
        ----------
        args : *args
            Optionally give number to set max number of messages to delete, 
            and optionally a player name as a 3rd argument to delete messages from
        """
        def int_check(number: str) -> Optional[int]:
            """Check if number is a valid integer, returned number but can be None"""
            try:
                return int(number)
            except ValueError:
                return None
        
        if len(args) > 0 and (number := int_check(args[0])):
            try:
                if len(args) == 1: # if passed number to set limit
                    await ctx.channel.purge(limit=number)
                    logging.info(f"{ctx.author} cleared up to {number} messages in '{ctx.channel}' channel")
                elif len(args) == 2: # if a third arg, remove messages with player name
                    await ctx.channel.purge(limit=number, check=lambda m: m.author.name == args[1])
                    logging.info(f"{ctx.author} cleared up to {number} messages from {args[1]} in '{ctx.channel}' channel")
            except Exception as e:
                logging.error(e)
                logging.error(f"Check '{number}' is a valid integer")
            return
        await ctx.channel.purge()
        logging.info(f"{ctx.author} cleared messages in '{ctx.channel}' channel")

async def setup(bot):
    await bot.add_cog(Clear(bot))