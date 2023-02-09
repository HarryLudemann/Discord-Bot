import discord
from discord.ext import commands
from discord import app_commands
import os
import logging
import logging.handlers
if __name__ != '__main__':
    from bot.constants import BOT_TOKEN, PREFIX

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX), 
            intents=discord.Intents.all(),
            case_insensitive=True)
        
    async def setup_hook(self) -> None:
        """Load all cogs in bot/cogs"""
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"bot.cogs.{filename[:-3]}")


def start() -> None:
    discord.utils.setup_logging(level=logging.INFO)
    Bot().run(BOT_TOKEN)
