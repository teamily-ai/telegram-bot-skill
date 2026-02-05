#!/usr/bin/env python3
"""
Send a file/document via Telegram Bot
"""

import asyncio
import sys
import argparse
from pathlib import Path
from telegram_bot import TelegramBotWrapper


async def main():
    """Send file"""
    parser = argparse.ArgumentParser(description='Send a file via Telegram')
    parser.add_argument('--chat-id', type=str, help='Target chat ID')
    parser.add_argument('--file', type=str, required=True, help='Path to file')
    parser.add_argument('--caption', type=str, help='File caption/description')
    parser.add_argument('--use-default', action='store_true',
                        help='Use default chat ID from .env')

    args = parser.parse_args()

    # Determine chat ID
    chat_id = None
    if args.use_default:
        chat_id = None  # Will use default from bot wrapper
    elif args.chat_id:
        chat_id = args.chat_id

    if not args.use_default and not chat_id:
        print("❌ Please specify --chat-id or --use-default")
        sys.exit(1)

    # Verify file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    # Get file size
    file_size = file_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    if file_size_mb > 50:
        print(f"⚠️  Warning: File is {file_size_mb:.2f} MB")
        print("   Telegram bot API has a 50 MB file size limit")
        print("   Consider using a file hosting service for larger files")

    print(f"📤 Sending file: {file_path.name} ({file_size_mb:.2f} MB)...")

    try:
        bot = TelegramBotWrapper()
        result = await bot.send_document(
            document_path=str(file_path),
            chat_id=chat_id,
            caption=args.caption
        )

        print(f"✅ File sent successfully!")
        print(f"   Message ID: {result['message_id']}")
        print(f"   Chat ID: {result['chat_id']}")
        print(f"   Time: {result['date']}")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to send file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
