from discord.ext.commands import Cog, command
from discord import Embed, Colour, Member
from random import choice

def get_joke() -> str:
    """Get a random joke from the jokes.txt file"""
    with open('data/dad-jokes.txt', 'r', encoding="utf8") as f:
        jokes = f.read().splitlines()
    joke = choice(jokes).split('<>')
    return joke[0], joke[1]

def get_comeback(name: str) -> str:
    """Get a random comeback from the comebacks.txt file"""
    with open('data/comebacks.txt', 'r', encoding="utf8") as f:
        comebacks = f.read().splitlines()
    return choice(comebacks)

class Jokes(Cog, name='Jokes'):
    """Contains joke commands"""
    def __init__(self, bot):
        self.bot = bot

    @command(name='joke', help='Get a random dad joke')
    async def joke(self, ctx):
        """Get a random dad joke, hide the punchline in an embed"""
        joke, punchline = get_joke()
        embed = Embed(
            title=joke,
            description='||' + punchline + '||',
            color=Colour.blue())
        await ctx.send(embed=embed)

    @command(name='comeback', help='Get a random crude comeback R18')
    async def comeback(self, ctx, member: Member):
        """Get a random comeback, mention the user"""
        await ctx.send(f"{member.mention} {get_comeback(member.name)}")


async def setup(bot):
    await bot.add_cog(Jokes(bot))