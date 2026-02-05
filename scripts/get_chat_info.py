#!/usr/bin/env python3
"""
Get information about a specific chat
"""

import asyncio
import sys
import argparse
from telegram_bot import TelegramBotWrapper


async def main():
    """Get chat information"""
    parser = argparse.ArgumentParser(description='Get chat information')
    parser.add_argument('--chat-id', type=str, required=True, help='Chat ID to query')

    args = parser.parse_args()

    print(f"🔍 Fetching information for chat {args.chat_id}...\n")

    try:
        bot = TelegramBotWrapper()
        info = await bot.get_chat(args.chat_id)

        print("✅ Chat Information:\n")
        print(f"   Chat ID: {info['id']}")
        print(f"   Type: {info['type']}")

        if info['type'] == 'private':
            print(f"   First Name: {info.get('first_name', 'N/A')}")
            print(f"   Last Name: {info.get('last_name', 'N/A')}")
            if info.get('username'):
                print(f"   Username: @{info['username']}")
        elif info['type'] in ['group', 'supergroup', 'channel']:
            print(f"   Title: {info.get('title', 'N/A')}")
            if info.get('username'):
                print(f"   Username: @{info['username']}")
            if info.get('description'):
                print(f"   Description: {info['description']}")

        print("\n💡 To send a message to this chat:")
        print(f"   python scripts/send_message.py --chat-id {args.chat_id} --message \"Your message\"")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to get chat info: {e}")
        print("\n💡 Make sure:")
        print("   - The chat ID is correct")
        print("   - The bot has access to this chat")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
