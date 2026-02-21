"""
Parser factory for selecting the appropriate parser based on file type.
"""
import os
import sys
from typing import Optional, List

# Ensure sub-modules can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.base import BaseParser, FileAnalysis
from parsers.python_parser import PythonParser
from parsers.javascript_parser import JavaScriptParser


class ParserFactory:
    """Factory for creating appropriate parsers based on file type."""
    
    def __init__(self):
        self.parsers: List[BaseParser] = [
            PythonParser(),
            JavaScriptParser(),
        ]
    
    def get_parser(self, filepath: str) -> Optional[BaseParser]:
        """
        Get the appropriate parser for a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Parser instance or None if no parser supports the file
        """
        for parser in self.parsers:
            if parser.supports_file(filepath):
                return parser
        return None
    
    def parse_file(self, filepath: str, content: str) -> Optional[FileAnalysis]:
        """
        Parse a file using the appropriate parser.
        
        Args:
            filepath: Path to the file
            content: Content of the file
            
        Returns:
            FileAnalysis or None if no parser supports the file
        """
        parser = self.get_parser(filepath)
        if parser:
            return parser.parse(filepath, content)
        return None
