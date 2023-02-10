from discord.ext import commands
import discord
from random import choice

def get_word() -> str:
    """Get a random word from data/wordle.txt"""
    with open("data/wordle.txt", "r") as f:
        lines = f.readlines()
        return choice(lines).strip()
    
def guess_to_emojis(guess: str, word: str) -> str:
    """Convert a guess to an emoji grid"""
    line = ""
    for expected, actual in zip(guess, word):
        if expected == actual:
            line += ":green_square:"
        elif expected in word:
            line += ":yellow_square:"
        else:
            line += ":black_large_square:"
    return line + '\n'

def available_letters(guesses: str) -> str:
    """Get string of alphabet with unavailable letters with lines through them and all bold"""
    letters = ""
    for letter in "abcdefghijklmnopqrstuvwxyz":
        if letter not in guesses:
            letters += f"**{letter}** "
    return letters.upper()

def create_embed(guesses: str, grid: str) -> discord.Embed:
    """Create an embed for the wordle game"""
    embed = discord.Embed(
        title="Wordle", 
        description=grid + '\n',
        colour=discord.Colour.blue())
    # create list of guesses
    formatted_guesses = ""
    for guess in guesses.split(', '):
        formatted_guesses += f"{guess}\n"
    if len(guesses) != 0:
        embed.add_field(name="Guesses:", value=formatted_guesses, inline=False)
    embed.add_field(name="Available Letters:", value=available_letters(guesses), inline=False)
    embed.set_footer(text="Guess a five letter word with ! prefix (e.g. !hello)")
    return embed

class Wordle(commands.Cog, name='Wordle'):
    """Controls wordle game"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wordle', help='Starts a game of Wordle')
    async def wordle(self, ctx):
        """Starts a game of Wordle, anyone can participate in the channel"""
        check = lambda msg: msg.channel == ctx.channel and msg.content.startswith('!')
        grid, guesses, word = "", "", get_word()
        message = await ctx.send(embed=create_embed(guesses, grid))
        while (guess := (await self.bot.wait_for('message', check=check)).content.lower()[1:]) != word:
            if len(guess) != 5: # end game if not 5 char
                embed = create_embed(guesses, grid)
                embed.add_field(name="You Lose!", value=f"You failed to guess the word '{word}'")
                return await message.edit(embed=embed)
            if len(guesses) != 0: 
                guesses += ', '
            guesses += guess
            grid += guess_to_emojis(guess, word)
            await message.edit(embed=create_embed(guesses, grid))
        grid += ":green_square:" * 5
        embed = create_embed(guesses, grid)
        embed.add_field(name="You Win!", value=f"You guessed the correct word '{word}'!")
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Wordle(bot))