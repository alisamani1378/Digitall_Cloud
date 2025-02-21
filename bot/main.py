import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from services.db import create_tables, save_user_to_db, get_all_products

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user_to_db(
        telegram_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )
    await update.message.reply_text("Welcome to the shop bot!")

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_all_products()  # list of tuples: (id, title, price)

    if not products:
        await update.message.reply_text("No products available.")
        return

    text = "Available Products:\n\n"
    for p in products:
        product_id, title, price = p
        text += f"{product_id}. {title} - ${price}\n"

    await update.message.reply_text(text)

def main():
    create_tables()
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("TELEGRAM_TOKEN not found")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("products", products_command))

    application.run_polling()

if __name__ == "__main__":
    main()
