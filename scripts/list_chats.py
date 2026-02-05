#!/usr/bin/env python3
"""
List recent chats and messages
Useful for discovering chat IDs
"""

import asyncio
import sys
from telegram_bot import TelegramBotWrapper


async def main():
    """List recent chats"""
    print("📋 Fetching recent chats...\n")

    try:
        bot = TelegramBotWrapper()
        updates = await bot.get_updates()

        if not updates:
            print("📭 No recent messages found.")
            print("\n💡 Tips:")
            print("   1. Send a message to your bot on Telegram")
            print("   2. Run this script again to see the chat ID")
            print("   3. For groups, add the bot and send a message in the group")
            return

        print(f"✅ Found {len(updates)} recent update(s)\n")

        # Extract unique chats
        chats = {}
        for update in updates:
            if 'message' in update:
                msg = update['message']
                chat_info = msg['chat']
                chat_id = chat_info['id']

                if chat_id not in chats:
                    chats[chat_id] = {
                        'chat': chat_info,
                        'from': msg.get('from'),
                        'latest_text': msg.get('text', '(no text)'),
                        'update_id': update['update_id']
                    }

        print(f"📬 Unique Chats ({len(chats)}):\n")

        for i, (chat_id, info) in enumerate(chats.items(), 1):
            chat = info['chat']
            print(f"{i}. Chat ID: {chat_id}")
            print(f"   Type: {chat['type']}")

            if chat['type'] == 'private':
                print(f"   User: {chat.get('first_name', 'N/A')} (@{chat.get('username', 'N/A')})")
            elif chat['type'] in ['group', 'supergroup']:
                print(f"   Group: {chat.get('title', 'N/A')}")
                if chat.get('username'):
                    print(f"   Username: @{chat['username']}")
            elif chat['type'] == 'channel':
                print(f"   Channel: {chat.get('title', 'N/A')}")

            if info['from']:
                from_user = info['from']
                print(f"   Last From: {from_user.get('first_name', 'N/A')} (@{from_user.get('username', 'N/A')})")

            print(f"   Latest: {info['latest_text'][:50]}...")
            print()

        print("💡 To send a message, use:")
        print(f"   python scripts/send_message.py --chat-id <CHAT_ID> --message \"Your message\"")
        print("\n💡 To set a default chat, add to .env:")
        print(f"   DEFAULT_CHAT_ID=<CHAT_ID>")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to fetch chats: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
