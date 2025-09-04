import aiohttp
from typing import List, Dict, Any, Optional
from urllib.parse import quote


class RymovacAPI:
    """Client for rymovac.cz API"""
    
    BASE_URL = "https://rymovac.cz/api/v1"
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session for requests"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def check_rhyme(self, word1: str, word2: str) -> Dict[str, Any]:
        """
        Check if two words/phrases rhyme using the rymovac.cz API
        
        Args:
            word1: First word/phrase/verse to compare
            word2: Second word/phrase/verse to compare
            
        Returns:
            Dict containing 'precision', 'is_rhyme', and 'log' fields
        """
        session = await self._get_session()
        
        url = f"{self.BASE_URL}/is-rhyme"
        params = {
            "word1": word1,
            "word2": word2
        }
        
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def find_rhymes(
        self, 
        word: str, 
        count: int = 10, 
        from_index: int = 0,
        precision: int = 0,
        source: int = 3
    ) -> Dict[str, Any]:
        """
        Find rhymes for a given word/phrase using the rymovac.cz API
        
        Args:
            word: Word or phrase to find rhymes for
            count: Number of rhymes to return (default: 10)
            from_index: Starting index for pagination (default: 0)
            precision: Precision level, use 0 for automatic (default: 0)
            source: Source type, always use 3 (default: 3)
            
        Returns:
            Dict containing rhymes data with 'word', 'precision', 'source', 'total_min', 'is_more_rhymes', 'arr_stats', 'arr', 'log'
        """
        session = await self._get_session()
        
        # URL encode the word for the path
        encoded_word = quote(word)
        url = f"{self.BASE_URL}/rhymes/{encoded_word}"
        
        params = {
            "precision": precision,
            "source": source,
            "from": from_index,
            "count": count
        }
        
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None


# Convenience functions for direct usage
async def check_rhyme_api(word1: str, word2: str) -> bool:
    """
    Simple function to check if two words rhyme
    
    Returns:
        bool: True if words rhyme, False otherwise
    """
    async with RymovacAPI() as api:
        result = await api.check_rhyme(word1, word2)
        return result.get("is_rhyme", False)


async def find_rhymes_api(word: str, count: int = 10) -> List[str]:
    """
    Simple function to find rhymes for a word
    
    Returns:
        List[str]: List of rhyming words
    """
    async with RymovacAPI() as api:
        result = await api.find_rhymes(word, count=count)
        rhymes = result.get("arr", [])
        return [rhyme.get("word", "") for rhyme in rhymes]