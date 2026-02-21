"""
Test the LLM client with a real API call.
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Set API key
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', '')

from llm_client import LLMClient

print("🧪 Testing LLM Client with Gemini API...\n")

# Initialize client
client = LLMClient(model="models/gemini-2.5-flash")
print("✓ Client initialized")

# Test with a simple prompt
prompt = """Update the following README to include the new function:

Current README:
# Calculator
A simple calculator library.

New Function:
def multiply(a: int, b: int) -> int:
    \"\"\"Multiply two numbers.\"\"\"
    return a * b

Please update the README to document this new function.
"""

print("\n📤 Sending request to Gemini...")
response = client.generate_documentation_update(prompt)

print("\n📥 Response received:")
print("=" * 60)
print(response)
print("=" * 60)

print("\n✅ Test completed successfully!")
