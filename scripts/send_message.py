#!/usr/bin/env python3
"""
Send a text message via Telegram Bot
Supports sending to specific chat ID or using default
"""

import asyncio
import sys
import argparse
from telegram.constants import ParseMode
from telegram_bot import TelegramBotWrapper


async def main():
    """Send message"""
    parser = argparse.ArgumentParser(description='Send a Telegram message')
    parser.add_argument('--chat-id', type=str, help='Target chat ID')
    parser.add_argument('--username', type=str, help='Target username (not supported directly, use chat-id)')
    parser.add_argument('--message', type=str, required=True, help='Message text')
    parser.add_argument('--format', type=str, choices=['markdown', 'html', 'none'],
                        default='none', help='Message format')
    parser.add_argument('--use-default', action='store_true',
                        help='Use default chat ID from .env')

    args = parser.parse_args()

    # Determine parse mode
    parse_mode = None
    if args.format == 'markdown':
        parse_mode = ParseMode.MARKDOWN_V2
    elif args.format == 'html':
        parse_mode = ParseMode.HTML

    # Determine chat ID
    chat_id = None
    if args.use_default:
        chat_id = None  # Will use default from bot wrapper
    elif args.chat_id:
        chat_id = args.chat_id
    elif args.username:
        print("❌ Username lookup not supported. Please use --chat-id instead.")
        print("💡 Tip: Run 'python scripts/list_chats.py' to find chat IDs")
        sys.exit(1)

    if not args.use_default and not chat_id:
        print("❌ Please specify --chat-id or --use-default")
        sys.exit(1)

    print(f"📤 Sending message...")

    try:
        bot = TelegramBotWrapper()
        result = await bot.send_message(
            text=args.message,
            chat_id=chat_id,
            parse_mode=parse_mode
        )

        print(f"✅ Message sent successfully!")
        print(f"   Message ID: {result['message_id']}")
        print(f"   Chat ID: {result['chat_id']}")
        print(f"   Time: {result['date']}")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
