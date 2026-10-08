"""Tools registry - Register all tools for LangChain."""

from datetime import datetime
from langchain_core.tools import StructuredTool, tool
from pydantic import BaseModel, Field

from app.tools.calculator import calculator
from app.tools.memory_tools import save_memory, search_memory


# Calculator tool schema
class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""

    expression: str = Field(description="Mathematical expression to evaluate (e.g., '2 + 3 * 4')")


# Save memory tool schema
class SaveMemoryInput(BaseModel):
    """Input schema for save_memory tool."""

    key: str = Field(description="Key to store in memory")
    value: str = Field(description="Value to store in memory")


# Search memory tool schema
class SearchMemoryInput(BaseModel):
    """Input schema for search_memory tool."""

    query: str = Field(description="Search query to find in memory")


# Create LangChain tools
calculator_tool = StructuredTool.from_function(
    func=calculator,
    name="calculator",
    description="Evaluate mathematical expressions. Use this for any arithmetic calculations.",
    args_schema=CalculatorInput,
)

@tool
def get_current_time_tool() -> str:
    """Get the current date and time. Use this when user asks about time."""
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

save_memory_tool = StructuredTool.from_function(
    func=save_memory,
    name="save_memory",
    description="Save a key-value pair to long-term memory. Use this when user wants to remember something.",
    args_schema=SaveMemoryInput,
)

search_memory_tool = StructuredTool.from_function(
    func=search_memory,
    name="search_memory",
    description="Search long-term memory for preferences. Use this when user asks about their preferences or things they've told you to remember.",
    args_schema=SearchMemoryInput,
)

# List of all available tools
TOOLS = [calculator_tool, get_current_time_tool, save_memory_tool, search_memory_tool]
