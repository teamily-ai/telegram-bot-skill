#!/usr/bin/env python3
"""
Initialize Telegram Bot configuration
Creates .env file with bot credentials
"""

import os
import sys
from pathlib import Path


def init_bot():
    """Initialize bot configuration"""
    print("🤖 Telegram Bot Initialization\n")

    # Get project root
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    # Check if .env already exists
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return

    # Get bot token
    print("📝 Please provide your bot information:")
    print("   (Get your bot token from @BotFather on Telegram)\n")

    bot_token = input("Bot Token: ").strip()

    if not bot_token:
        print("❌ Bot token is required!")
        sys.exit(1)

    # Optional: Get default chat ID
    print("\n💬 (Optional) Set a default chat ID for notifications:")
    print("   Leave empty to skip. You can add this later.\n")
    default_chat_id = input("Default Chat ID (optional): ").strip()

    # Create .env file
    env_content = f"""# Telegram Bot Configuration
# DO NOT commit this file to version control!

TELEGRAM_BOT_TOKEN={bot_token}
"""

    if default_chat_id:
        env_content += f"DEFAULT_CHAT_ID={default_chat_id}\n"

    # Write .env file
    with open(env_file, 'w') as f:
        f.write(env_content)

    print("\n✅ Configuration saved to .env")
    print("\n📋 Next steps:")
    print("   1. Test connection: python scripts/test_connection.py")
    print("   2. Message your bot on Telegram")
    print("   3. Get chat IDs: python scripts/list_chats.py")
    print("\n⚠️  Security reminder: Never commit the .env file!")

    # Create .gitignore if it doesn't exist
    gitignore_file = project_root / ".gitignore"
    if not gitignore_file.exists():
        with open(gitignore_file, 'w') as f:
            f.write(".env\n__pycache__/\n*.pyc\n.DS_Store\n")
        print("✅ Created .gitignore file")


if __name__ == '__main__':
    try:
        init_bot()
    except KeyboardInterrupt:
        print("\n\nInitialization cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
