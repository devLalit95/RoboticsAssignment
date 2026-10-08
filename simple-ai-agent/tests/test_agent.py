"""Test suite for agent module."""

import pytest
from unittest.mock import Mock, patch
from app.agent.agent import Agent
from app.agent.state import AgentState
from app.memory.memory_store import MemoryStore
from app.exceptions import EmptyMessageError, AgentError


@pytest.fixture
def agent():
    """Fixture for agent with mocked LLM."""
    memory_store = MemoryStore()
    with patch('app.agent.agent.ChatGoogleGenerativeAI'):
        agent = Agent(memory_store=memory_store)
        return agent


class TestAgentState:
    """Test agent state management."""

    def test_initial_state(self):
        """Test initial state values."""
        state = AgentState()
        assert state.messages == []
        assert state.current_input is None
        assert state.selected_tool is None
        assert state.tool_arguments is None
        assert state.tool_result is None
        assert state.final_response is None
        assert state.error is None

    def test_add_message(self):
        """Test adding a message to state."""
        state = AgentState()
        state.add_message("user", "Hello")
        assert len(state.messages) == 1
        assert state.messages[0]["role"] == "user"
        assert state.messages[0]["content"] == "Hello"

    def test_get_last_n_messages(self):
        """Test getting last n messages."""
        state = AgentState()
        state.add_message("user", "Msg 1")
        state.add_message("assistant", "Msg 2")
        state.add_message("user", "Msg 3")
        last_two = state.get_last_n_messages(2)
        assert len(last_two) == 2
        assert last_two[0]["content"] == "Msg 2"
        assert last_two[1]["content"] == "Msg 3"

    def test_clear_state(self):
        """Test clearing state."""
        state = AgentState()
        state.current_input = "test"
        state.selected_tool = "calculator"
        state.final_response = "result"
        state.clear()
        assert state.current_input is None
        assert state.selected_tool is None
        assert state.final_response is None


class TestAgent:
    """Test agent functionality."""

    def test_empty_message_raises_error(self, agent):
        """Test that empty message raises error."""
        with pytest.raises(EmptyMessageError):
            agent.process_message("")

    def test_whitespace_only_message_raises_error(self, agent):
        """Test that whitespace-only message raises error."""
        with pytest.raises(EmptyMessageError):
            agent.process_message("   ")

    def test_add_message_to_memory(self, agent):
        """Test that message is added to memory."""
        with patch.object(agent.llm_with_tools, 'invoke') as mock_invoke:
            # Mock response without tool calls
            mock_response = Mock()
            mock_response.content = "Test response"
            mock_response.tool_calls = None
            mock_invoke.return_value = mock_response

            agent.process_message("Hello")

            history = agent.memory_store.get_history()
            assert len(history) == 2  # user + assistant
            assert history[0]["role"] == "user"
            assert history[0]["content"] == "Hello"

    def test_get_conversation_history(self, agent):
        """Test getting conversation history."""
        agent.memory_store.add_message("user", "Hello")
        agent.memory_store.add_message("assistant", "Hi")
        history = agent.get_conversation_history()
        assert len(history) == 2

    def test_clear_conversation(self, agent):
        """Test clearing conversation."""
        agent.memory_store.add_message("user", "Hello")
        agent.clear_conversation()
        history = agent.get_conversation_history()
        assert len(history) == 0

    def test_get_memory(self, agent):
        """Test getting long-term memory."""
        agent.memory_store.save_preference("key", "value")
        memory = agent.get_memory()
        assert memory["key"] == "value"

    def test_clear_memory(self, agent):
        """Test clearing long-term memory."""
        agent.memory_store.save_preference("key", "value")
        agent.clear_memory()
        memory = agent.get_memory()
        assert len(memory) == 0
