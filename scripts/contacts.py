#!/usr/bin/env python3
"""
Contact management system for Telegram Bot
Allows users to save and use friendly names instead of chat IDs
"""

import json
import sys
from pathlib import Path
from typing import Optional, List, Dict


class ContactManager:
    """Manage contacts with friendly names"""

    def __init__(self, storage_file: Optional[str] = None):
        if storage_file is None:
            # Store in project root
            project_root = Path(__file__).parent.parent
            storage_file = project_root / "contacts.json"

        self.storage_file = Path(storage_file)
        self.contacts = self._load()

    def _load(self) -> Dict:
        """Load contacts from file"""
        if self.storage_file.exists():
            try:
                return json.loads(self.storage_file.read_text())
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.storage_file}, starting fresh")
                return {}
        return {}

    def _save(self):
        """Save contacts to file"""
        self.storage_file.write_text(json.dumps(self.contacts, indent=2, ensure_ascii=False))

    def add(self, name: str, chat_id: str, chat_type: str = "private", title: Optional[str] = None) -> bool:
        """
        Add or update a contact

        Args:
            name: Friendly name (e.g., "John", "Dev Team")
            chat_id: Telegram chat ID
            chat_type: Type of chat (private, group, supergroup, channel)
            title: Optional chat title from Telegram

        Returns:
            True if new contact, False if updated existing
        """
        name_lower = name.lower()
        is_new = name_lower not in self.contacts

        self.contacts[name_lower] = {
            "name": name,  # Keep original case
            "chat_id": str(chat_id),
            "type": chat_type,
            "title": title
        }

        self._save()
        return is_new

    def remove(self, name: str) -> bool:
        """Remove a contact by name"""
        name_lower = name.lower()
        if name_lower in self.contacts:
            del self.contacts[name_lower]
            self._save()
            return True
        return False

    def get_chat_id(self, name: str) -> Optional[str]:
        """Get chat ID by name"""
        name_lower = name.lower()
        if name_lower in self.contacts:
            return self.contacts[name_lower]["chat_id"]
        return None

    def get_contact(self, name: str) -> Optional[Dict]:
        """Get full contact info by name"""
        name_lower = name.lower()
        return self.contacts.get(name_lower)

    def search(self, query: str) -> List[Dict]:
        """
        Search contacts by partial name match

        Args:
            query: Search term

        Returns:
            List of matching contacts
        """
        query_lower = query.lower()
        results = []

        for name_lower, contact in self.contacts.items():
            if query_lower in name_lower or query_lower in contact["name"].lower():
                results.append(contact)

        return results

    def list_all(self) -> List[Dict]:
        """Get all contacts sorted by name"""
        return sorted(self.contacts.values(), key=lambda x: x["name"].lower())

    def import_from_chats(self, chats: List[Dict]):
        """
        Import contacts from chat list

        Args:
            chats: List of chat dictionaries from list_chats.py
        """
        imported = 0

        for chat_info in chats:
            chat = chat_info['chat']
            chat_id = str(chat['id'])
            chat_type = chat['type']

            # Generate a friendly name
            if chat_type == 'private':
                # Use first name or username
                name = chat.get('first_name') or chat.get('username') or f"User_{chat_id}"
                title = f"{chat.get('first_name', '')} {chat.get('last_name', '')}".strip()
            else:
                # Use group/channel title
                name = chat.get('title') or f"{chat_type}_{chat_id}"
                title = chat.get('title')

            # Only import if not already exists
            if self.get_chat_id(name) is None:
                self.add(name, chat_id, chat_type, title)
                imported += 1

        return imported


def main():
    """CLI for contact management"""
    import argparse

    parser = argparse.ArgumentParser(description='Manage Telegram bot contacts')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add contact
    add_parser = subparsers.add_parser('add', help='Add a contact')
    add_parser.add_argument('name', help='Friendly name')
    add_parser.add_argument('chat_id', help='Telegram chat ID')
    add_parser.add_argument('--type', default='private', help='Chat type')

    # Remove contact
    remove_parser = subparsers.add_parser('remove', help='Remove a contact')
    remove_parser.add_argument('name', help='Contact name to remove')

    # List contacts
    subparsers.add_parser('list', help='List all contacts')

    # Search contacts
    search_parser = subparsers.add_parser('search', help='Search contacts')
    search_parser.add_argument('query', help='Search term')

    # Get chat ID
    get_parser = subparsers.add_parser('get', help='Get chat ID for a contact')
    get_parser.add_argument('name', help='Contact name')

    # Import from chats
    subparsers.add_parser('import', help='Import contacts from recent chats')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = ContactManager()

    if args.command == 'add':
        is_new = manager.add(args.name, args.chat_id, args.type)
        if is_new:
            print(f"✅ Added contact: {args.name} → {args.chat_id}")
        else:
            print(f"✅ Updated contact: {args.name} → {args.chat_id}")

    elif args.command == 'remove':
        if manager.remove(args.name):
            print(f"✅ Removed contact: {args.name}")
        else:
            print(f"❌ Contact not found: {args.name}")

    elif args.command == 'list':
        contacts = manager.list_all()
        if not contacts:
            print("📭 No contacts saved yet.")
            print("\n💡 Tips:")
            print("   1. Run: python scripts/contacts.py import")
            print("   2. Or add manually: python scripts/contacts.py add <name> <chat_id>")
        else:
            print(f"\n📇 Contacts ({len(contacts)}):\n")
            for contact in contacts:
                icon = "👤" if contact['type'] == 'private' else "👥"
                print(f"{icon} {contact['name']}")
                print(f"   Chat ID: {contact['chat_id']}")
                print(f"   Type: {contact['type']}")
                if contact.get('title'):
                    print(f"   Title: {contact['title']}")
                print()

    elif args.command == 'search':
        results = manager.search(args.query)
        if not results:
            print(f"❌ No contacts found matching: {args.query}")
        else:
            print(f"\n🔍 Found {len(results)} contact(s):\n")
            for contact in results:
                icon = "👤" if contact['type'] == 'private' else "👥"
                print(f"{icon} {contact['name']} → {contact['chat_id']}")

    elif args.command == 'get':
        chat_id = manager.get_chat_id(args.name)
        if chat_id:
            print(chat_id)
        else:
            print(f"❌ Contact not found: {args.name}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'import':
        # Import from recent chats
        import asyncio
        from telegram_bot import TelegramBotWrapper

        async def import_chats():
            bot = TelegramBotWrapper()
            updates = await bot.get_updates()

            # Extract unique chats
            chats = {}
            for update in updates:
                if 'message' in update:
                    msg = update['message']
                    chat_info = msg['chat']
                    chat_id = chat_info['id']
                    if chat_id not in chats:
                        chats[chat_id] = {'chat': chat_info, 'from': msg.get('from')}

            chat_list = list(chats.values())
            imported = manager.import_from_chats(chat_list)

            print(f"✅ Imported {imported} new contact(s) from {len(chat_list)} chat(s)")
            print("\n💡 View contacts: python scripts/contacts.py list")

        try:
            asyncio.run(import_chats())
        except Exception as e:
            print(f"❌ Failed to import: {e}")
            sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
