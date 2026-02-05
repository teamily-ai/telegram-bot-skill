#!/usr/bin/env python3
"""
Send a message with inline keyboard buttons
"""

import asyncio
import sys
import argparse
from telegram_bot import TelegramBotWrapper


async def main():
    """Send message with buttons"""
    parser = argparse.ArgumentParser(description='Send a message with inline buttons')
    parser.add_argument('--chat-id', type=str, help='Target chat ID')
    parser.add_argument('--message', type=str, required=True, help='Message text')
    parser.add_argument('--buttons', type=str, required=True,
                        help='Button labels separated by commas (e.g., "Option 1,Option 2,Option 3")')
    parser.add_argument('--columns', type=int, default=2,
                        help='Number of buttons per row (default: 2)')
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

    # Parse button labels
    button_labels = [label.strip() for label in args.buttons.split(',')]

    # Arrange buttons in rows
    button_rows = []
    for i in range(0, len(button_labels), args.columns):
        row = button_labels[i:i + args.columns]
        button_rows.append(row)

    print(f"📤 Sending message with {len(button_labels)} button(s)...")

    try:
        bot = TelegramBotWrapper()

        # Create inline keyboard
        keyboard = bot.create_inline_keyboard(button_rows)

        # Send message
        result = await bot.send_message(
            text=args.message,
            chat_id=chat_id,
            reply_markup=keyboard
        )

        print(f"✅ Message sent successfully!")
        print(f"   Message ID: {result['message_id']}")
        print(f"   Chat ID: {result['chat_id']}")
        print(f"   Buttons: {', '.join(button_labels)}")

        print("\n💡 Note: To handle button clicks, you need to implement")
        print("   callback query handling in a bot listener script.")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
