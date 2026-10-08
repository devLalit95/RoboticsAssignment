"""Calculator tool - Evaluate mathematical expressions."""

from typing import Union
from app.exceptions import InvalidCalculatorExpressionError
from app.logger import logger


def calculator(expression: str) -> Union[float, str]:
    """Evaluate a mathematical expression.

    Args:
        expression: Mathematical expression as string (e.g., "2 + 3 * 4")

    Returns:
        Result of evaluation as float, or error message if invalid

    Raises:
        InvalidCalculatorExpressionError: If expression is invalid
    """
    try:
        # Validate expression
        if not expression or not expression.strip():
            raise InvalidCalculatorExpressionError("Expression cannot be empty")

        # Allow only safe characters
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            raise InvalidCalculatorExpressionError(
                "Expression contains invalid characters"
            )

        # Evaluate expression
        result = eval(expression, {"__builtins__": {}}, {})

        # Ensure result is numeric
        if not isinstance(result, (int, float)):
            raise InvalidCalculatorExpressionError(
                "Expression must evaluate to a number"
            )

        logger.log_info(f"Calculator evaluated: {expression} = {result}")
        return float(result)

    except InvalidCalculatorExpressionError:
        raise
    except ZeroDivisionError:
        raise InvalidCalculatorExpressionError("Division by zero")
    except SyntaxError:
        raise InvalidCalculatorExpressionError("Invalid expression syntax")
    except Exception as e:
        raise InvalidCalculatorExpressionError(f"Calculation error: {str(e)}")
