#!/usr/bin/env python3
"""
Send a photo via Telegram Bot
"""

import asyncio
import sys
import argparse
from pathlib import Path
from telegram_bot import TelegramBotWrapper


async def main():
    """Send photo"""
    parser = argparse.ArgumentParser(description='Send a photo via Telegram')
    parser.add_argument('--chat-id', type=str, help='Target chat ID')
    parser.add_argument('--photo', type=str, required=True, help='Path to photo')
    parser.add_argument('--caption', type=str, help='Photo caption')
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
    photo_path = Path(args.photo)
    if not photo_path.exists():
        print(f"❌ Photo not found: {args.photo}")
        sys.exit(1)

    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    if photo_path.suffix.lower() not in valid_extensions:
        print(f"⚠️  Warning: {photo_path.suffix} might not be a valid image format")
        print(f"   Valid formats: {', '.join(valid_extensions)}")

    # Get file size
    file_size = photo_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    if file_size_mb > 10:
        print(f"⚠️  Warning: Photo is {file_size_mb:.2f} MB")
        print("   Telegram recommends photos under 10 MB for best quality")

    print(f"📤 Sending photo: {photo_path.name}...")

    try:
        bot = TelegramBotWrapper()
        result = await bot.send_photo(
            photo_path=str(photo_path),
            chat_id=chat_id,
            caption=args.caption
        )

        print(f"✅ Photo sent successfully!")
        print(f"   Message ID: {result['message_id']}")
        print(f"   Chat ID: {result['chat_id']}")
        print(f"   Time: {result['date']}")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to send photo: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
