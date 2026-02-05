#!/usr/bin/env python3
"""
Test Telegram Bot connection
Verifies bot token is valid and bot is accessible
"""

import asyncio
import sys
from telegram_bot import TelegramBotWrapper


async def main():
    """Test bot connection"""
    print("🔍 Testing Telegram Bot connection...\n")

    try:
        bot = TelegramBotWrapper()
        info = await bot.get_me()

        print("✅ Bot connection successful!\n")
        print("📋 Bot Information:")
        print(f"   ID: {info['id']}")
        print(f"   Username: @{info['username']}")
        print(f"   Name: {info['first_name']}")
        print(f"   Can Join Groups: {info['can_join_groups']}")
        print(f"   Can Read All Group Messages: {info['can_read_all_group_messages']}")
        print(f"   Supports Inline Queries: {info['supports_inline_queries']}")
        print("\n✅ Your bot is ready to use!")

        # Check if default chat ID is set
        if bot.default_chat_id:
            print(f"\n💬 Default chat ID is set: {bot.default_chat_id}")
        else:
            print("\n💡 Tip: Set a default chat ID in .env for easier messaging")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Run 'python scripts/init_bot.py' to set up your bot")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("\n💡 Check your bot token and internet connection")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
