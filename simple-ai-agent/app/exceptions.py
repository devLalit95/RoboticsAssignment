"""Custom exception classes for error handling."""


class AgentError(Exception):
    """Base exception for agent-related errors."""

    pass


class InvalidCalculatorExpressionError(AgentError):
    """Raised when calculator receives an invalid expression."""

    pass


class ToolNotFoundError(AgentError):
    """Raised when a requested tool is not available."""

    pass


class MalformedInputError(AgentError):
    """Raised when user input is malformed."""

    pass


class LLMAPIError(AgentError):
    """Raised when LLM API call fails."""

    pass


class EmptyMessageError(AgentError):
    """Raised when user message is empty."""

    pass


class MemoryError(AgentError):
    """Raised when memory operation fails."""

    pass
