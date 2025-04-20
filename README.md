# MCP Client

The MCP Client is a Python-based application that interacts with the Model Context Protocol (MCP) server to process user queries using various AI models and tools.

## Features
- Supports multiple AI models: OpenAI (GPT-4), Claude, and Gemini.
- Connects to MCP servers to utilize available tools.
- Interactive chat loop for user queries.
- Handles tool calls dynamically based on server-provided tools.

## Requirements
- Python 3.13 or higher
- Required dependencies listed in `pyproject.toml`

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-client
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your API keys:
   ```env
   OPENAI_API_KEY=<your_openai_api_key>
   ANTHROPIC_API_KEY=<your_anthropic_api_key>
   GEMINI_API_KEY=<your_gemini_api_key>
   ```

## Usage
Run the client with the desired server script:

### OpenAI Client
```bash
python openai_client.py <path_to_server_script>
```

### Claude Client
```bash
python claude_client.py <path_to_server_script>
```

### Gemini Client
```bash
python gemini_client.py <path_to_server_script>
```

Replace `<path_to_server_script>` with the path to the MCP server script (e.g., `tool_poisoning.py` or `weather.py`).

## Example Commands
- Start the OpenAI client:
  ```bash
  python openai_client.py "C:/path/to/server_script.py"
  ```
- Start the Claude client:
  ```bash
  python claude_client.py "C:/path/to/server_script.py"
  ```
- Start the Gemini client:
  ```bash
  python gemini_client.py "C:/path/to/server_script.py"
  ```

## Notes
- The OpenAI and Claude client codes have not been tested due to the unavailability of API keys. They might require some tweaks to work properly.

## License
This project is licensed under the MIT License.
