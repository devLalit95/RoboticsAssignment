"""Memory store implementation - Short-term and long-term memory management."""

import json
import os
from typing import Dict, List, Optional
from threading import Lock

from app.exceptions import MemoryError
from app.logger import logger


class MemoryStore:
    """Manages both short-term and long-term memory for the agent."""

    def __init__(self, long_term_file: str = "long_term_memory.json"):
        """Initialize memory store.

        Args:
            long_term_file: File path for long-term memory storage
        """
        self.short_term_memory: List[Dict[str, str]] = []
        self.long_term_memory: Dict[str, str] = {}
        self.long_term_file = long_term_file
        self._lock = Lock()

        # Load long-term memory from file if exists
        self._load_long_term_memory()

    def _load_long_term_memory(self):
        """Load long-term memory from file."""
        try:
            if os.path.exists(self.long_term_file):
                with open(self.long_term_file, "r", encoding="utf-8") as f:
                    self.long_term_memory = json.load(f)
                logger.log_info(f"Loaded long-term memory from {self.long_term_file}")
        except Exception as e:
            logger.log_error(f"Failed to load long-term memory: {e}")
            self.long_term_memory = {}

    def _save_long_term_memory(self):
        """Save long-term memory to file."""
        try:
            with open(self.long_term_file, "w", encoding="utf-8") as f:
                json.dump(self.long_term_memory, f, indent=2)
            logger.log_info(f"Saved long-term memory to {self.long_term_file}")
        except Exception as e:
            logger.log_error(f"Failed to save long-term memory: {e}")
            raise MemoryError(f"Failed to save long-term memory: {e}")

    # Short-term memory methods (conversation history)

    def add_message(self, role: str, content: str):
        """Add a message to short-term memory.

        Args:
            role: Message role (user/assistant)
            content: Message content
        """
        with self._lock:
            self.short_term_memory.append({"role": role, "content": content})
            logger.log_info(f"Added {role} message to short-term memory")

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history.

        Args:
            limit: Optional limit on number of messages to return

        Returns:
            List of message dictionaries
        """
        with self._lock:
            if limit:
                return self.short_term_memory[-limit:]
            return self.short_term_memory.copy()

    def clear_history(self):
        """Clear short-term memory."""
        with self._lock:
            self.short_term_memory.clear()
            logger.log_info("Cleared short-term memory")

    # Long-term memory methods (user preferences)

    def save_preference(self, key: str, value: str) -> str:
        """Save a preference to long-term memory.

        Args:
            key: Preference key
            value: Preference value

        Returns:
            Confirmation message
        """
        with self._lock:
            self.long_term_memory[key] = value
            self._save_long_term_memory()
            logger.log_info(f"Saved preference: {key} = {value}")
            return f"Saved: {key} = {value}"

    def get_preference(self, key: str) -> Optional[str]:
        """Get a preference from long-term memory.

        Args:
            key: Preference key

        Returns:
            Preference value or None if not found
        """
        with self._lock:
            return self.long_term_memory.get(key)

    def search_preferences(self, query: str) -> List[Dict[str, str]]:
        """Search long-term memory for matching preferences.

        Args:
            query: Search query

        Returns:
            List of matching key-value pairs
        """
        with self._lock:
            query_lower = query.lower()
            results = []
            for key, value in self.long_term_memory.items():
                if query_lower in key.lower() or query_lower in value.lower():
                    results.append({"key": key, "value": value})
            logger.log_info(f"Search for '{query}' found {len(results)} results")
            return results

    def clear_long_term_memory(self):
        """Clear all long-term memory."""
        with self._lock:
            self.long_term_memory.clear()
            self._save_long_term_memory()
            logger.log_info("Cleared long-term memory")

    def get_all_preferences(self) -> Dict[str, str]:
        """Get all long-term memory preferences.

        Returns:
            Dictionary of all preferences
        """
        with self._lock:
            return self.long_term_memory.copy()
