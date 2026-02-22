# README-Sync 🔄

**Automatically update your documentation when code changes.**

README-Sync is a GitHub Action that uses AI to keep your documentation in sync with your codebase. It analyzes code changes using AST parsing, generates accurate documentation updates with LLMs, and creates pull requests for review.

## ✨ Features

-   **🔬 Structure-Aware Analysis**: Uses AST parsing (not regex) to extract exact function signatures, preventing hallucinations
-   **🤖 AI-Powered Updates**: Leverages Google Gemini to generate human-readable documentation. Now with an **expanded context window (up to 16,384 tokens)** for more comprehensive updates and **refined prompt instructions** for higher quality, more structured, and complete documentation output.
-   **🎯 Precision Targeting**: Only updates technical details that changed, preserving your tone and style
-   **🔄 Automated PRs**: Creates pull requests instead of direct commits, giving you full control
-   **🌐 Multi-Language**: Supports Python, JavaScript, and TypeScript out of the box
-   **⚙️ Configurable**: Customize which files to monitor, what to update, and how the AI behaves

## 🤖 Agent Examples

README-Sync can also be used to document projects that leverage advanced AI capabilities, or it can be extended to include agent-based functionalities. This section introduces an example of an interactive AI agent built using the `MCPAgent` framework, demonstrating how such complex systems can be developed and integrated.

### `agent.py`: Interactive Chat with Memory

The `agent.py` module provides a simple, interactive command-line chat application using `MCPAgent` with built-in conversation memory. This allows the agent to maintain context across multiple turns in a conversation, making interactions more natural and coherent.

**Purpose:**
To showcase the integration of `MCPAgent` with conversation memory, demonstrating how to build a stateful AI assistant. It leverages the `MCPClient` for interaction with an underlying agent server (e.g., `playwright-mcp`) and `ChatGroq` as the Large Language Model for generating responses.

**Key Components:**

*   **`MCPAgent`**: An agent designed for multi-turn conversations, now with enhanced memory capabilities to retain context.
*   **`MCPClient`**: The client used to establish and manage sessions with the underlying agent server, facilitating communication between the application and the agent.
*   **`ChatGroq`**: The LLM provider used for generating intelligent and context-aware responses from the agent.

**Usage Example:**

To run the interactive chat, ensure you have your `GROQ_API_KEY` set as an environment variable and a `mcp.json` configuration file present in your project root or specified path.

First, install the necessary dependencies: