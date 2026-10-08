# Simple AI Agent

A beginner-friendly Agentic AI project demonstrating the fundamental agent architecture: **LLM + Tools + Memory**.

## Table of Contents

- [Overview](#overview)
- [Concepts](#concepts)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Sample Conversations](#sample-conversations)
- [Viva Questions](#viva-questions)

---

## Overview

This project implements a simple AI agent that can:
- Accept natural language user requests
- Use tools (calculator, time, memory) when needed
- Remember conversation context (short-term memory)
- Store and retrieve user preferences (long-term memory)
- Decide autonomously when to use tools (no manual routing)

**Technology Stack:**
- Python 3.11+
- Gemini API (LLM - using gemini-1.5-pro model)
- LangChain/LangGraph (Agent framework)
- FastAPI (REST API)
- Pydantic (Data validation)
- python-dotenv (Environment variables)

---

## Concepts

### What is an AI Agent?

An AI Agent is an autonomous system that can perceive its environment, reason about it, and take actions to achieve goals. Unlike a simple chatbot that only responds to prompts, an agent can:

- Use tools to perform actions (calculations, API calls, database queries)
- Maintain memory across conversations
- Make decisions about which actions to take
- Chain multiple actions together to solve complex problems

**Key Components:**
1. **LLM (Large Language Model)** - The "brain" that understands language and makes decisions
2. **Tools** - Functions the agent can call to perform specific tasks
3. **Memory** - Storage for conversation history and user preferences

### What is an LLM?

A Large Language Model (LLM) is a neural network trained on vast amounts of text data. It can:
- Understand and generate human-like text
- Follow instructions and answer questions
- Make decisions based on context
- Decide when to call tools

In this project, we use **Gemini** (Google's LLM) through the LangChain library.

### What is a Tool?

A tool is a function that the agent can call to perform specific tasks that the LLM cannot do directly. Examples:

- **Calculator**: Perform mathematical calculations
- **Time Tool**: Get the current date/time
- **Memory Tools**: Save and retrieve information
- **API Tools**: Call external services (weather, news, etc.)

The LLM analyzes the user's request and decides if a tool is needed, which tool to use, and what arguments to pass.

### What is Short-term Memory?

Short-term memory (conversation history) stores the recent messages in the current conversation. This allows the agent to:

- Remember what the user said earlier in the conversation
- Maintain context across multiple turns
- Provide coherent, context-aware responses

**Example:**
```
User: What is 2 + 3?
Agent: 2 + 3 = 5
User: What about 4 + 5?
Agent: 4 + 5 = 9
```
The agent remembers the previous question about math.

### What is Long-term Memory?

Long-term memory stores user preferences and information that should persist across conversations. This allows the agent to:

- Remember user preferences (e.g., preferred programming language)
- Recall facts the user has shared
- Provide personalized responses over time

**Example:**
```
User: Remember that I prefer Python for backend development.
Agent: I've saved that you prefer Python for backend development.

[LATER IN A NEW CONVERSATION]
User: Which backend language do I prefer?
Agent: You prefer Python for backend development.
```

### How the LLM Decides to Call a Tool

The LLM decides to call a tool through a process called "tool calling" or "function calling":

1. **Analysis**: The LLM analyzes the user's request
2. **Tool Selection**: Based on the request, the LLM decides if a tool is needed
3. **Argument Extraction**: The LLM extracts the necessary arguments for the tool
4. **Execution**: The tool is executed with the provided arguments
5. **Response**: The LLM receives the tool result and formulates a response

**Example Flow:**
```
User: "What is 15 * 7?"

LLM Analysis:
- This is a mathematical calculation
- The calculator tool is appropriate
- Expression: "15 * 7"

Tool Call: calculator(expression="15 * 7")
Tool Result: 105

LLM Response: "15 * 7 = 105"
```

The LLM makes this decision autonomously - there are no if/else statements in our code routing specific requests to specific tools.

### Complete Execution Flow

```
1. User sends message
   ↓
2. Message added to short-term memory
   ↓
3. Check long-term memory for relevant context
   ↓
4. Build conversation history with system prompt
   ↓
5. Send to LLM with available tools
   ↓
6. LLM decides:
   - Respond directly OR
   - Call a tool
   ↓
7a. If tool call:
   - Execute tool with arguments
   - Send result back to LLM
   - LLM generates final response
   ↓
7b. If direct response:
   - Use LLM's response directly
   ↓
8. Add response to short-term memory
   ↓
9. Return response to user
```

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│              (CLI / FastAPI / Streamlit)                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│                      Agent Layer                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Agent (orchestrates LLM, tools, memory)         │  │
│  └──────────────────────────────────────────────────┘  │
└──────────┬────────────────────────────┬────────────────┘
           │                            │
           ↓                            ↓
┌──────────────────────┐    ┌──────────────────────┐
│       Tools          │    │       Memory         │
│  ┌────────────────┐  │    │  ┌────────────────┐  │
│  │ Calculator     │  │    │  │ Short-term     │  │
│  │ Time           │  │    │  │ (Conversation) │  │
│  │ Save Memory    │  │    │  └────────────────┘  │
│  │ Search Memory  │  │    │  ┌────────────────┐  │
│  └────────────────┘  │    │  │ Long-term      │  │
└──────────────────────┘    │  │ (Preferences)  │  │
                            │  └────────────────┘  │
                            └──────────────────────┘
                                         │
                                         ↓
                            ┌──────────────────────┐
                            │   Storage (JSON)     │
                            └──────────────────────┘
```

### Component Interactions

1. **Agent** coordinates between LLM, tools, and memory
2. **LLM** (Gemini) processes messages and decides on tool calls
3. **Tools** perform specific actions (calc, time, memory operations)
4. **Memory** stores conversation history and user preferences
5. **API/CLI** provides user-facing interfaces

---

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/))

### Installation

1. Clone or navigate to the project directory:
```bash
cd simple-ai-agent
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Running the Application

**CLI Mode (default):**
```bash
python -m app.main
```

**API Mode:**
```bash
python -m app.main api
```

The API will be available at `http://localhost:8000`

---

## Usage

### CLI Mode

Start the CLI:
```bash
python -m app.main
```

Available commands:
- `/help` - Show help
- `/clear` - Clear conversation history
- `/memory` - Show long-term memory
- `/exit` - Exit the program

**Example CLI Session:**
```
You: What is 25 * 4?
Agent: 25 * 4 = 100

You: Remember that I prefer Python
Agent: I've saved that you prefer Python

You: What programming language do I prefer?
Agent: You prefer Python.
```

### API Mode

Start the API server:
```bash
python -m app.main api
```

**Endpoints:**

- `POST /chat` - Send a message to the agent
  ```bash
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is 10 + 5?"}'
  ```

- `GET /memory` - Get long-term memory
  ```bash
  curl http://localhost:8000/memory
  ```

- `DELETE /memory` - Clear long-term memory
  ```bash
  curl -X DELETE http://localhost:8000/memory
  ```

- `GET /conversation` - Get conversation history
  ```bash
  curl http://localhost:8000/conversation
  ```

- `DELETE /conversation` - Clear conversation history
  ```bash
  curl -X DELETE http://localhost:8000/conversation
  ```

- `GET /health` - Health check
  ```bash
  curl http://localhost:8000/health
  ```

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

---

## Project Structure

```
simple-ai-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point (CLI and API)
│   ├── config.py               # Configuration management
│   ├── logger.py               # Logging system
│   ├── exceptions.py           # Custom exceptions
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py            # Core agent logic
│   │   ├── state.py            # Agent state management
│   │   └── prompts.py          # System prompts
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── calculator.py       # Calculator tool
│   │   ├── time_tool.py        # Time tool
│   │   ├── memory_tools.py     # Memory tools
│   │   └── tools.py            # Tool registry
│   ├── memory/
│   │   ├── __init__.py
│   │   └── memory_store.py     # Memory implementation
│   └── api/
│       ├── __init__.py
│       └── routes.py           # FastAPI routes
├── tests/
│   ├── __init__.py
│   ├── test_tools.py           # Tool tests
│   ├── test_memory.py          # Memory tests
│   ├── test_agent.py           # Agent tests
│   └── test_integration.py     # Integration tests
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
└── README.md                   # This file
```

---

## Testing

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_tools.py
```

Run with verbose output:
```bash
pytest -v
```

**Test Coverage:**
- Calculator usage (valid/invalid expressions)
- Time tool functionality
- Memory storage and retrieval
- Memory search functionality
- Normal conversation flow
- Invalid input handling
- Multiple tool calls
- Tool failure handling

**Test Scenarios (8+):**
1. ✅ Calculator usage - valid arithmetic expressions
2. ✅ Calculator usage - invalid expressions
3. ✅ Time tool usage
4. ✅ Memory storage
5. ✅ Memory retrieval
6. ✅ Memory search
7. ✅ Normal conversation
8. ✅ Invalid input handling
9. ✅ Multiple tool calls
10. ✅ Tool failure handling

---

## Sample Conversations

### Conversation 1: Calculator Usage
```
User: What is 15 * 7?
Agent: 15 * 7 = 105

User: Calculate (20 + 30) / 5
Agent: (20 + 30) / 5 = 10.0
```

### Conversation 2: Time Query
```
User: What time is it?
Agent: The current time is 2026-10-08 17:45:30
```

### Conversation 3: Memory Storage and Retrieval
```
User: Remember that I prefer Java for backend development.
Agent: I've saved that you prefer Java for backend development.

User: What backend language do I prefer?
Agent: You prefer Java for backend development.
```

### Conversation 4: Multi-turn Conversation
```
User: What is 10 + 5?
Agent: 10 + 5 = 15

User: Now multiply that by 2
Agent: 15 * 2 = 30
```

### Conversation 5: Error Handling
```
User: Calculate 10 / 0
Agent: Sorry, there was an error with the calculation: Division by zero
```

### Conversation 6: Multiple Preferences
```
User: Remember that I like Python and my favorite color is blue.
Agent: I've saved that you like Python and your favorite color is blue.

User: What are my preferences?
Agent: Based on your memory:
- Python: programming language preference
- blue: favorite color
```

### Conversation 7: Context Retention
```
User: I'm learning about AI agents.
Agent: That's a fascinating topic! AI agents are systems that can...

User: Can you explain the components?
Agent: AI agents typically have three main components: an LLM (the brain), tools (for actions), and memory (for context).
```

### Conversation 8: Mixed Tool Usage
```
User: What time is it and also calculate 5 * 5?
Agent: The current time is 2026-10-08 17:50:00, and 5 * 5 = 25.
```

---

## Viva Questions and Answers

### Q1: What is the difference between short-term and long-term memory?
**Answer:** Short-term memory stores the conversation history for the current session, allowing the agent to maintain context across multiple turns. Long-term memory stores user preferences and information that persists across different sessions, enabling personalized responses over time.

### Q2: How does the LLM decide which tool to call?
**Answer:** The LLM analyzes the user's request and compares it with the descriptions of available tools. Based on this analysis, it autonomously decides if a tool is needed, which tool is appropriate, and what arguments to pass. This decision is made by the LLM itself, not through manual if/else routing in the code.

### Q3: Why do we use LangChain instead of calling the Gemini API directly?
**Answer:** LangChain provides abstractions that simplify working with LLMs. It handles tool binding, message formatting, conversation management, and provides a consistent interface across different LLM providers. It also includes utilities for prompts, chains, and agents that accelerate development.

### Q4: What happens when a tool fails?
**Answer:** When a tool fails, the error is caught and logged. The error message is sent back to the LLM, which then formulates a user-friendly response explaining what went wrong. This ensures graceful error handling without crashing the application.

### Q5: How is conversation history managed?
**Answer:** Conversation history is stored in the MemoryStore as a list of message dictionaries with 'role' and 'content' fields. Each user message and agent response is appended to this list. When sending a message to the LLM, we include the recent history (limited to the last N messages) to provide context.

### Q6: What is the role of Pydantic in this project?
**Answer:** Pydantic is used for data validation and settings management. It ensures that configuration values are of the correct type, validates API request/response models, and provides type hints throughout the codebase for better code clarity and IDE support.

### Q7: How does the agent know when to search memory?
**Answer:** The agent uses a simple heuristic: if the user's input contains keywords like "remember", "preference", "like", "prefer", "told you", or "said", it searches long-term memory for relevant context. The LLM can also explicitly call the search_memory tool when needed.

### Q8: What is the execution flow when a user sends a message?
**Answer:**
1. Message is validated (not empty)
2. Message is added to short-term memory
3. Memory is checked for relevant context
4. Conversation history is built with system prompt
5. Message is sent to LLM with available tools
6. LLM decides to respond directly or call a tool
7. If tool call: execute tool, send result to LLM, get final response
8. Response is added to short-term memory
9. Response is returned to user

### Q9: Why do we use environment variables for API keys?
**Answer:** Using environment variables keeps sensitive information like API keys out of the source code. This is a security best practice that prevents accidental exposure of credentials when code is shared or committed to version control.

### Q10: How can this project be extended?
**Answer:** The project can be extended by:
- Adding more tools (weather, news, database queries)
- Implementing more sophisticated memory (vector database for semantic search)
- Adding a web UI with Streamlit or React
- Implementing multi-agent systems
- Adding streaming responses
- Supporting multiple LLM providers
- Adding authentication and user management

---

## License

This project is created for educational purposes.

## Contributing

This is a beginner-friendly project. Feel free to fork, modify, and learn from it!
