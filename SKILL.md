---
name: telegram-bot-agent
description: Comprehensive Telegram Bot management for Claude agents. Use when the user needs to: (1) Create or configure Telegram bots, (2) Send messages to users or groups BY NAME (e.g. "message John" or "send to the dev team"), (3) Manage contacts, (4) Join groups or channels, (5) Handle Telegram notifications, or any other Telegram bot automation tasks. Users naturally reference contacts by name, NOT by chat ID.
---

# Telegram Bot Agent

This skill enables Claude to act as a Telegram bot, managing accounts, sending messages, and automating Telegram interactions with a **natural, name-based contact system**.

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

4. **Import contacts** (IMPORTANT - do this early):
   ```bash
   # First, have users message the bot
   # Then import all chats as named contacts
   python scripts/contacts.py import
   ```

### 2. Contact Management

**CRITICAL**: Users speak naturally using names like "message John" or "chat with the dev team", NOT "send to chat_id 123456789". Always use the contact system to enable natural interactions.

**Import contacts from recent chats (recommended first step):**
```bash
python scripts/contacts.py import
```

**Add a contact manually:**
```bash
python scripts/contacts.py add "John" 123456789
python scripts/contacts.py add "Dev Team" -100123456789 --type supergroup
```

**List all contacts:**
```bash
python scripts/contacts.py list
```

**Search for a contact:**
```bash
python scripts/contacts.py search john
```

**Get chat ID by name (if needed):**
```bash
python scripts/contacts.py get "John"
```

**Remove a contact:**
```bash
python scripts/contacts.py remove "John"
```

### 3. Sending Messages

**IMPORTANT**: When users say "message John" or "send to the team", use contact names with `--to`:

**To a contact by name (PREFERRED METHOD):**
```bash
python scripts/send_message.py --to "John" -m "Hey, how are you?"
python scripts/send_message.py --to "Dev Team" -m "Deployment complete!"
python scripts/send_message.py --to "mom" -m "Love you!"
```

**To a chat ID (only if contact not saved):**
```bash
python scripts/send_message.py --to 123456789 -m "Hello!"
```

**Using default contact:**
```bash
python scripts/send_message.py --use-default -m "Quick update"
```

**With formatting:**
```bash
python scripts/send_message.py --to "John" -m "**Important** update" --format markdown
python scripts/send_message.py --to "Team" -m "<b>Bold</b> text" --format html
```

### 4. Other Operations

**Get bot information:**
```bash
python scripts/bot_info.py
```

**List recent chats (for debugging):**
```bash
python scripts/list_chats.py
```

**Get specific chat info:**
```bash
python scripts/get_chat_info.py --chat-id 123456789
```

### 5. Joining Groups

To join a group or channel:

1. The bot must be added to the group by a group admin
2. Use the invite link or have an admin add the bot directly
3. Import the group as a contact:
   ```bash
   python scripts/contacts.py import
   ```
4. Send messages by group name:
   ```bash
   python scripts/send_message.py --to "Project Team" -m "Hello everyone!"
   ```

### 6. Advanced Features

**Send formatted messages:**
```bash
python scripts/send_message.py --to "John" -m "**Bold** _italic_" --format markdown
```

**Send messages with buttons:**
```bash
python scripts/send_with_buttons.py --to "John" -m "Choose option" --buttons "Yes,No,Maybe"
```

**Send files/photos:**
```bash
python scripts/send_file.py --to "John" --file path/to/file.pdf
python scripts/send_photo.py --to "John" --photo path/to/photo.jpg --caption "Check this out!"
```

## Natural Language Translation

When users make requests in natural language, translate them to contact-based commands:

| User Says | Command to Use |
|-----------|----------------|
| "Message John" | `send_message.py --to "John" -m "..."` |
| "Send this to the dev team" | `send_message.py --to "dev team" -m "..."` |
| "Chat with mom" | `send_message.py --to "mom" -m "..."` |
| "Tell Sarah about the update" | `send_message.py --to "Sarah" -m "update"` |
| "Notify everyone in the group" | `send_message.py --to "group name" -m "..."` |

## Configuration

All bot configuration is stored in `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DEFAULT_CHAT_ID=your_default_chat_id
```

Contacts are stored in `contacts.json` (created automatically).

## Important Notes

1. **Always Use Contact Names**: When a user says "message John", use `--to "John"` not `--to 123456789`. This is more natural and user-friendly.

2. **Contact Import Workflow**:
   - Have users message the bot first (or add bot to groups)
   - Run `python scripts/contacts.py import` to auto-import all chats with names
   - Users can then reference everyone by name

3. **Natural Language**: Translate natural requests to commands:
   - "chat with the dev team" → `--to "dev team"`
   - "message John" → `--to "John"`
   - "send to everyone" → loop through contacts

4. **Group IDs**: Group chat IDs are negative numbers (e.g., -100123456789). The contact system handles this automatically.

5. **Privacy Mode**: By default, bots in groups only receive messages that:
   - Start with `/` (commands)
   - Are replies to the bot's messages
   - Use @mentions of the bot

   To receive all messages, disable privacy mode via @BotFather.

6. **Rate Limits**: Telegram enforces rate limits (30 messages/second). The scripts include basic rate limiting.

7. **Contact Names Are Case-Insensitive**: "John", "john", and "JOHN" all work the same way.

## Reference Documentation

For detailed API information and advanced usage:
- See `references/telegram_api.md` for complete Telegram Bot API reference
- See `references/examples.md` for common usage patterns and code examples

## Security Best Practices

1. **Never commit** the `.env` file or `contacts.json` (contains chat IDs)
2. **Never share** the bot token
3. **Validate** all user inputs before sending messages
4. **Use** environment variables for all sensitive configuration
5. **Rotate** bot tokens regularly via @BotFather if compromised

## Troubleshooting

**Contact not found:**
- Run `python scripts/contacts.py list` to see all contacts
- Run `python scripts/contacts.py import` to import from recent chats
- Add manually: `python scripts/contacts.py add "Name" chat_id`

**Bot not receiving messages:**
- Check privacy mode settings with @BotFather
- Verify the bot is in the group/chat
- Ensure the bot hasn't been blocked

**"Unauthorized" errors:**
- Verify the bot token is correct in `.env`
- Check if the token has been revoked via @BotFather

**Cannot send to group:**
- Confirm the bot is a member of the group
- Check bot has permission to send messages
- Import the group: `python scripts/contacts.py import`

## Examples

### Quick Setup for Natural Messaging

```bash
# 1. Initialize bot
python scripts/init_bot.py

# 2. Have people message your bot or add it to groups

# 3. Import all contacts with names
python scripts/contacts.py import

# 4. Now send messages naturally by name
python scripts/send_message.py --to "John" -m "Hey!"
python scripts/send_message.py --to "Dev Team" -m "Deploy complete"
python scripts/send_message.py --to "mom" -m "Love you"
```

### Integration Example

```python
# In your Python code
import subprocess

def message_contact(name, text):
    """Send message to a contact by name"""
    subprocess.run([
        'python', 'scripts/send_message.py',
        '--to', name,
        '-m', text
    ])

# Usage
message_contact("John", "Task completed!")
message_contact("Dev Team", "Build successful!")
```
