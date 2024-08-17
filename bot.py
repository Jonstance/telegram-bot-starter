#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with inline buttons when the command /start is issued."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Define the inline keyboard buttons
    keyboard = [
        [InlineKeyboardButton("Start now!", web_app={
            "url": "https://bot.snowdex.org"  # Replace with your actual mini app URL
        })],
        [InlineKeyboardButton("Join Telegram Channel", url="https://t.me/snowcoin_App")],  # Replace with your channel URL
        [InlineKeyboardButton("Follow on X", url="https://x.com/Snowcoin_App?t=JQJpsFgQuZRIo1qMP3Tmig&s=09")]  # Replace with your Twitter URL
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the message with the inline buttons
    await update.message.reply_text(
        f"SnowCoin is a cutting-edge, decentralized network that revolutionises the crypto landscape, launching on the Ice Open network.\n\n"
        f"As a fast and reliable cryptocurrency, SnowCoin prioritises security, transparency, and community governance, ensuring a trustworthy and accessible environment for all users. With its decentralised governance and multi-layered security measures, SnowCoin provides a robust foundation for SnowDex, its native decentralised crypto exchange. \n\n"
        f"Join the SnowCoin and SnowDex community today and be part of a revolutionary decentralised exchange that prioritises user needs and empowers financial freedom!\n\n"
        f"JOIN THE REVOLUTION, START MINING SNOWCOIN TODAY!"
        f"Hello {user.first_name}! Click the button below to start earning .",
        reply_markup=reply_markup,
        parse_mode='Markdown'  # Use Markdown for formatting
    )
    

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    load_dotenv()

    token = os.getenv("TOKEN")
    if not token:
        logger.error("TOKEN environment variable not set")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
