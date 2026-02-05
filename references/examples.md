# Telegram Bot Usage Examples

This document provides practical examples for common Telegram bot use cases.

## Table of Contents

1. [Notification System](#notification-system)
2. [Interactive Menus](#interactive-menus)
3. [File Sharing](#file-sharing)
4. [Multi-User Management](#multi-user-management)
5. [Group Bot](#group-bot)
6. [Scheduled Messages](#scheduled-messages)

## Notification System

### Simple Alert Bot

Send notifications from your application:

```python
# notify.py
import asyncio
from telegram_bot import TelegramBotWrapper

async def send_alert(message, level="info"):
    """Send an alert notification"""
    bot = TelegramBotWrapper()

    # Add emoji based on level
    emoji = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    formatted_message = f"{emoji.get(level, 'ℹ️')} **{level.upper()}**\n\n{message}"

    await bot.send_message(
        text=formatted_message,
        parse_mode="Markdown"
    )

# Usage
if __name__ == '__main__':
    asyncio.run(send_alert("Deployment completed successfully!", "success"))
```

### System Monitoring

Monitor server health and send alerts:

```python
# monitor.py
import asyncio
import psutil
from telegram_bot import TelegramBotWrapper

async def check_system():
    """Check system resources and alert if needed"""
    bot = TelegramBotWrapper()

    # Check CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    alerts = []
    if cpu_percent > 90:
        alerts.append(f"⚠️ High CPU usage: {cpu_percent}%")
    if memory_percent > 90:
        alerts.append(f"⚠️ High memory usage: {memory_percent}%")
    if disk_percent > 90:
        alerts.append(f"⚠️ High disk usage: {disk_percent}%")

    if alerts:
        message = "**System Alert**\n\n" + "\n".join(alerts)
        await bot.send_message(text=message, parse_mode="Markdown")

# Run periodically
if __name__ == '__main__':
    asyncio.run(check_system())
```

### CI/CD Notifications

Notify about build/deployment status:

```python
# ci_notify.py
import asyncio
import sys
from telegram_bot import TelegramBotWrapper

async def notify_build(status, branch, commit_msg):
    """Notify about build status"""
    bot = TelegramBotWrapper()

    emoji = "✅" if status == "success" else "❌"

    message = f"""{emoji} **Build {status.upper()}**

**Branch:** `{branch}`
**Commit:** {commit_msg}

[View Details](https://your-ci-url.com)
"""

    await bot.send_message(text=message, parse_mode="Markdown")

# Usage from CI/CD pipeline
if __name__ == '__main__':
    status = sys.argv[1]  # success or failed
    branch = sys.argv[2]
    commit_msg = sys.argv[3]
    asyncio.run(notify_build(status, branch, commit_msg))
```

## Interactive Menus

### Simple Menu Bot

Create an interactive menu:

```python
# menu_bot.py
import asyncio
from telegram_bot import TelegramBotWrapper

async def show_main_menu(chat_id):
    """Display main menu"""
    bot = TelegramBotWrapper()

    buttons = [
        ["📊 Status", "⚙️ Settings"],
        ["📝 Reports", "ℹ️ Help"]
    ]

    keyboard = bot.create_inline_keyboard(buttons)

    await bot.send_message(
        chat_id=chat_id,
        text="**Main Menu**\n\nWhat would you like to do?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

if __name__ == '__main__':
    # Replace with your chat ID
    asyncio.run(show_main_menu("123456789"))
```

### Dynamic Options

Generate menu based on data:

```python
# dynamic_menu.py
import asyncio
from telegram_bot import TelegramBotWrapper

async def show_servers_menu(chat_id):
    """Display menu of available servers"""
    bot = TelegramBotWrapper()

    # Fetch server list (example)
    servers = ["Server-1", "Server-2", "Server-3", "Server-4"]

    # Create buttons (2 per row)
    buttons = [servers[i:i+2] for i in range(0, len(servers), 2)]

    keyboard = bot.create_inline_keyboard(buttons)

    await bot.send_message(
        chat_id=chat_id,
        text="**Select a server:**",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

if __name__ == '__main__':
    asyncio.run(show_servers_menu("123456789"))
```

## File Sharing

### Automated Report Delivery

Generate and send reports:

```python
# send_report.py
import asyncio
from datetime import datetime
from telegram_bot import TelegramBotWrapper

async def send_daily_report(chat_id):
    """Generate and send daily report"""
    bot = TelegramBotWrapper()

    # Generate report (example)
    report_date = datetime.now().strftime("%Y-%m-%d")
    report_path = f"/tmp/report_{report_date}.pdf"

    # Generate your report file here
    # generate_report(report_path)

    # Send report
    caption = f"📊 Daily Report - {report_date}"

    await bot.send_document(
        chat_id=chat_id,
        document_path=report_path,
        caption=caption
    )

if __name__ == '__main__':
    asyncio.run(send_daily_report("123456789"))
```

### Screenshot Sharing

Send screenshots automatically:

```python
# screenshot_bot.py
import asyncio
import subprocess
from datetime import datetime
from telegram_bot import TelegramBotWrapper

async def send_screenshot(chat_id):
    """Take and send screenshot"""
    bot = TelegramBotWrapper()

    # Take screenshot (Linux example)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"/tmp/screenshot_{timestamp}.png"

    subprocess.run(["import", "-window", "root", screenshot_path])

    # Send screenshot
    await bot.send_photo(
        chat_id=chat_id,
        photo_path=screenshot_path,
        caption=f"Screenshot taken at {timestamp}"
    )

if __name__ == '__main__':
    asyncio.run(send_screenshot("123456789"))
```

## Multi-User Management

### Broadcast Messages

Send message to multiple users:

```python
# broadcast.py
import asyncio
from telegram_bot import TelegramBotWrapper

async def broadcast(user_ids, message):
    """Send message to multiple users"""
    bot = TelegramBotWrapper()

    results = {"success": 0, "failed": 0}

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=message)
            results["success"] += 1
            # Rate limiting
            await asyncio.sleep(0.05)  # 20 messages per second
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")
            results["failed"] += 1

    print(f"Broadcast complete: {results['success']} sent, {results['failed']} failed")

if __name__ == '__main__':
    users = ["123456789", "987654321"]  # Your user list
    msg = "🎉 Important announcement!"
    asyncio.run(broadcast(users, msg))
```

### User Preference Management

Store and use user preferences:

```python
# preferences.py
import asyncio
import json
from pathlib import Path
from telegram_bot import TelegramBotWrapper

class UserPreferences:
    def __init__(self, storage_file="user_prefs.json"):
        self.storage = Path(storage_file)
        self.prefs = self.load()

    def load(self):
        if self.storage.exists():
            return json.loads(self.storage.read_text())
        return {}

    def save(self):
        self.storage.write_text(json.dumps(self.prefs, indent=2))

    def set_notification_time(self, user_id, time):
        if str(user_id) not in self.prefs:
            self.prefs[str(user_id)] = {}
        self.prefs[str(user_id)]["notification_time"] = time
        self.save()

    def get_notification_time(self, user_id):
        return self.prefs.get(str(user_id), {}).get("notification_time", "09:00")

# Usage
prefs = UserPreferences()
prefs.set_notification_time("123456789", "08:00")
```

## Group Bot

### Group Welcome Message

Welcome new members:

```python
# This would be part of a bot with update handlers

async def handle_new_member(update, context):
    """Send welcome message to new group members"""
    for member in update.message.new_chat_members:
        welcome_text = f"""
👋 Welcome to the group, {member.first_name}!

Please read our group rules and introduce yourself.

Use /help to see available commands.
"""
        await update.message.reply_text(welcome_text)
```

### Group Statistics

Send group statistics:

```python
# group_stats.py
import asyncio
from telegram_bot import TelegramBotWrapper

async def send_group_stats(group_chat_id):
    """Send group statistics"""
    bot = TelegramBotWrapper()

    # Get group info
    chat = await bot.get_chat(group_chat_id)

    # Get member count
    member_count = await bot.bot.get_chat_member_count(group_chat_id)

    stats = f"""📊 **Group Statistics**

**Group:** {chat['title']}
**Members:** {member_count}
**Type:** {chat['type']}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

    await bot.send_message(
        chat_id=group_chat_id,
        text=stats,
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    asyncio.run(send_group_stats("-100123456789"))  # Group chat IDs are negative
```

## Scheduled Messages

### Cron Job Integration

Use with cron for scheduled messages:

```bash
# crontab -e

# Send daily report at 9 AM
0 9 * * * cd /path/to/project && python scripts/send_message.py --use-default --message "Good morning! Daily report ready."

# Send weekly summary every Monday at 10 AM
0 10 * * 1 cd /path/to/project && python send_weekly_report.py
```

### Python Scheduler

Use schedule library:

```python
# scheduler.py
import asyncio
import schedule
import time
from telegram_bot import TelegramBotWrapper

async def send_reminder():
    """Send scheduled reminder"""
    bot = TelegramBotWrapper()
    await bot.send_message(text="⏰ Don't forget your meeting!")

def job():
    """Wrapper for async function"""
    asyncio.run(send_reminder())

# Schedule tasks
schedule.every().day.at("09:00").do(job)
schedule.every().monday.at("10:00").do(job)

print("Scheduler started. Press Ctrl+C to exit.")

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Integration Examples

### Flask Webhook

Receive notifications via HTTP:

```python
# webhook.py
from flask import Flask, request
import asyncio
from telegram_bot import TelegramBotWrapper

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    message = data.get('message', 'No message provided')

    asyncio.run(TelegramBotWrapper().send_message(text=message))

    return {"status": "sent"}, 200

if __name__ == '__main__':
    app.run(port=5000)
```

Usage:
```bash
curl -X POST http://localhost:5000/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from webhook!"}'
```

### Docker Integration

Send notifications from Docker containers:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Use environment variables for bot token
ENV TELEGRAM_BOT_TOKEN=""
ENV DEFAULT_CHAT_ID=""

CMD ["python", "your_bot_script.py"]
```

```bash
# Run with environment variables
docker run -e TELEGRAM_BOT_TOKEN="your_token" \
           -e DEFAULT_CHAT_ID="your_chat_id" \
           your-bot-image
```
