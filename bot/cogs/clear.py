from discord.ext.commands import Cog, command
import logging
from typing import Optional


def int_check(number: str) -> Optional[int]:
    """Check if number is a valid integer, returned number but can be None"""
    try:
        return int(number)
    except ValueError:
        return None


class Clear(Cog, name='Clear'):
    """Clear messages in channel command"""
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases=["cls"], hidden=True)
    async def clear(self, ctx, *args):
        """Clears messages in channel, only for administrators.

        Parameters
        ----------
        args : *args
            Optionally give number to set max number of messages to delete,
            and optionally a player name as a 3rd argument to delete
            messages from
        """
        # if arg and first is valid int
        if len(args) > 0 and (number := int_check(args[0])):
            try:
                # if passed number to set limit
                if len(args) == 1:
                    await ctx.channel.purge(limit=number+1)
                    logging.info(
                        f"{ctx.author} cleared {number} messages")
                # if a third arg, remove messages with player name
                elif len(args) == 2:
                    await ctx.channel.purge(
                        limit=number+1,
                        check=lambda m: m.author.name == args[1])
                    logging.info(
                        f"{ctx.author} cleared {number} messages")
            except Exception as e:
                logging.error(e)
                logging.error(f"Check '{number}' is a valid integer")
            return
        await ctx.channel.purge()
        logging.info(
            f"{ctx.author} cleared messages in '{ctx.channel}' channel")


async def setup(bot):
    await bot.add_cog(Clear(bot))
