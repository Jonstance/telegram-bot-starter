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
        f"**Snowcoin: A Decentralized Ecosystem**\n\n"
        f"Snowcoin is a cutting-edge blockchain project revolutionizing the crypto landscape. Our mission is to create a decentralized ecosystem, empowering individuals to take control of their financial freedom.\n\n"
        f"**SnowDex: A Decentralized Crypto Exchange**\n\n"
        f"At the heart of Snowcoin lies SnowDex, a decentralized crypto exchange built on the latest blockchain technology. SnowDex prioritizes security, transparency, and community governance, ensuring a fair and accessible trading experience for all.\n\n"
        f"**Key Features:**\n\n"
        f"- Decentralized Governance: SnowDex operates on a decentralized network, allowing the community to drive decision-making and development.\n"
        f"- Security: Multi-layered security measures protect users' assets and data.\n"
        f"- Transparency: Real-time market data, transparent order books, and open-source smart contracts ensure a trustworthy trading environment.\n"
        f"- Community-Driven: SnowDex is built by the community, for the community, with user feedback shaping our development roadmap.\n"
        f"- Multi-Asset Support: Trade a diverse range of cryptocurrencies, with more assets added based on community demand.\n"
        f"- Liquidity Incentives: SnowDex rewards liquidity providers, ensuring a stable and liquid market.\n"
        f"- User-Friendly Interface: Seamlessly navigate SnowDex's intuitive design, making it easy for beginners and experienced traders alike.\n\n"
        f"**Join the Snowcoin and SnowDex Community Today!**\n\n"
        f"Participate in a revolutionary decentralized exchange that prioritizes user needs and empowers financial freedom. Engage with our community, contribute to our growth, and shape the future of SnowDex!\n\n"
        f"Hello {user.first_name}! Click the button below to open the mini app.",
        reply_markup=reply_markup,
        parse_mode='Markdown'  # Use Markdown for formatting
    )
    """Send a message with an inline button when the command /start is issued."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Define the inline keyboard button
    keyboard = [
        [InlineKeyboardButton("Start now!", web_app={
            "url": "https://bot.snowdex.org"  # Replace with your actual mini app URL
        })],
        [InlineKeyboardButton("Join Telegram Channel", url="https://t.me/snowcoin_App")],  # Replace with your channel URL
        [InlineKeyboardButton("Follow on X", url="https://x.com/Snowcoin_App?t=JQJpsFgQuZRIo1qMP3Tmig&s=09")]  # Replace with your Twitter URL
   

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the message with the inline button
    await update.message.reply_text(
        f"Hello {user.first_name}! Welcome to the bot. Click the button below to open the mini app.",
        reply_markup=reply_markup
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
