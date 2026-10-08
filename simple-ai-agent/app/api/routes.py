"""FastAPI routes - REST API endpoints for the agent."""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from app.agent.agent import Agent
from app.memory.memory_store import MemoryStore
from app.exceptions import AgentError, EmptyMessageError


# Request/Response models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., description="User message to process")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="Agent's response")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Information about tools called (if any)"
    )


class MemoryResponse(BaseModel):
    """Response model for memory endpoints."""

    memory: Dict[str, str] = Field(..., description="Long-term memory contents")


class HealthResponse(BaseModel):
    """Response model for health endpoint."""

    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")


# Initialize FastAPI app
app = FastAPI(
    title="Simple AI Agent API",
    description="REST API for the Simple AI Agent with LLM, tools, and memory",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent and memory store
memory_store = MemoryStore()
agent = Agent(memory_store=memory_store)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Simple AI Agent API is running"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a user message and return agent response.

    Args:
        request: Chat request with user message

    Returns:
        Chat response with agent's response and tool call info
    """
    try:
        response = agent.process_message(request.message)

        # Get tool call information from agent state
        tool_calls = None
        if agent.state.selected_tool:
            tool_calls = [{
                "tool": agent.state.selected_tool,
                "arguments": agent.state.tool_arguments,
                "result": agent.state.tool_result
            }]

        return ChatResponse(
            response=response,
            tool_calls=tool_calls
        )

    except EmptyMessageError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except AgentError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/memory", response_model=MemoryResponse)
async def get_memory():
    """Get all long-term memory.

    Returns:
        Current long-term memory contents
    """
    memory = agent.get_memory()
    return MemoryResponse(memory=memory)


@app.delete("/memory")
async def clear_memory():
    """Clear all long-term memory.

    Returns:
        Success message
    """
    agent.clear_memory()
    return {"message": "Long-term memory cleared"}


@app.get("/conversation")
async def get_conversation():
    """Get conversation history.

    Returns:
        List of conversation messages
    """
    history = agent.get_conversation_history()
    return {"conversation": history}


@app.delete("/conversation")
async def clear_conversation():
    """Clear conversation history.

    Returns:
        Success message
    """
    agent.clear_conversation()
    return {"message": "Conversation history cleared"}
