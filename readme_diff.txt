diff --git a/README.md b/README.md
index 5562050..c5971ec 100644
--- a/README.md
+++ b/README.md
@@ -13,8 +13,25 @@ README-Sync is a GitHub Action that uses AI to keep your documentation in sync w
 -   **🌐 Multi-Language**: Supports Python, JavaScript, and TypeScript out of the box
 -   **⚙️ Configurable**: Customize which files to monitor, what to update, and how the AI behaves
 
-## 🚀 Quick Start
+## 🤖 Agent Examples
 
-### 1. Add to Your Repository
+README-Sync can also be used to document projects that leverage advanced AI capabilities, or it can be extended to include agent-based functionalities. This section introduces an example of an interactive AI agent built using the `MCPAgent` framework, demonstrating how such complex systems can be developed and integrated.
 
-Create `.github/workflows/readme-sync.yml`:
\ No newline at end of file
+### `agent.py`: Interactive Chat with Memory
+
+The `agent.py` module provides a simple, interactive command-line chat application using `MCPAgent` with built-in conversation memory. This allows the agent to maintain context across multiple turns in a conversation, making interactions more natural and coherent.
+
+**Purpose:**
+To showcase the integration of `MCPAgent` with conversation memory, demonstrating how to build a stateful AI assistant. It leverages the `MCPClient` for interaction with an underlying agent server (e.g., `playwright-mcp`) and `ChatGroq` as the Large Language Model for generating responses.
+
+**Key Components:**
+
+*   **`MCPAgent`**: An agent designed for multi-turn conversations, now with enhanced memory capabilities to retain context.
+*   **`MCPClient`**: The client used to establish and manage sessions with the underlying agent server, facilitating communication between the application and the agent.
+*   **`ChatGroq`**: The LLM provider used for generating intelligent and context-aware responses from the agent.
+
+**Usage Example:**
+
+To run the interactive chat, ensure you have your `GROQ_API_KEY` set as an environment variable and a `mcp.json` configuration file present in your project root or specified path.
+
+First, install the necessary dependencies:
\ No newline at end of file
