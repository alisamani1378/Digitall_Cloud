import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from services.db import create_tables, save_user_to_db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Save or update user info in the database
    save_user_to_db(
        telegram_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )

    await update.message.reply_text("Welcome to the shop bot!")

def main():
    # Create or update database tables
    create_tables()

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("TELEGRAM_TOKEN not found in environment")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))

    application.run_polling()

if __name__ == "__main__":
    main()
