"""
Test module to demonstrate README-Sync functionality.

This file is used to test the README-Sync workflow.
"""


def greet_user(name: str) -> str:
    """
    Greet a user by name.
    
    Args:
        name: The name of the user to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to README-Sync!"


def calculate_total(items: list[float]) -> float:
    """
    Calculate the total sum of items.
    
    Args:
        items: List of numbers to sum
        
    Returns:
        The total sum of all items
    """
    return sum(items)


class DocumentationHelper:
    """Helper class for documentation operations."""
    
    def __init__(self, project_name: str):
        """
        Initialize the documentation helper.
        
        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        self.docs_updated = False
    
    def update_docs(self, content: str) -> bool:
        """
        Update documentation with new content.
        
        Args:
            content: New documentation content
            
        Returns:
            True if update was successful
        """
        # Simulated update
        self.docs_updated = True
        return True
