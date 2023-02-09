from discord.ext import commands
from random import choice

def get_word() -> str:
    """Get a random word from data/wordle.txt"""
    with open("data/wordle.txt", "r") as f:
        lines = f.readlines()
        return choice(lines).strip()

class Wordle(commands.Cog, name='Wordle'):
    """Controls wordle game"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wordle', help='Starts a game of Wordle')
    async def _wordle(self, ctx):
        new_word = get_word()
        await ctx.send("Started a game of Wordle. Make a guess!")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        grid = ""
        while (guess := (await self.bot.wait_for('message', check=check)).content.lower()) != new_word:
            line = ""
            if len(guess) != 5:
                await ctx.send("Bad guess, Try again.")
                return
            else:
                for expected, actual in zip(guess, new_word):
                    if expected == actual:
                        line += ":green_square:"
                    elif expected in new_word:
                        line += ":yellow_square:"
                    else:
                        line += ":black_large_square:"
                grid += f"{line}\n"
                await ctx.send(line)
        grid += ":green_square:" * 5
        
        await ctx.send(grid)


async def setup(bot):
    await bot.add_cog(Wordle(bot))