#!/usr/bin/env python3
"""
Core Telegram Bot wrapper class
Provides high-level interface to Telegram Bot API
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBotWrapper:
    """High-level wrapper for Telegram Bot operations"""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize bot wrapper

        Args:
            token: Bot token. If None, loads from .env file
        """
        if token is None:
            # Load from .env
            project_root = Path(__file__).parent.parent
            env_file = project_root / ".env"

            if not env_file.exists():
                raise ValueError(
                    "No bot token provided and .env file not found. "
                    "Run 'python scripts/init_bot.py' first."
                )

            load_dotenv(env_file)
            token = os.getenv('TELEGRAM_BOT_TOKEN')

            if not token:
                raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")

        self.bot = Bot(token=token)
        self.default_chat_id = os.getenv('DEFAULT_CHAT_ID')
        logger.info("TelegramBotWrapper initialized")

    async def get_me(self) -> Dict[str, Any]:
        """Get bot information"""
        try:
            me = await self.bot.get_me()
            return {
                'id': me.id,
                'username': me.username,
                'first_name': me.first_name,
                'is_bot': me.is_bot,
                'can_join_groups': me.can_join_groups,
                'can_read_all_group_messages': me.can_read_all_group_messages,
                'supports_inline_queries': me.supports_inline_queries
            }
        except TelegramError as e:
            logger.error(f"Failed to get bot info: {e}")
            raise

    async def send_message(
        self,
        text: str,
        chat_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[str, Any]:
        """
        Send a text message

        Args:
            text: Message text
            chat_id: Target chat ID. Uses default if None
            parse_mode: 'Markdown', 'MarkdownV2', or 'HTML'
            reply_markup: Inline keyboard markup for buttons

        Returns:
            Message information
        """
        if chat_id is None:
            chat_id = self.default_chat_id
            if chat_id is None:
                raise ValueError("No chat_id provided and no default chat_id set")

        try:
            message = await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )

            logger.info(f"Message sent to {chat_id}: {message.message_id}")

            return {
                'message_id': message.message_id,
                'chat_id': message.chat.id,
                'date': message.date.isoformat(),
                'text': message.text
            }
        except TelegramError as e:
            logger.error(f"Failed to send message: {e}")
            raise

    async def send_photo(
        self,
        photo_path: str,
        chat_id: Optional[str] = None,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a photo"""
        if chat_id is None:
            chat_id = self.default_chat_id
            if chat_id is None:
                raise ValueError("No chat_id provided and no default chat_id set")

        try:
            with open(photo_path, 'rb') as photo:
                message = await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption
                )

            logger.info(f"Photo sent to {chat_id}: {message.message_id}")

            return {
                'message_id': message.message_id,
                'chat_id': message.chat.id,
                'date': message.date.isoformat()
            }
        except TelegramError as e:
            logger.error(f"Failed to send photo: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Photo file not found: {photo_path}")
            raise

    async def send_document(
        self,
        document_path: str,
        chat_id: Optional[str] = None,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a document/file"""
        if chat_id is None:
            chat_id = self.default_chat_id
            if chat_id is None:
                raise ValueError("No chat_id provided and no default chat_id set")

        try:
            with open(document_path, 'rb') as document:
                message = await self.bot.send_document(
                    chat_id=chat_id,
                    document=document,
                    caption=caption
                )

            logger.info(f"Document sent to {chat_id}: {message.message_id}")

            return {
                'message_id': message.message_id,
                'chat_id': message.chat.id,
                'date': message.date.isoformat()
            }
        except TelegramError as e:
            logger.error(f"Failed to send document: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Document file not found: {document_path}")
            raise

    async def get_updates(self, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get updates (messages, etc.)

        Args:
            offset: Identifier of the first update to be returned

        Returns:
            List of updates
        """
        try:
            updates = await self.bot.get_updates(offset=offset, timeout=10)

            results = []
            for update in updates:
                update_dict = {
                    'update_id': update.update_id
                }

                if update.message:
                    msg = update.message
                    update_dict['message'] = {
                        'message_id': msg.message_id,
                        'date': msg.date.isoformat(),
                        'chat': {
                            'id': msg.chat.id,
                            'type': msg.chat.type,
                            'title': msg.chat.title,
                            'username': msg.chat.username,
                            'first_name': msg.chat.first_name
                        },
                        'from': {
                            'id': msg.from_user.id,
                            'is_bot': msg.from_user.is_bot,
                            'first_name': msg.from_user.first_name,
                            'username': msg.from_user.username
                        } if msg.from_user else None,
                        'text': msg.text
                    }

                results.append(update_dict)

            return results
        except TelegramError as e:
            logger.error(f"Failed to get updates: {e}")
            raise

    async def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """Get information about a chat"""
        try:
            chat = await self.bot.get_chat(chat_id=chat_id)

            result = {
                'id': chat.id,
                'type': chat.type,
                'title': chat.title,
                'username': chat.username,
                'first_name': chat.first_name,
                'last_name': chat.last_name,
                'description': chat.description
            }

            return result
        except TelegramError as e:
            logger.error(f"Failed to get chat info: {e}")
            raise

    def create_inline_keyboard(self, buttons: List[List[str]]) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard

        Args:
            buttons: 2D list of button labels
                Example: [['Button 1', 'Button 2'], ['Button 3']]

        Returns:
            InlineKeyboardMarkup object
        """
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for label in row:
                # Use label as both display text and callback data
                keyboard_row.append(InlineKeyboardButton(label, callback_data=label))
            keyboard.append(keyboard_row)

        return InlineKeyboardMarkup(keyboard)
