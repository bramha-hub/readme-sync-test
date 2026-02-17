"""
Example Python module to demonstrate README-Sync.

This module contains sample functions that will be parsed by the AST parser.
"""


def calculate_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n: Position in the Fibonacci sequence (0-indexed)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


async def fetch_user_data(user_id: str, include_posts: bool = False) -> dict:
    """
    Fetch user data from the API.
    
    Args:
        user_id: Unique identifier for the user
        include_posts: Whether to include user's posts in the response
        
    Returns:
        Dictionary containing user data
    """
    # Simulated async operation
    return {
        "id": user_id,
        "name": "Example User",
        "posts": [] if include_posts else None
    }


class DataProcessor:
    """
    Process and transform data for analysis.
    
    This class provides methods for cleaning, transforming, and
    validating data before analysis.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the data processor.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.processed_count = 0
    
    def clean_data(self, data: list) -> list:
        """
        Remove invalid entries from data.
        
        Args:
            data: List of data entries
            
        Returns:
            Cleaned data list
        """
        cleaned = [item for item in data if self._is_valid(item)]
        self.processed_count += len(cleaned)
        return cleaned
    
    def _is_valid(self, item: dict) -> bool:
        """Check if a data item is valid."""
        return item is not None and len(item) > 0
    
    @staticmethod
    def transform(data: list, transformation: str) -> list:
        """
        Apply a transformation to the data.
        
        Args:
            data: Input data
            transformation: Type of transformation to apply
            
        Returns:
            Transformed data
        """
        if transformation == "uppercase":
            return [str(item).upper() for item in data]
        return data
