"""Test suite for memory module."""

import pytest
import os
import json
from app.memory.memory_store import MemoryStore


@pytest.fixture
def memory_store():
    """Fixture for memory store with test file."""
    test_file = "test_memory.json"
    store = MemoryStore(long_term_file=test_file)
    yield store
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)


class TestShortTermMemory:
    """Test short-term memory (conversation history)."""

    def test_add_message(self, memory_store):
        """Test adding a message."""
        memory_store.add_message("user", "Hello")
        history = memory_store.get_history()
        assert len(history) == 1
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"

    def test_add_multiple_messages(self, memory_store):
        """Test adding multiple messages."""
        memory_store.add_message("user", "Hello")
        memory_store.add_message("assistant", "Hi there!")
        memory_store.add_message("user", "How are you?")
        history = memory_store.get_history()
        assert len(history) == 3

    def test_get_history_with_limit(self, memory_store):
        """Test getting history with limit."""
        memory_store.add_message("user", "Message 1")
        memory_store.add_message("user", "Message 2")
        memory_store.add_message("user", "Message 3")
        history = memory_store.get_history(limit=2)
        assert len(history) == 2
        assert history[0]["content"] == "Message 2"
        assert history[1]["content"] == "Message 3"

    def test_clear_history(self, memory_store):
        """Test clearing history."""
        memory_store.add_message("user", "Hello")
        memory_store.clear_history()
        history = memory_store.get_history()
        assert len(history) == 0


class TestLongTermMemory:
    """Test long-term memory (user preferences)."""

    def test_save_preference(self, memory_store):
        """Test saving a preference."""
        result = memory_store.save_preference("language", "Python")
        assert "Saved" in result
        assert memory_store.get_preference("language") == "Python"

    def test_get_preference(self, memory_store):
        """Test getting a preference."""
        memory_store.save_preference("color", "blue")
        value = memory_store.get_preference("color")
        assert value == "blue"

    def test_get_nonexistent_preference(self, memory_store):
        """Test getting a preference that doesn't exist."""
        value = memory_store.get_preference("nonexistent")
        assert value is None

    def test_search_preferences_found(self, memory_store):
        """Test searching preferences with match."""
        memory_store.save_preference("backend_language", "Java")
        memory_store.save_preference("frontend_language", "JavaScript")
        results = memory_store.search_preferences("language")
        assert len(results) == 2

    def test_search_preferences_not_found(self, memory_store):
        """Test searching preferences with no match."""
        memory_store.save_preference("color", "blue")
        results = memory_store.search_preferences("nonexistent")
        assert len(results) == 0

    def test_search_preferences_case_insensitive(self, memory_store):
        """Test that search is case insensitive."""
        memory_store.save_preference("Language", "Python")
        results = memory_store.search_preferences("language")
        assert len(results) == 1

    def test_clear_long_term_memory(self, memory_store):
        """Test clearing long-term memory."""
        memory_store.save_preference("key1", "value1")
        memory_store.save_preference("key2", "value2")
        memory_store.clear_long_term_memory()
        all_memory = memory_store.get_all_preferences()
        assert len(all_memory) == 0

    def test_get_all_preferences(self, memory_store):
        """Test getting all preferences."""
        memory_store.save_preference("key1", "value1")
        memory_store.save_preference("key2", "value2")
        all_memory = memory_store.get_all_preferences()
        assert len(all_memory) == 2
        assert all_memory["key1"] == "value1"
        assert all_memory["key2"] == "value2"

    def test_persistence(self, memory_store):
        """Test that memory persists to file."""
        memory_store.save_preference("test_key", "test_value")
        # Create new store with same file
        new_store = MemoryStore(long_term_file=memory_store.long_term_file)
        value = new_store.get_preference("test_key")
        assert value == "test_value"
        # Cleanup
        if os.path.exists(memory_store.long_term_file):
            os.remove(memory_store.long_term_file)
