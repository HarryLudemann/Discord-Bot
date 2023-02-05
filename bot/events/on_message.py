import logging
from discord.ext.commands import Bot

def add_on_message(bot: Bot) -> None:
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

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        logging.info(f'{message.author} said {message.content}')
        if banned_words_check(message.content.lower()) or banned_sub_words_check(message.content.lower()):
            await message.delete()
        await bot.process_commands(message)
