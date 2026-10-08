"""Agent implementation - Core agent logic with LLM integration and tool routing."""

from typing import Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.config import settings
from app.memory.memory_store import MemoryStore
from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT
from app.tools.tools import TOOLS
from app.tools.memory_tools import set_memory_store
from app.exceptions import (
    EmptyMessageError,
    LLMAPIError,
    InvalidCalculatorExpressionError,
    AgentError
)
from app.logger import logger


class Agent:
    """Simple AI Agent with LLM, tools, and memory."""

    def __init__(self, memory_store: Optional[MemoryStore] = None):
        """Initialize the agent.

        Args:
            memory_store: Optional memory store instance
        """
        self.state = AgentState()
        self.memory_store = memory_store or MemoryStore()

        # Initialize memory store for tools
        set_memory_store(self.memory_store)

        # Initialize LLM
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=settings.gemini_api_key,
                temperature=0.7,
            )
            # Bind tools to LLM
            self.llm_with_tools = self.llm.bind_tools(TOOLS)
            logger.log_info("Agent initialized with Gemini LLM and tools")
        except Exception as e:
            logger.log_error(f"Failed to initialize LLM: {e}")
            raise LLMAPIError(f"Failed to initialize LLM: {e}")

    def process_message(self, user_input: str) -> str:
        """Process a user message and return agent response.

        Args:
            user_input: User's input message

        Returns:
            Agent's response

        Raises:
            EmptyMessageError: If input is empty
            AgentError: If processing fails
        """
        # Validate input
        if not user_input or not user_input.strip():
            raise EmptyMessageError("User message cannot be empty")

        # Log user input
        logger.log_user_input(user_input)

        # Update state
        self.state.current_input = user_input

        try:
            # Add user message to memory
            self.memory_store.add_message("user", user_input)

            # Get conversation history
            history = self.memory_store.get_history(limit=10)

            # Check if we need to search memory based on context
            self._check_memory_context(user_input)

            # Build messages for LLM
            messages = self._build_messages(user_input, history)

            # Invoke LLM
            response = self.llm_with_tools.invoke(messages)

            # Check if LLM wants to call a tool
            if hasattr(response, 'tool_calls') and response.tool_calls:
                return self._handle_tool_calls(response, messages)
            else:
                # Direct response without tool call
                final_response = response.content
                self._finalize_interaction(final_response)
                return final_response

        except EmptyMessageError:
            raise
        except InvalidCalculatorExpressionError:
            raise
        except Exception as e:
            logger.log_error(f"Error processing message: {e}")
            self.state.error = str(e)
            raise AgentError(f"Failed to process message: {e}")

    def _build_messages(self, user_input: str, history: list) -> list:
        """Build message list for LLM.

        Args:
            user_input: Current user input
            history: Conversation history

        Returns:
            List of messages for LLM
        """
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        # Add conversation history
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        # Add current user input
        messages.append(HumanMessage(content=user_input))

        return messages

    def _check_memory_context(self, user_input: str):
        """Check if we need to retrieve memory based on context.

        Args:
            user_input: User's input message
        """
        # Simple heuristic: if user asks about preferences, memories, or things they said
        memory_keywords = ["remember", "preference", "like", "prefer", "told you", "said"]
        user_input_lower = user_input.lower()

        if any(keyword in user_input_lower for keyword in memory_keywords):
            # Search memory for relevant context
            results = self.memory_store.search_preferences(user_input)
            if results:
                logger.log_info(f"Retrieved {len(results)} memory items for context")

    def _handle_tool_calls(self, response, messages: list) -> str:
        """Handle tool calls from LLM.

        Args:
            response: LLM response with tool calls
            messages: Current message list

        Returns:
            Final agent response
        """
        tool_calls = response.tool_calls

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Log tool selection
            logger.log_tool_selected(tool_name, tool_args)
            self.state.selected_tool = tool_name
            self.state.tool_arguments = tool_args

            # Execute tool
            try:
                tool_result = self._execute_tool(tool_name, tool_args)
                logger.log_tool_result(str(tool_result))
                self.state.tool_result = str(tool_result)

                # Add tool result to messages and get final response
                messages.append(AIMessage(content="", tool_calls=[tool_call]))
                messages.append(HumanMessage(content=f"Tool result: {tool_result}"))

                # Get final response from LLM
                final_response = self.llm_with_tools.invoke(messages)
                final_text = final_response.content

                self._finalize_interaction(final_text)
                return final_text

            except Exception as e:
                error_msg = f"Tool execution failed: {str(e)}"
                logger.log_error(error_msg)
                self.state.error = error_msg

                # Inform LLM of error and get response
                messages.append(AIMessage(content="", tool_calls=[tool_call]))
                messages.append(HumanMessage(content=f"Tool error: {error_msg}"))

                error_response = self.llm_with_tools.invoke(messages)
                self._finalize_interaction(error_response.content)
                return error_response.content

        return "No tools were executed."

    def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        """Execute a tool by name.

        Args:
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool

        Returns:
            Tool execution result

        Raises:
            AgentError: If tool not found or execution fails
        """
        # Find tool in TOOLS list
        tool = None
        for t in TOOLS:
            if t.name == tool_name:
                tool = t
                break

        if tool is None:
            raise AgentError(f"Tool not found: {tool_name}")

        # Execute tool
        try:
            result = tool.invoke(tool_args)
            return result
        except Exception as e:
            raise AgentError(f"Tool execution error: {str(e)}")

    def _finalize_interaction(self, response: str):
        """Finalize the interaction and update state.

        Args:
            response: Final agent response
        """
        self.state.final_response = response
        logger.log_final_response(response)

        # Add assistant response to memory
        self.memory_store.add_message("assistant", response)

        # Add to state messages
        self.state.add_message("assistant", response)

    def get_conversation_history(self) -> list:
        """Get conversation history.

        Returns:
            List of conversation messages
        """
        return self.memory_store.get_history()

    def clear_conversation(self):
        """Clear conversation history."""
        self.memory_store.clear_history()
        self.state.clear()
        logger.log_info("Conversation cleared")

    def get_memory(self) -> Dict[str, str]:
        """Get all long-term memory.

        Returns:
            Dictionary of all preferences
        """
        return self.memory_store.get_all_preferences()

    def clear_memory(self):
        """Clear long-term memory."""
        self.memory_store.clear_long_term_memory()
        logger.log_info("Long-term memory cleared")
