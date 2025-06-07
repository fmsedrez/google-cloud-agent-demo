from langchain.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def square(a: int) -> int:
    """Calculates the square of a number."""
    a = int(a)
    return a * a


@tool
def make_upper_case(text: str) -> str:
    """convert string to all upper case string"""
    return text.upper()


@tool
def make_lower_case(text: str) -> str:
    """convert string to all lower case string"""
    return text.lower()


@tool
def add_smiley(text: str) -> str:
    """add smiley face to the end of string"""
    return text + " :)"


math_toolkit = [add, multiply, square]
text_toolkit = [make_upper_case, make_lower_case, add_smiley]
