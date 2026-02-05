---
name: telegram-bot-agent
description: Comprehensive Telegram Bot management for Claude agents. Use when the user needs to: (1) Create or configure Telegram bots, (2) Send messages to users or groups, (3) Manage bot interactions, (4) Join groups or channels, (5) Handle Telegram notifications, or any other Telegram bot automation tasks.
---

# Telegram Bot Agent

This skill enables Claude to act as a Telegram bot, managing accounts, sending messages, and automating Telegram interactions.

## Prerequisites

Before using this skill, ensure the following are installed:

```bash
pip install python-telegram-bot python-dotenv
```

## Workflow

### 1. Bot Creation and Setup

When the user wants to create or configure a Telegram bot:

1. Guide them to create a bot via @BotFather on Telegram:
   - Send `/newbot` to @BotFather
   - Provide a name and username for the bot
   - Save the API token provided by BotFather

2. Run the initialization script:
   ```bash
   python scripts/init_bot.py
   ```
   This will prompt for the bot token and create a `.env` file with configuration.

3. Verify the bot is working:
   ```bash
   python scripts/test_connection.py
   ```

### 2. Sending Messages

When the user wants to send messages:

**To a specific user (by chat ID):**
```bash
python scripts/send_message.py --chat-id <CHAT_ID> --message "Your message here"
```

**To a specific username:**
```bash
python scripts/send_message.py --username @username --message "Your message here"
```

**To a group:**
```bash
python scripts/send_message.py --chat-id <GROUP_CHAT_ID> --message "Your message here"
```

### 3. Managing Contacts

**Get bot information:**
```bash
python scripts/bot_info.py
```

**List recent chats:**
```bash
python scripts/list_chats.py
```

### 4. Joining Groups

To join a group or channel:

1. The bot must be added to the group by a group admin
2. Use the invite link or have an admin add the bot directly
3. Verify group membership:
   ```bash
   python scripts/get_chat_info.py --chat-id <GROUP_CHAT_ID>
   ```

### 5. Advanced Features

**Send formatted messages (Markdown/HTML):**
```bash
python scripts/send_message.py --chat-id <CHAT_ID> --message "**Bold** text" --format markdown
```

**Send messages with buttons:**
```bash
python scripts/send_with_buttons.py --chat-id <CHAT_ID> --message "Choose option" --buttons "Option 1,Option 2"
```

**Send files/photos:**
```bash
python scripts/send_file.py --chat-id <CHAT_ID> --file path/to/file.pdf
python scripts/send_photo.py --chat-id <CHAT_ID> --photo path/to/photo.jpg
```

## Configuration

All bot configuration is stored in `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DEFAULT_CHAT_ID=your_default_chat_id
```

## Important Notes

1. **Chat ID Discovery**: Users need to interact with the bot first. Run `scripts/list_chats.py` after users message the bot to get their chat IDs.

2. **Privacy Mode**: By default, bots in groups only receive messages that:
   - Start with `/` (commands)
   - Are replies to the bot's messages
   - Use @mentions of the bot

   To receive all messages, disable privacy mode via @BotFather.

3. **Rate Limits**: Telegram enforces rate limits. The scripts include basic rate limiting, but avoid sending too many messages too quickly.

4. **Error Handling**: All scripts include comprehensive error handling and logging. Check console output for debugging.

## Reference Documentation

For detailed API information and advanced usage:
- See `references/telegram_api.md` for complete Telegram Bot API reference
- See `references/examples.md` for common usage patterns and code examples

## Security Best Practices

1. **Never commit** the `.env` file or expose the bot token
2. **Validate** all user inputs before sending messages
3. **Use** environment variables for all sensitive configuration
4. **Rotate** bot tokens regularly via @BotFather if compromised
5. **Monitor** bot activity and set up alerts for unusual behavior

## Troubleshooting

**Bot not receiving messages:**
- Check privacy mode settings with @BotFather
- Verify the bot is actually in the group/chat
- Ensure the bot hasn't been blocked by the user

**"Unauthorized" errors:**
- Verify the bot token is correct in `.env`
- Check if the token has been revoked via @BotFather

**Cannot send to group:**
- Confirm the bot is a member of the group
- Check bot has permission to send messages
- Verify the chat ID is correct (group IDs are negative numbers)

## Examples

### Quick Notification Setup

To set up a bot for sending notifications:

```bash
# 1. Initialize bot
python scripts/init_bot.py

# 2. Message your bot on Telegram to establish chat
# 3. Get your chat ID
python scripts/list_chats.py

# 4. Send a test notification
python scripts/send_message.py --chat-id YOUR_CHAT_ID --message "Test notification"

# 5. (Optional) Set as default chat
echo "DEFAULT_CHAT_ID=YOUR_CHAT_ID" >> .env
```

### Integration with Claude Agent

The agent can automatically send Telegram notifications by calling the scripts:

```python
# In your agent code
import subprocess

def notify_telegram(message):
    subprocess.run([
        'python', 'scripts/send_message.py',
        '--use-default',  # Uses DEFAULT_CHAT_ID from .env
        '--message', message
    ])
```
