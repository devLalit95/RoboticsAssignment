"""Memory tools - Save and search long-term memory."""

from typing import List, Dict
from app.memory.memory_store import MemoryStore
from app.logger import logger


# Global memory store instance
_memory_store: MemoryStore = None


def set_memory_store(memory_store: MemoryStore):
    """Set the global memory store instance.

    Args:
        memory_store: MemoryStore instance to use
    """
    global _memory_store
    _memory_store = memory_store
    logger.log_info("Memory store initialized for tools")


def save_memory(key: str, value: str) -> str:
    """Save a key-value pair to long-term memory.

    Args:
        key: Key to store
        value: Value to store

    Returns:
        Confirmation message
    """
    if _memory_store is None:
        raise RuntimeError("Memory store not initialized")

    result = _memory_store.save_preference(key, value)
    logger.log_info(f"Memory tool saved: {key} = {value}")
    return result


def search_memory(query: str) -> str:
    """Search long-term memory for matching preferences.

    Args:
        query: Search query

    Returns:
        Formatted string with search results
    """
    if _memory_store is None:
        raise RuntimeError("Memory store not initialized")

    results = _memory_store.search_preferences(query)

    if not results:
        logger.log_info(f"Memory tool search for '{query}' found no results")
        return f"No preferences found matching '{query}'"

    formatted_results = []
    for item in results:
        formatted_results.append(f"- {item['key']}: {item['value']}")

    result_text = f"Found {len(results)} preference(s) matching '{query}':\n" + "\n".join(formatted_results)
    logger.log_info(f"Memory tool search for '{query}' found {len(results)} results")
    return result_text
