"""Logging module - Custom logger for tool-call logging."""

import logging
import sys
from typing import Optional


class AgentLogger:
    """Custom logger for agent operations with tool-call tracking."""

    def __init__(self, name: str = "agent", level: int = logging.INFO):
        """Initialize the logger.

        Args:
            name: Logger name
            level: Logging level (default: INFO)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(handler)

    def log_user_input(self, message: str):
        """Log user input.

        Args:
            message: User's input message
        """
        self.logger.info(f"USER INPUT: {message}")

    def log_tool_selected(self, tool_name: str, arguments: dict):
        """Log selected tool and its arguments.

        Args:
            tool_name: Name of the selected tool
            arguments: Tool arguments
        """
        self.logger.info(f"TOOL SELECTED: {tool_name}")
        self.logger.info(f"TOOL ARGUMENTS: {arguments}")

    def log_tool_result(self, result: str):
        """Log tool execution result.

        Args:
            result: Result from tool execution
        """
        self.logger.info(f"TOOL RESULT: {result}")

    def log_final_response(self, response: str):
        """Log final agent response.

        Args:
            response: Agent's final response
        """
        self.logger.info(f"FINAL RESPONSE: {response}")

    def log_error(self, error: str):
        """Log error.

        Args:
            error: Error message
        """
        self.logger.error(f"ERROR: {error}")

    def log_info(self, message: str):
        """Log general info.

        Args:
            message: Info message
        """
        self.logger.info(message)

    def log_warning(self, message: str):
        """Log warning.

        Args:
            message: Warning message
        """
        self.logger.warning(message)


# Global logger instance
logger = AgentLogger()
