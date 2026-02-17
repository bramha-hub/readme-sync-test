"""
Demo script to test README-Sync parsers locally.
"""
from src.parsers import ParserFactory


def demo_python_parsing():
    """Demonstrate Python AST parsing."""
    print("=" * 60)
    print("DEMO: Python AST Parsing")
    print("=" * 60)
    
    code = '''
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

async def fetch_api(url: str) -> dict:
    """Fetch data from API."""
    return {}

class Calculator:
    """A simple calculator class."""
    
    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y
'''
    
    factory = ParserFactory()
    analysis = factory.parse_file("demo.py", code)
    
    print(f"\n📄 File: {analysis.filepath}")
    print(f"🔤 Language: {analysis.language}")
    
    print(f"\n📦 Functions ({len(analysis.functions)}):")
    for func in analysis.functions:
        async_marker = "[async] " if func.is_async else ""
        params = ", ".join(func.parameters)
        return_type = f" -> {func.return_type}" if func.return_type else ""
        print(f"  • {async_marker}{func.name}({params}){return_type}")
        if func.docstring:
            print(f"    └─ {func.docstring}")
    
    print(f"\n🏗️  Classes ({len(analysis.classes)}):")
    for cls in analysis.classes:
        print(f"  • {cls.name}")
        if cls.docstring:
            print(f"    └─ {cls.docstring}")
        for method in cls.methods:
            params = ", ".join(method.parameters)
            print(f"    ├─ {method.name}({params})")


def demo_javascript_parsing():
    """Demonstrate JavaScript parsing."""
    print("\n" + "=" * 60)
    print("DEMO: JavaScript Parsing")
    print("=" * 60)
    
    code = '''
export function greet(name) {
    return `Hello, ${name}!`;
}

export async function loadUser(userId) {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
}

export class UserService {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
    }
    
    async getUser(id) {
        return fetch(`${this.apiUrl}/users/${id}`);
    }
}
'''
    
    factory = ParserFactory()
    analysis = factory.parse_file("demo.js", code)
    
    print(f"\n📄 File: {analysis.filepath}")
    print(f"🔤 Language: {analysis.language}")
    
    print(f"\n📦 Functions ({len(analysis.functions)}):")
    for func in analysis.functions:
        async_marker = "[async] " if func.is_async else ""
        params = ", ".join(func.parameters)
        print(f"  • {async_marker}{func.name}({params})")
    
    print(f"\n🏗️  Classes ({len(analysis.classes)}):")
    for cls in analysis.classes:
        print(f"  • {cls.name}")


def demo_prompt_building():
    """Demonstrate prompt building."""
    print("\n" + "=" * 60)
    print("DEMO: Prompt Building")
    print("=" * 60)
    
    from src.prompt_builder import PromptBuilder
    
    builder = PromptBuilder()
    
    # Simulate a simple scenario
    current_readme = "# My Project\n\nA simple calculator."
    file_changes = [{
        'filepath': 'calc.py',
        'diff': '+def multiply(a, b):\n+    return a * b'
    }]
    
    # Create a mock analysis
    from src.parsers.base import FileAnalysis, FunctionInfo
    
    func = FunctionInfo(
        name="multiply",
        parameters=["a", "b"],
        return_type=None,
        docstring="Multiply two numbers",
        line_number=1
    )
    
    analysis = FileAnalysis(
        filepath="calc.py",
        language="python",
        functions=[func],
        classes=[],
        imports=[],
        module_docstring=None
    )
    
    prompt = builder.build_update_prompt(
        current_readme=current_readme,
        file_changes=file_changes,
        parsed_files=[analysis]
    )
    
    print("\n📝 Generated Prompt Preview (first 500 chars):")
    print("-" * 60)
    print(prompt[:500] + "...")
    print("-" * 60)
    print(f"\n✓ Full prompt length: {len(prompt)} characters")


if __name__ == "__main__":
    print("\n🚀 README-Sync Parser Demo\n")
    
    demo_python_parsing()
    demo_javascript_parsing()
    demo_prompt_building()
    
    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Set GEMINI_API_KEY environment variable")
    print("  2. Initialize a git repository")
    print("  3. Run: python src/sync_readme.py")
    print()
