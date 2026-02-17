"""
LLM integration for generating documentation updates.
"""
import os
from google import genai
from typing import Optional


class LLMClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "models/gemini-2.5-flash",
        temperature: float = 0.3,
        max_tokens: int = 4096
    ):
        """
        Initialize the LLM client.
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model name to use
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        # Initialize the modern Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate_documentation_update(self, prompt: str) -> str:
        """
        Generate documentation update using the LLM.
        
        Args:
            prompt: Structured prompt with context
            
        Returns:
            Generated documentation content
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'temperature': self.temperature,
                    'max_output_tokens': self.max_tokens,
                }
            )
            
            if not response or not response.text:
                raise ValueError("Empty response from LLM")
            
            return response.text.strip()
        
        except Exception as e:
            raise RuntimeError(f"Failed to generate documentation: {str(e)}")
    
    def extract_markdown_content(self, response: str) -> Optional[str]:
        """
        Extract markdown content from LLM response.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Extracted markdown content or None if no changes needed
        """
        # Check if no changes are needed
        if "NO_CHANGES_NEEDED" in response:
            return None
        
        # Try to extract content from markdown code blocks
        if "```markdown" in response:
            start = response.find("```markdown") + len("```markdown")
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()
        
        # If no code block, try to extract from triple backticks
        if "```" in response:
            parts = response.split("```")
            if len(parts) >= 3:
                return parts[1].strip()
        
        # Otherwise, return the full response (assuming it's already markdown)
        return response.strip()
