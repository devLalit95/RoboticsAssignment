"""Main entry point for the Simple AI Agent application."""

import sys
import uvicorn
from app.api.routes import app


def run_api():
    """Run the FastAPI server."""
    print("Starting Simple AI Agent API server...")
    uvicorn.run(
        "app.api.routes:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


def run_cli():
    """Run the CLI interface."""
    from app.agent.agent import Agent
    from app.memory.memory_store import MemoryStore

    print("=" * 50)
    print("Simple AI Agent - CLI Mode")
    print("=" * 50)
    print("Type your messages to chat with the agent.")
    print("Commands: /help, /clear, /memory, /exit")
    print("=" * 50)

    # Initialize agent
    memory_store = MemoryStore()
    agent = Agent(memory_store=memory_store)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input == "/exit":
                print("Goodbye!")
                break
            elif user_input == "/help":
                print("\nAvailable commands:")
                print("  /help  - Show this help message")
                print("  /clear - Clear conversation history")
                print("  /memory - Show long-term memory")
                print("  /exit  - Exit the program")
                continue
            elif user_input == "/clear":
                agent.clear_conversation()
                print("Conversation history cleared.")
                continue
            elif user_input == "/memory":
                memory = agent.get_memory()
                if memory:
                    print("\nLong-term memory:")
                    for key, value in memory.items():
                        print(f"  {key}: {value}")
                else:
                    print("\nNo long-term memory stored.")
                continue

            # Process message
            response = agent.process_message(user_input)
            print(f"\nAgent: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api()
    else:
        run_cli()
