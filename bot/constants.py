PREFIX = '#'

REACTION_CHANNELS = [
    '1071989982924910683',
    '1071669604809711636'
]

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
