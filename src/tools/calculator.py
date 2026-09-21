
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression and return the result.
    Supports +, -, *, /, and parentheses. Example input: "12 * (3 + 4)"
    """
    try:
        allowed_chars = set("0123456789+-*/(). ")
        if not all(char in allowed_chars for char in expression):
            return "Error: expression contains invalid characters."

        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero."
    except Exception as e:
        return f"Error: could not evaluate expression — {e}"