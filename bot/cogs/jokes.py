from discord.ext.commands import Cog, command
from discord import Embed, Colour
from random import choice


def get_dad_joke() -> str:
    """Get a random joke from the jokes.txt file"""
    with open('data/dad-jokes.txt', 'r', encoding="utf8") as f:
        jokes = f.read().splitlines()
    joke = choice(jokes).split('<>')
    return joke[0], joke[1]


class Jokes(Cog, name='Jokes'):
    """Contains joke commands"""
    def __init__(self, bot):
        self.bot = bot

    @command(name='joke', help='Get a random dad joke')
    async def joke(self, ctx):
        """Get a random dad joke, hide the punchline in an embed"""
        joke, punchline = get_dad_joke()
        embed = Embed(
            title=joke,
            description='||' + punchline + '||',
            color=Colour.blue())
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Jokes(bot))
