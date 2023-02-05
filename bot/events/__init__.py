from bot.events.on_message import add_on_message
from bot.events.on_ready import add_on_ready
from bot.events.on_reaction_add import add_on_reaction_add
from bot.events.on_reaction_remove import add_on_reaction_remove
from bot.events.on_member_join import add_on_member_join
from bot.events.on_member_remove import add_on_member_remove


__all__ = [
    'add_on_message',
    'add_on_ready',
    'add_on_reaction_add',
    'add_on_reaction_remove',
    'add_on_member_join',
    'add_on_member_remove',
    ]