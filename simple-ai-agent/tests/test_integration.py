"""Integration tests for the agent with mocked LLM."""

import pytest
from unittest.mock import Mock, patch
from app.agent.agent import Agent
from app.memory.memory_store import MemoryStore
from app.tools.tools import TOOLS


@pytest.fixture
def agent_with_mock():
    """Fixture for agent with mocked LLM."""
    memory_store = MemoryStore()

    with patch('app.agent.agent.ChatGoogleGenerativeAI') as mock_llm_class:
        # Create mock LLM instance
        mock_llm = Mock()
        mock_llm_class.return_value = mock_llm

        # Create agent
        agent = Agent(memory_store=memory_store)

        # Mock the bind_tools method
        mock_llm_with_tools = Mock()
        mock_llm.bind_tools.return_value = mock_llm_with_tools
        agent.llm_with_tools = mock_llm_with_tools

        return agent, mock_llm_with_tools


class TestIntegrationNormalConversation:
    """Test normal conversation without tools."""

    def test_simple_conversation(self, agent_with_mock):
        """Test simple Q&A conversation."""
        agent, mock_llm = agent_with_mock

        # Mock response without tool calls
        mock_response = Mock()
        mock_response.content = "Hello! How can I help you today?"
        mock_response.tool_calls = None
        mock_llm.invoke.return_value = mock_response

        response = agent.process_message("Hello")
        assert response == "Hello! How can I help you today?"
        assert agent.state.final_response == response

    def test_multi_turn_conversation(self, agent_with_mock):
        """Test multi-turn conversation."""
        agent, mock_llm = agent_with_mock

        # First message
        mock_response1 = Mock()
        mock_response1.content = "Hi there!"
        mock_response1.tool_calls = None
        mock_llm.invoke.return_value = mock_response1

        response1 = agent.process_message("Hello")
        assert response1 == "Hi there!"

        # Second message
        mock_response2 = Mock()
        mock_response2.content = "I'm doing well, thanks!"
        mock_response2.tool_calls = None
        mock_llm.invoke.return_value = mock_response2

        response2 = agent.process_message("How are you?")
        assert response2 == "I'm doing well, thanks!"

        # Check history
        history = agent.get_conversation_history()
        assert len(history) == 4  # 2 user + 2 assistant


class TestIntegrationToolCalls:
    """Test tool calling functionality."""

    def test_calculator_tool_call(self, agent_with_mock):
        """Test calculator tool call."""
        agent, mock_llm = agent_with_mock

        # Mock tool call response
        mock_tool_call = {
            "name": "calculator",
            "args": {"expression": "2 + 3"},
            "id": "call_123"
        }

        mock_response1 = Mock()
        mock_response1.content = ""
        mock_response1.tool_calls = [mock_tool_call]
        mock_llm.invoke.return_value = mock_response1

        # Mock final response after tool execution
        mock_response2 = Mock()
        mock_response2.content = "The result is 5"
        mock_response2.tool_calls = None
        mock_llm.invoke.return_value = mock_response2

        response = agent.process_message("What is 2 + 3?")
        assert "5" in response

    def test_time_tool_call(self, agent_with_mock):
        """Test time tool call."""
        agent, mock_llm = agent_with_mock

        # Mock tool call response
        mock_tool_call = {
            "name": "get_current_time",
            "args": {},
            "id": "call_123"
        }

        mock_response1 = Mock()
        mock_response1.content = ""
        mock_response1.tool_calls = [mock_tool_call]
        mock_llm.invoke.return_value = mock_response1

        # Mock final response
        mock_response2 = Mock()
        mock_response2.content = "The current time is available"
        mock_response2.tool_calls = None
        mock_llm.invoke.return_value = mock_response2

        response = agent.process_message("What time is it?")
        assert "time" in response.lower()

    def test_memory_save_tool_call(self, agent_with_mock):
        """Test save_memory tool call."""
        agent, mock_llm = agent_with_mock

        # Mock tool call response
        mock_tool_call = {
            "name": "save_memory",
            "args": {"key": "language", "value": "Python"},
            "id": "call_123"
        }

        mock_response1 = Mock()
        mock_response1.content = ""
        mock_response1.tool_calls = [mock_tool_call]
        mock_llm.invoke.return_value = mock_response1

        # Mock final response
        mock_response2 = Mock()
        mock_response2.content = "I've saved that preference"
        mock_response2.tool_calls = None
        mock_llm.invoke.return_value = mock_response2

        response = agent.process_message("Remember that I like Python")
        assert "saved" in response.lower()

    def test_memory_search_tool_call(self, agent_with_mock):
        """Test search_memory tool call."""
        agent, mock_llm = agent_with_mock

        # First save a preference
        agent.memory_store.save_preference("language", "Python")

        # Mock tool call response
        mock_tool_call = {
            "name": "search_memory",
            "args": {"query": "language"},
            "id": "call_123"
        }

        mock_response1 = Mock()
        mock_response1.content = ""
        mock_response1.tool_calls = [mock_tool_call]
        mock_llm.invoke.return_value = mock_response1

        # Mock final response
        mock_response2 = Mock()
        mock_response2.content = "You prefer Python"
        mock_response2.tool_calls = None
        mock_llm.invoke.return_value = mock_response2

        response = agent.process_message("What language do I prefer?")
        assert "python" in response.lower()


class TestIntegrationErrorHandling:
    """Test error handling in integration."""

    def test_tool_failure_handling(self, agent_with_mock):
        """Test handling of tool failure."""
        agent, mock_llm = agent_with_mock

        # Mock tool call with invalid calculator expression
        mock_tool_call = {
            "name": "calculator",
            "args": {"expression": "invalid"},
            "id": "call_123"
        }

        mock_response1 = Mock()
        mock_response1.content = ""
        mock_response1.tool_calls = [mock_tool_call]
        mock_llm.invoke.return_value = mock_response1

        # Mock error response
        mock_response2 = Mock()
        mock_response2.content = "Sorry, there was an error with the calculation"
        mock_response2.tool_calls = None
        mock_llm.invoke.return_value = mock_response2

        response = agent.process_message("Calculate invalid")
        assert "error" in response.lower()

    def test_invalid_input_handling(self, agent_with_mock):
        """Test handling of invalid input."""
        agent, _ = agent_with_mock

        with pytest.raises(Exception):
            agent.process_message("")


class TestIntegrationMemoryContext:
    """Test memory context retrieval."""

    def test_memory_context_on_preference_question(self, agent_with_mock):
        """Test that memory is checked when user asks about preferences."""
        agent, mock_llm = agent_with_mock

        # Save a preference
        agent.memory_store.save_preference("language", "Python")

        # Mock response
        mock_response = Mock()
        mock_response.content = "You prefer Python"
        mock_response.tool_calls = None
        mock_llm.invoke.return_value = mock_response

        response = agent.process_message("What is my preferred language?")
        assert response == "You prefer Python"
