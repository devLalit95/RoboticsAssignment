"""Agent state management - Pydantic models for agent state."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """State of the agent during conversation."""

    messages: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Conversation history"
    )
    current_input: Optional[str] = Field(
        default=None,
        description="Current user input"
    )
    selected_tool: Optional[str] = Field(
        default=None,
        description="Name of selected tool"
    )
    tool_arguments: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arguments for the selected tool"
    )
    tool_result: Optional[str] = Field(
        default=None,
        description="Result from tool execution"
    )
    final_response: Optional[str] = Field(
        default=None,
        description="Final agent response"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if any"
    )

    def add_message(self, role: str, content: str):
        """Add a message to conversation history.

        Args:
            role: Message role (user/assistant)
            content: Message content
        """
        self.messages.append({"role": role, "content": content})

    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """Get last n messages from history.

        Args:
            n: Number of messages to retrieve

        Returns:
            List of last n messages
        """
        return self.messages[-n:] if n > 0 else []

    def clear(self):
        """Clear all state except conversation history."""
        self.current_input = None
        self.selected_tool = None
        self.tool_arguments = None
        self.tool_result = None
        self.final_response = None
        self.error = None
