"""
JavaScript/TypeScript parser using regex-based extraction.
For production use, consider using proper parsers like esprima or @babel/parser.
"""
import re
from typing import List, Optional

from .base import BaseParser, FileAnalysis, FunctionInfo, ClassInfo


class JavaScriptParser(BaseParser):
    """Basic parser for JavaScript and TypeScript files."""
    
    def supports_file(self, filepath: str) -> bool:
        """Check if file is JavaScript or TypeScript."""
        return filepath.endswith(('.js', '.jsx', '.ts', '.tsx'))
    
    def parse(self, filepath: str, content: str) -> FileAnalysis:
        """Parse JavaScript/TypeScript file using regex."""
        language = 'typescript' if filepath.endswith(('.ts', '.tsx')) else 'javascript'
        
        functions = self._extract_functions(content)
        classes = self._extract_classes(content)
        imports = self._extract_imports(content)
        
        return FileAnalysis(
            filepath=filepath,
            language=language,
            functions=functions,
            classes=classes,
            imports=imports,
            module_docstring=None
        )
    
    def _extract_functions(self, content: str) -> List[FunctionInfo]:
        """Extract function declarations."""
        functions = []
        
        # Pattern for function declarations and arrow functions
        patterns = [
            # function name(params): returnType
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\((.*?)\)(?:\s*:\s*(\w+))?',
            # const name = (params): returnType => 
            r'(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\((.*?)\)(?:\s*:\s*(\w+))?\s*=>',
            # const name = async (params): returnType =>
            r'(?:export\s+)?const\s+(\w+)\s*=\s*async\s*\((.*?)\)(?:\s*:\s*(\w+))?\s*=>',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                name = match.group(1)
                params_str = match.group(2)
                return_type = match.group(3) if len(match.groups()) > 2 else None
                
                # Parse parameters
                parameters = []
                if params_str.strip():
                    for param in params_str.split(','):
                        parameters.append(param.strip())
                
                # Estimate line number
                line_number = content[:match.start()].count('\n') + 1
                
                # Check if async
                is_async = 'async' in content[max(0, match.start()-50):match.start()]
                
                functions.append(FunctionInfo(
                    name=name,
                    parameters=parameters,
                    return_type=return_type,
                    docstring=None,  # Would need JSDoc parsing
                    line_number=line_number,
                    is_async=is_async
                ))
        
        return functions
    
    def _extract_classes(self, content: str) -> List[ClassInfo]:
        """Extract class declarations."""
        classes = []
        
        # Pattern for class declarations
        pattern = r'(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?'
        
        for match in re.finditer(pattern, content):
            name = match.group(1)
            base_class = match.group(2)
            base_classes = [base_class] if base_class else []
            
            line_number = content[:match.start()].count('\n') + 1
            
            # Extract methods (simplified - would need proper parsing for accuracy)
            methods = []
            
            classes.append(ClassInfo(
                name=name,
                base_classes=base_classes,
                methods=methods,
                docstring=None,
                line_number=line_number
            ))
        
        return classes
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        imports = []
        
        # Pattern for ES6 imports
        patterns = [
            r'import\s+.*?\s+from\s+[\'"].*?[\'"]',
            r'import\s+[\'"].*?[\'"]',
            r'const\s+.*?\s+=\s+require\([\'"].*?[\'"]\)',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                imports.append(match.group(0))
        
        return imports
