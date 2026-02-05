# Telegram Bot API Reference

This document provides quick reference for common Telegram Bot API operations.

## Table of Contents

1. [Bot Setup](#bot-setup)
2. [Sending Messages](#sending-messages)
3. [Message Formatting](#message-formatting)
4. [Interactive Elements](#interactive-elements)
5. [File Operations](#file-operations)
6. [Chat Management](#chat-management)
7. [Rate Limits](#rate-limits)
8. [Error Handling](#error-handling)

## Bot Setup

### Creating a Bot

1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Provide bot name (displayed to users)
4. Provide bot username (must end with 'bot')
5. Save the API token provided

### Bot Configuration

Configure via @BotFather:
- `/setdescription` - Set bot description
- `/setabouttext` - Set "About" text
- `/setuserpic` - Set bot profile picture
- `/setcommands` - Set bot commands menu
- `/setprivacy` - Toggle privacy mode for groups

### Privacy Mode

**Enabled (default)**: Bot only receives:
- Messages starting with `/`
- Replies to bot's messages
- @mentions of the bot

**Disabled**: Bot receives all group messages

Change via @BotFather: `/setprivacy`

## Sending Messages

### Basic Text Message

```python
await bot.send_message(
    chat_id="123456789",
    text="Hello, World!"
)
```

### Message with Formatting

```python
# Markdown
await bot.send_message(
    chat_id="123456789",
    text="*bold* _italic_ `code`",
    parse_mode=ParseMode.MARKDOWN_V2
)

# HTML
await bot.send_message(
    chat_id="123456789",
    text="<b>bold</b> <i>italic</i> <code>code</code>",
    parse_mode=ParseMode.HTML
)
```

### Long Messages

Messages are limited to 4096 characters. For longer content:
- Split into multiple messages
- Send as a file (.txt)
- Use Telegraph (for formatted content)

## Message Formatting

### Markdown V2

- `*bold*` - **bold**
- `_italic_` - *italic*
- `__underline__` - <u>underline</u>
- `~strikethrough~` - ~~strikethrough~~
- `||spoiler||` - spoiler text
- `[link](url)` - hyperlink
- `` `code` `` - inline code
- ` ```language\ncode\n``` ` - code block

**Important**: Special characters must be escaped: `_*[]()~`>#+-=|{}.!`

### HTML

- `<b>text</b>` - **bold**
- `<i>text</i>` - *italic*
- `<u>text</u>` - <u>underline</u>
- `<s>text</s>` - ~~strikethrough~~
- `<span class="tg-spoiler">text</span>` - spoiler
- `<a href="url">text</a>` - hyperlink
- `<code>text</code>` - inline code
- `<pre><code class="language">code</code></pre>` - code block

## Interactive Elements

### Inline Keyboards

Buttons displayed below messages:

```python
keyboard = [
    [InlineKeyboardButton("Option 1", callback_data="opt1")],
    [InlineKeyboardButton("Option 2", callback_data="opt2")],
    [InlineKeyboardButton("Link", url="https://example.com")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

await bot.send_message(
    chat_id="123456789",
    text="Choose an option:",
    reply_markup=reply_markup
)
```

### Reply Keyboards

Custom keyboard replacing the default one:

```python
keyboard = [
    [KeyboardButton("Button 1"), KeyboardButton("Button 2")],
    [KeyboardButton("Button 3")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

await bot.send_message(
    chat_id="123456789",
    text="Use the keyboard:",
    reply_markup=reply_markup
)
```

## File Operations

### Sending Photos

```python
with open('photo.jpg', 'rb') as photo:
    await bot.send_photo(
        chat_id="123456789",
        photo=photo,
        caption="Photo caption"
    )
```

**Limits**:
- Photo size: 10 MB max recommended
- File size: 50 MB max via Bot API

### Sending Documents

```python
with open('document.pdf', 'rb') as document:
    await bot.send_document(
        chat_id="123456789",
        document=document,
        caption="Document description"
    )
```

### Sending Other Media

- `send_audio()` - Audio files
- `send_video()` - Video files
- `send_voice()` - Voice messages
- `send_video_note()` - Video messages
- `send_animation()` - GIF animations
- `send_sticker()` - Stickers

### Downloading Files

```python
# Get file info
file = await bot.get_file(file_id)

# Download file
await file.download_to_drive('local_filename')
```

## Chat Management

### Getting Chat Information

```python
chat = await bot.get_chat(chat_id="123456789")
# Returns: id, type, title, username, etc.
```

### Chat Types

- `private` - One-on-one chat
- `group` - Regular group (< 200 members)
- `supergroup` - Supergroup (> 200 members)
- `channel` - Broadcast channel

### Group Administration

```python
# Get chat administrators
admins = await bot.get_chat_administrators(chat_id="-100123456789")

# Get chat member count
count = await bot.get_chat_member_count(chat_id="-100123456789")

# Get chat member info
member = await bot.get_chat_member(chat_id="-100123456789", user_id=123456789)
```

### Bot Permissions in Groups

Check what the bot can do:

```python
member = await bot.get_chat_member(chat_id="-100123456789", user_id=bot_id)
# Check: can_send_messages, can_delete_messages, can_restrict_members, etc.
```

## Rate Limits

Telegram enforces the following limits:

### Message Limits

- **Normal messages**: 30 messages per second
- **Bulk messages**: 30 messages per second to different chats
- **Same chat**: 1 message per second

### Best Practices

1. Implement exponential backoff for retries
2. Queue messages when approaching limits
3. Use bulk sending methods when available
4. Monitor for rate limit errors (429)

### Handling Rate Limits

```python
from telegram.error import RetryAfter

try:
    await bot.send_message(chat_id="123456789", text="Hello")
except RetryAfter as e:
    # Wait for the specified time
    await asyncio.sleep(e.retry_after)
    # Retry the request
    await bot.send_message(chat_id="123456789", text="Hello")
```

## Error Handling

### Common Error Codes

- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid bot token
- `403 Forbidden` - Bot blocked by user or kicked from group
- `404 Not Found` - Chat not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Telegram server error

### Error Messages

- `"Unauthorized"` - Invalid bot token
- `"Bad Request: chat not found"` - Invalid chat ID or bot not in chat
- `"Forbidden: bot was blocked by the user"` - User blocked the bot
- `"Forbidden: bot is not a member of the supergroup"` - Bot not in group
- `"Bad Request: message is too long"` - Message exceeds 4096 characters

### Retry Strategy

```python
from telegram.error import NetworkError, TelegramError
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        await bot.send_message(chat_id="123456789", text="Hello")
        break
    except NetworkError:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        raise
    except TelegramError as e:
        # Log error and potentially notify admin
        print(f"Error: {e}")
        break
```

## Additional Resources

- [Official Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Bot FAQ](https://core.telegram.org/bots/faq)
- [Bot Best Practices](https://core.telegram.org/bots/tutorial)
