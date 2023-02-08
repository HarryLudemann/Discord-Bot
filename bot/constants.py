from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')


REACTION_ROLE_CHANNEL_ID = 1071669604809711636

ROLES = {
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

POLL_OPTIONS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
THUMBS_UP = '👍'
THUMBS_DOWN = '👎'