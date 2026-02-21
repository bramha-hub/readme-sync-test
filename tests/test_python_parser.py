"""
Unit tests for the Python parser.
"""
import unittest
from src.parsers.python_parser import PythonParser


class TestPythonParser(unittest.TestCase):
    """Test cases for Python AST parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = PythonParser()
    
    def test_supports_python_files(self):
        """Test that parser recognizes Python files."""
        self.assertTrue(self.parser.supports_file("test.py"))
        self.assertFalse(self.parser.supports_file("test.js"))
    
    def test_parse_simple_function(self):
        """Test parsing a simple function."""
        code = '''
def greet(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"
'''
        analysis = self.parser.parse("test.py", code)
        
        self.assertEqual(len(analysis.functions), 1)
        func = analysis.functions[0]
        self.assertEqual(func.name, "greet")
        self.assertEqual(len(func.parameters), 1)
        self.assertEqual(func.return_type, "str")
        self.assertIn("Say hello", func.docstring)
    
    def test_parse_async_function(self):
        """Test parsing async functions."""
        code = '''
async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    return {}
'''
        analysis = self.parser.parse("test.py", code)
        
        self.assertEqual(len(analysis.functions), 1)
        self.assertTrue(analysis.functions[0].is_async)
    
    def test_parse_class(self):
        """Test parsing a class with methods."""
        code = '''
class Calculator:
    """A simple calculator."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a."""
        return a - b
'''
        analysis = self.parser.parse("test.py", code)
        
        self.assertEqual(len(analysis.classes), 1)
        cls = analysis.classes[0]
        self.assertEqual(cls.name, "Calculator")
        self.assertEqual(len(cls.methods), 2)
        self.assertIn("simple calculator", cls.docstring)
    
    def test_parse_with_decorators(self):
        """Test parsing functions with decorators."""
        code = '''
@staticmethod
@cache
def compute(n: int) -> int:
    """Compute something."""
    return n * 2
'''
        analysis = self.parser.parse("test.py", code)
        
        func = analysis.functions[0]
        self.assertEqual(len(func.decorators), 2)
        self.assertIn("staticmethod", func.decorators)
    
    def test_parse_imports(self):
        """Test extracting imports."""
        code = '''
import os
from typing import List, Dict
from pathlib import Path
'''
        analysis = self.parser.parse("test.py", code)
        
        # from typing import List, Dict produces 2 entries (one per name)
        self.assertEqual(len(analysis.imports), 4)
        self.assertIn("import os", analysis.imports)


if __name__ == '__main__':
    unittest.main()
