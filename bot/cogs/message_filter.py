from discord.ext.commands import Cog, command
import logging
import discord
if __name__ != '__main__':
    from bot.database import BannedWordsDatabase

class MessageFilter(Cog, name='Message Filter'):
    """Remove messages that contain profanity or websites"""
    def __init__(self, bot):
        self.bot = bot
        self.__database = BannedWordsDatabase()

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if self.__database.check_message(message.guild.id, message.content):
            await message.delete()
            logging.warning(f'{message.author} said banned content {message.content}')
    
    @command(name='addbannedword', hidden=True)
    async def add_banned_word(self, ctx, word: str):
        self.__database.add_word(ctx.guild.id, word)
        await ctx.send(f"Added '{word}' to banned words")

    @command(name='removebannedword', hidden=True)
    async def remove_banned_word(self, ctx, word: str):
        self.__database.remove_word(ctx.guild.id, word)
        await ctx.send(f"Removed '{word}' from banned words")

    @command(name='listbannedwords', aliases=['bannedwordslist'], hidden=True)
    async def list_banned_words(self, ctx):
        await ctx.send(embed=discord.Embed(
                title='Banned Words', 
                description=self.__database.list_to_string(
                    self.__database.get_words(ctx.guild.id), '\n', True)))


async def setup(bot):
    await bot.add_cog(MessageFilter(bot))