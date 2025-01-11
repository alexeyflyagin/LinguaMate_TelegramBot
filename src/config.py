import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT_PATH = Path(__file__).parent.parent
ENV_PATH = ROOT_PATH / '.env'
LOG_FOLDER_PATH = ROOT_PATH / 'logs'

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d - %(message)s"

os.makedirs(LOG_FOLDER_PATH, exist_ok=True)
load_dotenv(ENV_PATH)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DB_URL')

logging.getLogger('aiogram').setLevel(level=logging.WARNING)
logging.getLogger('asyncio').setLevel(level=logging.WARNING)
logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(LOG_FOLDER_PATH / 'app.log')],
)
