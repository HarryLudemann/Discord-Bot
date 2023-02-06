from discord.ext import commands
import logging
if __name__ != '__main__':
    from bot.constants import POLL_OPTIONS, THUMBS_DOWN, THUMBS_UP

class Poll(commands.Cog, name='Poll'):
    """Poll system allowing admin todo polls with 2-9 options"""
    def __init__(self, bot):
        self.bot = bot

    # check admin permissions
    @commands.command(name='poll', help='Given options and question, starts a poll')
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, question: str, *options: str):
        """Given options and question starts a poll, must be administrator.

        Parameters
        ----------
        question : str
            Question to ask
        options : *str
            Options to choose from
        """
        # try delete the message containing the command
        try:
            await ctx.message.delete()
        except Exception as e:
            logging.error(e)
        if len(options) == 0: # if no options, use thumbs up and down
            message = await ctx.channel.send(question)
            await message.add_reaction(THUMBS_UP)
            await message.add_reaction(THUMBS_DOWN)
        elif len(options) < 10 and len(options) > 1: # use count
            for index, option in enumerate(options):
                question += f"\n{index+1}: {option}"
            message = await ctx.channel.send(question)
            for option in POLL_OPTIONS[:len(options)]:
                await message.add_reaction(option)
        logging.info(f"{ctx.author} started a poll in '{ctx.channel}' channel")


async def setup(bot):
    await bot.add_cog(Poll(bot))