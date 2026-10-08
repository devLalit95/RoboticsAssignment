"""Agent prompts - System and conversation prompts for the LLM."""

SYSTEM_PROMPT = """You are a helpful AI assistant with access to various tools. You can help users with calculations, tell them the current time, and remember their preferences.

Available tools:
- calculator: Evaluate mathematical expressions (e.g., "2 + 3 * 4")
- get_current_time: Get the current date and time
- save_memory: Save a key-value pair to long-term memory
- search_memory: Search long-term memory for preferences

Instructions:
1. Use tools when appropriate based on the user's request
2. For calculations, always use the calculator tool
3. For time-related questions, use the get_current_time tool
4. When the user asks you to remember something, use save_memory with a relevant key and value
5. When the user asks about their preferences or things they've told you, use search_memory
6. Provide clear and helpful responses
7. If a tool fails, explain the error to the user
8. Maintain conversation context from previous messages

You are designed to be educational and beginner-friendly. Explain your actions clearly when using tools."""


def get_conversation_prompt(user_input: str, conversation_history: list) -> str:
    """Construct conversation prompt with history.

    Args:
        user_input: Current user input
        conversation_history: List of previous messages

    Returns:
        Formatted conversation prompt
    """
    prompt_parts = [SYSTEM_PROMPT]

    if conversation_history:
        prompt_parts.append("\nConversation history:")
        for msg in conversation_history:
            role = msg["role"].upper()
            content = msg["content"]
            prompt_parts.append(f"{role}: {content}")

    prompt_parts.append(f"\nUSER: {user_input}")
    prompt_parts.append("ASSISTANT:")

    return "\n".join(prompt_parts)
