#!/usr/bin/env python3
"""
Send a text message via Telegram Bot
Supports sending by chat ID, contact name, or using default
"""

import asyncio
import sys
import argparse
from telegram.constants import ParseMode
from telegram_bot import TelegramBotWrapper
from contacts import ContactManager


async def main():
    """Send message"""
    parser = argparse.ArgumentParser(description='Send a Telegram message')
    parser.add_argument('--to', type=str, help='Contact name or chat ID')
    parser.add_argument('--chat-id', type=str, help='Target chat ID (deprecated, use --to)')
    parser.add_argument('--message', '-m', type=str, required=True, help='Message text')
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
    contact_name = None

    if args.use_default:
        chat_id = None  # Will use default from bot wrapper
    elif args.to:
        # Check if it's a chat ID (numeric or starts with -)
        if args.to.lstrip('-').isdigit():
            chat_id = args.to
        else:
            # Treat as contact name
            contact_name = args.to
            manager = ContactManager()
            chat_id = manager.get_chat_id(contact_name)

            if chat_id is None:
                print(f"❌ Contact not found: {contact_name}")
                print("\n💡 Available contacts:")
                contacts = manager.list_all()
                if contacts:
                    for contact in contacts[:5]:
                        print(f"   - {contact['name']}")
                    if len(contacts) > 5:
                        print(f"   ... and {len(contacts) - 5} more")
                else:
                    print("   (none)")
                print("\n💡 Import contacts: python scripts/contacts.py import")
                print("💡 Add contact: python scripts/contacts.py add <name> <chat_id>")
                sys.exit(1)
    elif args.chat_id:
        # Legacy support
        chat_id = args.chat_id

    if not args.use_default and not chat_id:
        print("❌ Please specify --to <name|chat_id> or --use-default")
        print("\n💡 Examples:")
        print("   python scripts/send_message.py --to John -m 'Hello!'")
        print("   python scripts/send_message.py --to 123456789 -m 'Hello!'")
        print("   python scripts/send_message.py --use-default -m 'Hello!'")
        sys.exit(1)

    if contact_name:
        print(f"📤 Sending message to {contact_name}...")
    else:
        print(f"📤 Sending message...")

    try:
        bot = TelegramBotWrapper()
        result = await bot.send_message(
            text=args.message,
            chat_id=chat_id,
            parse_mode=parse_mode
        )

        print(f"✅ Message sent successfully!")
        if contact_name:
            print(f"   To: {contact_name}")
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
