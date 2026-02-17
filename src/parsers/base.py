"""
Base parser interface for code analysis.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FunctionInfo:
    """Information about a function or method."""
    name: str
    parameters: List[str]
    return_type: Optional[str]
    docstring: Optional[str]
    line_number: int
    is_async: bool = False
    decorators: List[str] = None
    
    def __post_init__(self):
        if self.decorators is None:
            self.decorators = []


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    base_classes: List[str]
    methods: List[FunctionInfo]
    docstring: Optional[str]
    line_number: int
    decorators: List[str] = None
    
    def __post_init__(self):
        if self.decorators is None:
            self.decorators = []


@dataclass
class FileAnalysis:
    """Complete analysis of a source file."""
    filepath: str
    language: str
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: List[str]
    module_docstring: Optional[str]


class BaseParser(ABC):
    """Base class for language-specific parsers."""
    
    @abstractmethod
    def parse(self, filepath: str, content: str) -> FileAnalysis:
        """
        Parse a source file and extract structural information.
        
        Args:
            filepath: Path to the file being parsed
            content: Content of the file
            
        Returns:
            FileAnalysis object containing extracted information
        """
        pass
    
    @abstractmethod
    def supports_file(self, filepath: str) -> bool:
        """
        Check if this parser supports the given file.
        
        Args:
            filepath: Path to check
            
        Returns:
            True if this parser can handle the file
        """
        pass
