import discord
from discord.ext.commands import Bot, when_mentioned_or
import os
import logging
if __name__ != '__main__':
    from bot.constants import BOT_TOKEN, PREFIX

class Bot(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=when_mentioned_or(PREFIX), 
            intents=discord.Intents.all(),
            case_insensitive=True)
        discord.utils.setup_logging(level=logging.INFO)
        
    async def setup_hook(self) -> None:
        """Load all cogs in bot/cogs"""
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"bot.cogs.{filename[:-3]}")

    # create partial function of run with token set
    def run(self) -> None:
        super().run(BOT_TOKEN)
