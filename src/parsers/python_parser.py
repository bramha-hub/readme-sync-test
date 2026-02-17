"""
Python AST parser for extracting code structure.
"""
import ast
from typing import List, Optional
from pathlib import Path

from parsers.base import BaseParser, FileAnalysis, FunctionInfo, ClassInfo


class PythonParser(BaseParser):
    """Parser for Python source files using AST."""
    
    def supports_file(self, filepath: str) -> bool:
        """Check if file is a Python file."""
        return filepath.endswith('.py')
    
    def parse(self, filepath: str, content: str) -> FileAnalysis:
        """Parse Python file using AST."""
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            # Return empty analysis if file has syntax errors
            return FileAnalysis(
                filepath=filepath,
                language='python',
                functions=[],
                classes=[],
                imports=[],
                module_docstring=None
            )
        
        # Extract module docstring
        module_docstring = ast.get_docstring(tree)
        
        # Extract imports
        imports = self._extract_imports(tree)
        
        # Extract functions and classes
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                # Only get top-level functions (not methods)
                if self._is_top_level(node, tree):
                    functions.append(self._extract_function(node))
            elif isinstance(node, ast.ClassDef):
                classes.append(self._extract_class(node))
        
        return FileAnalysis(
            filepath=filepath,
            language='python',
            functions=functions,
            classes=classes,
            imports=imports,
            module_docstring=module_docstring
        )
    
    def _is_top_level(self, node: ast.AST, tree: ast.Module) -> bool:
        """Check if a node is at the top level of the module."""
        return node in tree.body
    
    def _extract_function(self, node: ast.FunctionDef) -> FunctionInfo:
        """Extract information from a function definition."""
        # Get parameters
        parameters = []
        for arg in node.args.args:
            param_str = arg.arg
            if arg.annotation:
                param_str += f": {ast.unparse(arg.annotation)}"
            parameters.append(param_str)
        
        # Get return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        # Get decorators
        decorators = [ast.unparse(dec) for dec in node.decorator_list]
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        return FunctionInfo(
            name=node.name,
            parameters=parameters,
            return_type=return_type,
            docstring=docstring,
            line_number=node.lineno,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            decorators=decorators
        )
    
    def _extract_class(self, node: ast.ClassDef) -> ClassInfo:
        """Extract information from a class definition."""
        # Get base classes
        base_classes = [ast.unparse(base) for base in node.bases]
        
        # Get decorators
        decorators = [ast.unparse(dec) for dec in node.decorator_list]
        
        # Get methods
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(self._extract_function(item))
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        return ClassInfo(
            name=node.name,
            base_classes=base_classes,
            methods=methods,
            docstring=docstring,
            line_number=node.lineno,
            decorators=decorators
        )
    
    def _extract_imports(self, tree: ast.Module) -> List[str]:
        """Extract import statements."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"from {module} import {alias.name}")
        return imports
