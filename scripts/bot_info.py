#!/usr/bin/env python3
"""
Get bot information
Displays bot username, ID, and capabilities
"""

import asyncio
import sys
from telegram_bot import TelegramBotWrapper


async def main():
    """Display bot information"""
    print("🤖 Telegram Bot Information\n")

    try:
        bot = TelegramBotWrapper()
        info = await bot.get_me()

        print("📋 Bot Details:\n")
        print(f"   Bot ID: {info['id']}")
        print(f"   Username: @{info['username']}")
        print(f"   First Name: {info['first_name']}")
        print(f"   Is Bot: {info['is_bot']}")
        print()

        print("⚙️  Capabilities:\n")
        print(f"   Can Join Groups: {'✅ Yes' if info['can_join_groups'] else '❌ No'}")
        print(f"   Can Read All Group Messages: {'✅ Yes' if info['can_read_all_group_messages'] else '❌ No'}")
        print(f"   Supports Inline Queries: {'✅ Yes' if info['supports_inline_queries'] else '❌ No'}")
        print()

        print("🔗 Bot Link:")
        print(f"   https://t.me/{info['username']}")
        print()

        # Check default chat ID
        if bot.default_chat_id:
            print(f"💬 Default Chat ID: {bot.default_chat_id}")
            print("   (Set in .env file)")
        else:
            print("💡 No default chat ID set")
            print("   To set one, add DEFAULT_CHAT_ID to your .env file")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to get bot info: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
