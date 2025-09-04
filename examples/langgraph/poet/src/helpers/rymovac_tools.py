from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


@tool
async def check_rhyme(word1: str, word2: str) -> str:
    """
    Check if two words/phrases/verses rhyme using rymovac.cz API.
    
    Args:
        word1: First word, phrase, or verse to compare
        word2: Second word, phrase, or verse to compare
    
    Returns:
        String description of rhyme check result
    """
    from helpers.rymovac_api import check_rhyme_api
    
    try:
        is_rhyme = await check_rhyme_api(word1, word2)
        if is_rhyme:
            return f"'{word1}' and '{word2}' DO rhyme according to rymovac.cz"
        else:
            return f"'{word1}' and '{word2}' do NOT rhyme according to rymovac.cz"
    except Exception as e:
        return f"Error checking rhyme for '{word1}' and '{word2}': {str(e)}"


@tool
async def find_rhymes(word: str, count: int = 10) -> str:
    """
    Find rhymes for a given word/phrase/verse using rymovac.cz API.
    
    Args:
        word: Word, phrase, or verse to find rhymes for
        count: Maximum number of rhymes to return (default: 10)
    
    Returns:
        String with list of rhyming words
    """
    from helpers.rymovac_api import find_rhymes_api
    
    try:
        rhymes = await find_rhymes_api(word, count=count)
        if rhymes:
            rhymes_text = ", ".join(rhymes)
            return f"Rhymes for '{word}': {rhymes_text}"
        else:
            return f"No rhymes found for '{word}'"
    except Exception as e:
        return f"Error finding rhymes for '{word}': {str(e)}"
