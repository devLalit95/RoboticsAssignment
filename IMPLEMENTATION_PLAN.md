# Simple AI Agent - Implementation Plan

## Overview
Build a beginner-friendly Agentic AI project demonstrating LLM + Tools + Memory architecture using Python, Gemini API, LangChain/LangGraph, and FastAPI.

---

## Phase 1: Project Setup and Structure

### 1.1 Create directory structure
```
simple-ai-agent/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── state.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   ├── time_tool.py
│   │   └── memory_tools.py
│   ├── memory/
│   │   ├── __init__.py
│   │   └── memory_store.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   ├── test_memory.py
│   ├── test_agent.py
│   └── test_integration.py
├── .env.example
├── requirements.txt
├── README.md
└── IMPLEMENTATION_PLAN.md
```

### 1.2 Create configuration files
- `requirements.txt`: All dependencies
- `.env.example`: Environment variable template
- `__init__.py` files for Python package structure

### 1.3 Dependencies
- langchain
- langchain-google-genai
- langgraph
- fastapi
- uvicorn
- pydantic
- python-dotenv
- pytest
- httpx (for testing)

---

## Phase 2: Core Infrastructure

### 2.1 Configuration Module (`app/config.py`)
- Load environment variables using python-dotenv
- Validate required API keys
- Centralized configuration class
- Error handling for missing configuration

### 2.2 Logging System
- Custom logger for tool-call logging
- Log format: timestamp, level, message
- Console output showing:
  - User input
  - Selected tool
  - Tool arguments
  - Tool result
  - Final response

### 2.3 Error Handling
- Custom exception classes
- Error handlers for:
  - Invalid calculator expressions
  - Unavailable tools
  - Malformed input
  - LLM/API errors
  - Empty user messages
- Graceful error responses

---

## Phase 3: Memory Implementation

### 3.1 Memory Store (`app/memory/memory_store.py`)
- **Short-term Memory**: In-memory conversation history
  - Store message pairs (user, assistant)
  - Context window management
  - Methods: add_message, get_history, clear

- **Long-term Memory**: Persistent user preferences
  - Simple key-value storage (JSON file or dict)
  - Methods: save_preference, get_preference, search_preferences
  - Search functionality for querying stored preferences

### 3.2 Memory State Management
- Initialize memory store on startup
- Ensure thread-safe operations
- Validation of memory operations

---

## Phase 4: Tools Implementation

### 4.1 Calculator Tool (`app/tools/calculator.py`)
- Function: `calculator(expression: str) -> float`
- Uses Python's `eval()` with safe evaluation
- Error handling for invalid expressions
- Input validation
- Returns numeric result or error message

### 4.2 Time Tool (`app/tools/time_tool.py`)
- Function: `get_current_time() -> str`
- Returns current timestamp in readable format
- Uses Python's `datetime` module
- No parameters required

### 4.3 Memory Tools (`app/tools/memory_tools.py`)
- Function: `save_memory(key: str, value: str) -> str`
  - Stores key-value pair in long-term memory
  - Returns confirmation message

- Function: `search_memory(query: str) -> str`
  - Searches long-term memory for matching keys/values
  - Returns relevant preferences

### 4.4 Tool Registration
- Create tool schemas for LangChain
- Define tool descriptions for LLM
- Tool decorators and metadata

---

## Phase 5: Agent Core

### 5.1 State Management (`app/agent/state.py`)
- Pydantic models for agent state
- Fields: messages, current_input, selected_tool, tool_result
- Type validation
- State serialization

### 5.2 Prompts (`app/agent/prompts.py`)
- System prompt defining agent behavior
- Tool usage instructions
- Memory retrieval guidelines
- Few-shot examples for tool calling

### 5.3 Agent Implementation (`app/agent/agent.py`)
- **LLM Integration**:
  - Initialize Gemini model via LangChain
  - Configure tool binding
  - Set temperature and other parameters

- **Tool Routing**:
  - LLM decides which tool to call (no manual if/else)
  - Parse tool calls from LLM response
  - Execute selected tool with arguments
  - Handle tool results

- **Memory Integration**:
  - Load conversation history (short-term)
  - Retrieve relevant long-term memory
  - Update conversation after each interaction

- **Execution Flow**:
  1. Receive user input
  2. Add to conversation history
  3. Check memory for relevant context
  4. Send to LLM with history and tools
  5. LLM decides: respond directly or call tool
  6. If tool call: execute tool, send result to LLM
  7. LLM generates final response
  8. Update conversation history
  9. Return response to user

- **Error Handling**:
  - Catch and log all errors
  - Provide user-friendly error messages
  - Retry logic for transient failures

---

## Phase 6: API Layer

### 6.1 FastAPI Routes (`app/api/routes.py`)
- Endpoint: `POST /chat`
  - Request: `{ "message": "user input" }`
  - Response: `{ "response": "agent response", "tool_calls": [...] }`

- Endpoint: `GET /memory`
  - Returns current long-term memory

- Endpoint: `DELETE /memory`
  - Clears long-term memory

- Endpoint: `GET /health`
  - Health check endpoint

### 6.2 Request/Response Models
- Pydantic models for validation
- Error response schemas
- Tool call information in response

### 6.3 CORS and Middleware
- CORS configuration for frontend
- Request logging middleware
- Error handling middleware

---

## Phase 7: UI Layer

### 7.1 CLI Interface
- Simple command-line interface
- Interactive chat loop
- Commands:
  - `/help` - show help
  - `/clear` - clear conversation
  - `/memory` - show memory
  - `/exit` - quit

### 7.2 Streamlit UI (Optional/Alternative)
- Simple web UI
- Chat interface
- Memory viewer
- Tool call logs display

---

## Phase 8: Testing

### 8.1 Test Scenarios (8+ tests in `tests/`)

1. **Calculator Usage**
   - Test valid arithmetic expressions
   - Test complex expressions
   - Test invalid expressions

2. **Time Tool Usage**
   - Test current time retrieval
   - Verify format

3. **Memory Storage**
   - Test saving preferences
   - Test retrieval of saved data
   - Test persistence

4. **Memory Retrieval**
   - Test search functionality
   - Test partial matches
   - Test no matches

5. **Normal Conversation**
   - Test simple Q&A
   - Test multi-turn conversation
   - Test context retention

6. **Invalid Input**
   - Test empty messages
   - Test malformed input
   - Test error handling

7. **Multiple Tool Calls**
   - Test sequential tool calls
   - Test tool chaining
   - Test tool call dependencies

8. **Tool Failure**
   - Test calculator with invalid math
   - Test memory with missing keys
   - Test API failure scenarios

### 8.2 Test Implementation
- Use pytest framework
- Mock LLM responses for unit tests
- Integration tests with real tools
- Test coverage reporting

---

## Phase 9: Documentation

### 9.1 README.md Contents

**Conceptual Explanations**:
- What is an AI agent?
- What is an LLM?
- What is a tool?
- What is short-term memory?
- What is long-term memory?
- How the LLM decides to call a tool
- Complete execution flow

**Setup Instructions**:
- Prerequisites (Python 3.11+)
- Installation steps
- API key setup
- Running the application

**Usage Examples**:
- CLI usage
- API usage
- Sample conversations

**Project Structure**:
- Directory layout
- Module descriptions

### 9.2 Architecture Documentation
- High-level architecture diagram
- Component interactions
- Data flow diagram
- Technology stack rationale

### 9.3 Code Documentation
- Docstrings for all functions
- Type hints throughout
- Inline comments for complex logic

---

## Phase 10: Final Verification

### 10.1 Testing
- Run all test suites
- Verify 8+ test scenarios pass
- Check test coverage

### 10.2 Sample Conversations
Document 5-10 example conversations:
- Calculator usage
- Time queries
- Memory storage and retrieval
- Multi-turn conversations
- Error handling scenarios

### 10.3 Viva Questions and Answers
Prepare comprehensive Q&A covering:
- Agent architecture
- Tool calling mechanism
- Memory systems
- LLM integration
- Error handling
- Design decisions

### 10.4 Final Checklist
- ✓ All dependencies in requirements.txt
- ✓ No hardcoded API keys
- ✓ Clean project structure
- ✓ All tools implemented
- ✓ Memory systems working
- ✓ LLM tool routing functional
- ✓ Error handling comprehensive
- ✓ Logging shows all required info
- ✓ 8+ test scenarios passing
- ✓ README complete with explanations
- ✓ Setup instructions verified
- ✓ Project runnable with specified commands

---

## Implementation Notes

### Key Design Decisions
1. **LangGraph for Agent Logic**: Use LangGraph for stateful agent workflow
2. **In-Memory Short-term Memory**: Simple dict-based for conversation history
3. **JSON-based Long-term Memory**: File-based persistence for user preferences
4. **Gemini API**: Chosen for cost-effectiveness and good tool-calling support
5. **Pydantic**: Ensures type safety and validation throughout

### Best Practices
- Never commit API keys (use .env)
- Comprehensive error handling
- Extensive logging for debugging
- Modular design for maintainability
- Type hints for code clarity
- Test-driven development approach

### Success Criteria
- Agent successfully calls tools based on LLM decisions
- Memory systems function correctly
- Error handling covers all specified cases
- Logging shows complete execution flow
- All test scenarios pass
- README provides clear educational content
- Project is runnable with simple commands
