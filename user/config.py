import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("bot_token")
BOT_NAME = os.getenv("bot_name")
ADMIN_ID = int(os.getenv("admin_id", 0))
DB_PATH = os.getenv("db_path")
BONUS_AMOUNT = os.getenv("bonus_amount")