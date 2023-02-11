import discord
from discord.ext.commands import Bot, when_mentioned_or, command, has_permissions
import os
import logging
from dotenv import load_dotenv
if __name__ != '__main__':
    from bot.database import PrefixDatabase

class Bot(Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=when_mentioned_or(self.get_prefix), 
            intents=discord.Intents.all(),
            case_insensitive=True)
        discord.utils.setup_logging(level=logging.INFO)
        load_dotenv()
        self.__database = PrefixDatabase()

    def get_prefix(self, message): 
        return self.__database.get_prefix(message.guild.id)
        
    async def setup_hook(self) -> None:
        """Load all cogs in bot/cogs"""
        for filename in os.listdir("bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"bot.cogs.{filename[:-3]}")

    def run(self) -> None:
        super().run(os.getenv('BOT_TOKEN'))