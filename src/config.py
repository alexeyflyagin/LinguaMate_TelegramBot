import os
from pathlib import Path
from dotenv import load_dotenv


ROOT_PATH = Path(__file__).parent.parent
ENV_PATH = ROOT_PATH / '.env'

load_dotenv(ENV_PATH)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DB_URL')
