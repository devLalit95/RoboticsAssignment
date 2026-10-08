Build a beginner-friendly Agentic AI project named "simple-ai-agent".

Goal:
Implement a simple AI agent demonstrating the fundamental agent architecture:

LLM + Tools + Memory.

Technology stack:

- Python 3.11+
- gemini API for the LLM
- LangChain/LangGraph where appropriate
- FastAPI for backend API
- Simple CLI or Streamlit UI
- Pydantic for data validation
- python-dotenv for environment variables

Functional requirements:

1. Create an AI agent that accepts natural-language user requests.

2. Implement these tools:
   - calculator(expression)
   - get_current_time()
   - save_memory(key, value)
   - search_memory(query)

3. The LLM should decide when a tool is required.
   Do not manually route every request using if/else statements.

4. Implement short-term conversation memory so the agent can understand
   previous messages in the same conversation.

5. Implement simple long-term memory for user preferences.
   Example:
   User: "Remember that I prefer Java for backend development."
   Later:
   User: "Which backend language do I prefer?"

6. The agent should decide when to retrieve memory.

7. Add tool-call logging so that the console shows:
   - user input
   - selected tool
   - tool arguments
   - tool result
   - final response

8. Handle:
   - invalid calculator expressions
   - unavailable tools
   - malformed input
   - LLM/API errors
   - empty user messages

9. Use a clean project structure:

   simple-ai-agent/
   ├── app/
   │ ├── main.py
   │ ├── agent/
   │ │ ├── agent.py
   │ │ ├── prompts.py
   │ │ └── state.py
   │ ├── tools/
   │ │ ├── calculator.py
   │ │ ├── time_tool.py
   │ │ └── memory_tools.py
   │ ├── memory/
   │ │ └── memory_store.py
   │ └── api/
   │ └── routes.py
   ├── tests/
   ├── .env.example
   ├── requirements.txt
   └── README.md

10. Keep the implementation simple and educational.
    Do not add unnecessary enterprise architecture.

11. Explain in README:
    - What is an AI agent?
    - What is an LLM?
    - What is a tool?
    - What is short-term memory?
    - What is long-term memory?
    - How the LLM decides to call a tool
    - Complete execution flow

12. Add at least 8 test scenarios demonstrating:
    calculator usage,
    time tool usage,
    memory storage,
    memory retrieval,
    normal conversation,
    invalid input,
    multiple tool calls,
    tool failure.

13. Make the project runnable with:

    pip install -r requirements.txt
    python -m app.main

14. Never hard-code API keys.
    Use .env.

At the end, provide:

- complete source code
- setup instructions
- architecture explanation
- execution flow
- sample conversations
- test cases
- viva questions and answers
