"""Time tool - Get current time."""

from datetime import datetime
from app.logger import logger


def get_current_time() -> str:
    """Get the current time.

    Returns:
        Current time as formatted string
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    logger.log_info(f"Retrieved current time: {formatted_time}")
    return formatted_time
