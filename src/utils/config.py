import os
from pathlib import Path
from dotenv import load_dotenv

root = Path(__file__).resolve().parents[2]
env_path = root / '.env'
if env_path.exists():
    load_dotenv(env_path)

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TWITTER_BEARER = os.environ.get('TWITTER_BEARER')
PUSHSHIFT_KEY = os.environ.get('PUSHSHIFT_KEY')
