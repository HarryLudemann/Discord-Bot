from discord.ext import commands
import logging

class MessageFilter(commands.Cog, name='Message Filter'):
    """Remove messages that contain profanity or websites"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        def banned_words_check(text: str) -> bool:
            """Check bad-words.txt for profanity in text"""
            with open('banned-words.txt', 'r') as f:
                banned_words = f.read().splitlines()
            words = text.split()
            for word in words:
                if word in banned_words:
                    return True
            return False
        
        def banned_sub_words_check(text: str) -> bool:
            """Check website-identifies.txt for features in text"""
            with open('banned-sub-words.txt', 'r') as f:
                banned_sub_words = f.read().splitlines()
            for identifier in banned_sub_words:
                if identifier in text:
                    return True 
            return False
    
        # if message is from bot, ignore
        if message.author == self.bot.user:
            return
        if banned_words_check(message.content.lower()) or banned_sub_words_check(message.content.lower()):
            await message.delete()
            logging.warning(f'{message.author} said banned content {message.content}')

async def setup(bot):
    await bot.add_cog(MessageFilter(bot))