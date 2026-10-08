"""Test suite for tools module."""

import pytest
import uuid
import os
from app.tools.calculator import calculator
from app.tools.time_tool import get_current_time
from app.tools.memory_tools import save_memory, search_memory, set_memory_store
from app.memory.memory_store import MemoryStore
from app.exceptions import InvalidCalculatorExpressionError


@pytest.fixture
def memory_store():
    """Fixture for memory store."""
    test_file = f"test_memory_{uuid.uuid4()}.json"
    store = MemoryStore(long_term_file=test_file)
    set_memory_store(store)
    yield store
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)


class TestCalculator:
    """Test calculator tool."""

    def test_valid_addition(self):
        """Test valid addition expression."""
        result = calculator("2 + 3")
        assert result == 5.0

    def test_valid_complex_expression(self):
        """Test complex arithmetic expression."""
        result = calculator("2 + 3 * 4")
        assert result == 14.0

    def test_valid_subtraction(self):
        """Test subtraction."""
        result = calculator("10 - 4")
        assert result == 6.0

    def test_valid_multiplication(self):
        """Test multiplication."""
        result = calculator("6 * 7")
        assert result == 42.0

    def test_valid_division(self):
        """Test division."""
        result = calculator("20 / 4")
        assert result == 5.0

    def test_valid_parentheses(self):
        """Test expression with parentheses."""
        result = calculator("(2 + 3) * 4")
        assert result == 20.0

    def test_invalid_empty_expression(self):
        """Test empty expression raises error."""
        with pytest.raises(InvalidCalculatorExpressionError):
            calculator("")

    def test_invalid_characters(self):
        """Test expression with invalid characters."""
        with pytest.raises(InvalidCalculatorExpressionError):
            calculator("2 + abc")

    def test_division_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(InvalidCalculatorExpressionError):
            calculator("10 / 0")

    def test_invalid_syntax(self):
        """Test invalid syntax raises error."""
        with pytest.raises(InvalidCalculatorExpressionError):
            calculator("2 + * 3")


class TestTimeTool:
    """Test time tool."""

    def test_get_current_time(self):
        """Test getting current time."""
        result = get_current_time()
        assert isinstance(result, str)
        assert len(result) > 0
        # Check format (YYYY-MM-DD HH:MM:SS)
        assert "-" in result and ":" in result


class TestMemoryTools:
    """Test memory tools."""

    def test_save_memory(self, memory_store):
        """Test saving to memory."""
        result = save_memory("language", "Python")
        assert "Saved" in result
        assert "language" in result
        assert "Python" in result

    def test_save_and_retrieve_memory(self, memory_store):
        """Test saving and retrieving memory."""
        save_memory("color", "blue")
        value = memory_store.get_preference("color")
        assert value == "blue"

    def test_search_memory_found(self, memory_store):
        """Test searching memory with match."""
        save_memory("backend", "Java")
        result = search_memory("backend")
        assert "backend" in result
        assert "Java" in result

    def test_search_memory_not_found(self, memory_store):
        """Test searching memory with no match."""
        result = search_memory("nonexistent")
        assert "No preferences found" in result

    def test_search_memory_partial_match(self, memory_store):
        """Test searching memory with partial match."""
        save_memory("programming_language", "Python")
        result = search_memory("language")
        assert "programming_language" in result or "language" in result

    def test_multiple_saves(self, memory_store):
        """Test saving multiple preferences."""
        save_memory("key1", "value1")
        save_memory("key2", "value2")
        all_memory = memory_store.get_all_preferences()
        assert len(all_memory) == 2
        assert all_memory["key1"] == "value1"
        assert all_memory["key2"] == "value2"
