from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


# TODO: implement following function
@tool
def check_rhyme(word1: str, word2: str) -> str:
    """Checks rhyme"""
    # TODO
    return str(word1[-2:] == word2[-2:])
