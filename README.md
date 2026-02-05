# Telegram Bot Agent Skill

A comprehensive Telegram Bot agent skill for Claude Code that enables automated bot management, messaging, and notification capabilities.

## 🚀 Features

- ✅ Easy bot setup and configuration
- 📤 Send messages to users and groups
- 📎 Send files, photos, and documents
- 🔘 Interactive inline keyboards
- 👥 Multi-user and group management
- 🔔 Notification system integration
- 📊 Chat information and analytics
- 🔒 Secure credential management

## 📋 Prerequisites

- Python 3.8 or higher
- A Telegram account
- Bot token from @BotFather

## 🔧 Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd telegram-bot-skill
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize your bot:
```bash
python scripts/init_bot.py
```

Follow the prompts to enter your bot token from @BotFather.

## 🎯 Quick Start

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Save the API token provided

### 2. Configure the Skill

```bash
python scripts/init_bot.py
```

Enter your bot token when prompted.

### 3. Test Connection

```bash
python scripts/test_connection.py
```

### 4. Get Your Chat ID

1. Message your bot on Telegram
2. Run:
```bash
python scripts/list_chats.py
```

3. Copy your chat ID from the output

### 5. Send Your First Message

```bash
python scripts/send_message.py --chat-id YOUR_CHAT_ID --message "Hello from my bot!"
```

Or set a default chat ID in `.env` and use:
```bash
python scripts/send_message.py --use-default --message "Hello!"
```

## 📚 Usage Examples

### Send a Text Message

```bash
# To specific chat
python scripts/send_message.py --chat-id 123456789 --message "Hello!"

# Using default chat
python scripts/send_message.py --use-default --message "Hello!"

# With formatting
python scripts/send_message.py --use-default --message "**Bold** text" --format markdown
```

### Send a Photo

```bash
python scripts/send_photo.py --chat-id 123456789 --photo path/to/photo.jpg --caption "Check this out!"
```

### Send a File

```bash
python scripts/send_file.py --chat-id 123456789 --file path/to/document.pdf
```

### Send Interactive Buttons

```bash
python scripts/send_with_buttons.py --chat-id 123456789 --message "Choose option" --buttons "Option 1,Option 2,Option 3"
```

### Get Chat Information

```bash
python scripts/get_chat_info.py --chat-id 123456789
```

### Get Bot Information

```bash
python scripts/bot_info.py
```

## 🔌 Integration with Claude Code

This skill is designed to work seamlessly with Claude Code. When installed as a skill, Claude can automatically:

- Send notifications about task completion
- Share generated files and reports
- Create interactive workflows
- Manage group communications

### Installing as a Claude Code Skill

1. Copy this directory to your Claude skills folder:
```bash
cp -r telegram-bot-skill ~/.claude/skills/
```

2. Restart Claude Code or reload skills

3. Claude will now recognize Telegram bot requests and use this skill automatically

## 🛠️ Available Scripts

| Script | Description |
|--------|-------------|
| `init_bot.py` | Initialize bot configuration |
| `test_connection.py` | Test bot connection |
| `bot_info.py` | Display bot information |
| `send_message.py` | Send text messages |
| `send_photo.py` | Send photos |
| `send_file.py` | Send documents |
| `send_with_buttons.py` | Send messages with buttons |
| `list_chats.py` | List recent chats |
| `get_chat_info.py` | Get specific chat information |

## 📖 Documentation

- [Telegram API Reference](references/telegram_api.md) - Complete API documentation
- [Usage Examples](references/examples.md) - Practical code examples
- [SKILL.md](SKILL.md) - Claude agent instructions

## 🔒 Security Best Practices

1. **Never commit** the `.env` file
2. **Never share** your bot token
3. **Validate** all user inputs
4. **Use** environment variables for credentials
5. **Rotate** tokens if compromised
6. **Monitor** bot activity regularly

## 🐛 Troubleshooting

### Bot not receiving messages

- Check privacy mode settings via @BotFather
- Ensure bot is in the group/chat
- Verify bot hasn't been blocked

### "Unauthorized" errors

- Verify bot token in `.env`
- Check if token was revoked via @BotFather

### Cannot send to group

- Confirm bot is a group member
- Check bot permissions
- Verify chat ID is correct (group IDs are negative)

### Rate limiting

- Telegram limits: 30 messages/second
- Implement delays between messages
- Use exponential backoff for retries

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Telegram Bot API](https://core.telegram.org/bots/api) - Official documentation
- Claude Code Skills system

## 📞 Support

For issues and questions:
- Check [Telegram Bot FAQ](https://core.telegram.org/bots/faq)
- Review [python-telegram-bot docs](https://docs.python-telegram-bot.org/)
- Open an issue in this repository

## 🔗 Useful Links

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [@BotFather](https://t.me/botfather) - Bot management on Telegram

---

Made with ❤️ for Claude Code agents
