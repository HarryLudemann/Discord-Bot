PREFIX = '#'

REACTION_ROLE_CHANNEL_ID = 1071669604809711636
RULES_CHANNEL_ID = 1071989982924910683

ROLES = {
    '✅': 'Verified',
    '👨‍💻': 'Developer',
    '🎨': 'Designer',
    '📖': 'Writer',
    '🎥': 'Video Editor',
    '🎤': 'Voice Actor',
    '🎮': 'Gamer',
    '🎵': 'Musician',
    '📷': 'Photographer',
    '📚': 'Reader',
    '📺': 'Streamer',
    '🌿': 'Stoner'
}

# make partial dict of roles without verified role
EXTRA_ROLES = {key: value for key, value in ROLES.items() if value != 'Verified'}

POLL_OPTIONS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
THUMBS_UP = '👍'
THUMBS_DOWN = '👎'