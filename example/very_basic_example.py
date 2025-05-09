import logging
import os
import json
from dotenv import load_dotenv

# Import the unified logger
from teletracker import UnifiedTgLogger

load_dotenv(".env",override=True)  # Load environment variables from .env file
TELEGRAM_TOKEN: str = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID: list = json.loads(os.environ.get("TELEGRAM_CHAT_ID", "[]"))
SERVER_NAME: str = os.environ.get("SERVER_NAME", "❎localhost")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    print("Please set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID environment variables or replace placeholders in the script.")
    exit()

# --- Setup Unified Logger ---

# Get the root logger or a specific logger
logger = logging.getLogger(__name__) # Use __name__ or a specific name like 'my_app'
logger.setLevel(logging.INFO) # Set desired level for console/file output

# Create formatter
formatter = logging.Formatter(
    f'%(asctime)s - {SERVER_NAME} - %(name)s - %(levelname)s : %(message)s',
    datefmt='%d-%m %H:%M'
)

# Optional: Add a console handler to see logs locally as well
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create and add the UnifiedTgLogger handler
# This handler will send logs >= INFO to Telegram
tg_handler = UnifiedTgLogger(token=TELEGRAM_TOKEN, users=TELEGRAM_CHAT_ID)
tg_handler.setLevel(logging.INFO) # Set level specifically for Telegram logs
tg_handler.setFormatter(formatter) # Use the same formatter or a different one
logger.addHandler(tg_handler)


if __name__ == "__main__":
    print("Starting UnifiedTgLogger demo...")
    # --- Logging example ---
    logger.info("Hello from UnifiedTgLogger (INFO log)")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    try:
        1/0
    except Exception as ex:
        logger.exception("exception-message")
