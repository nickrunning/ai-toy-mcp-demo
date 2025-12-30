# MCP Demo: AI Toy Controller

This project demonstrates a Model Context Protocol (MCP) server and client using Gemini 2.0 Flash Expedition (or 2.5 Flash if available).

## Structure

*   `server.py`: The MCP Server representing an AI Toy with capabilities (move, play sound, check battery).
*   `client.py`: The MCP Client that connects to the server and uses Gemini to translate natural language into tool calls.
*   `requirements.txt`: Python dependencies.

## Setup

1.  **Create and Activate Virtual Environment** (Already done if you let the agent run it):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Demo

1.  **Set your Google API Key**:
    ```bash
    export GOOGLE_API_KEY="your_actual_api_key_here"
    ```

2.  **Run the Client**:
    ```bash
    python client.py
    ```

3.  **Interact**:
    *   Type messages like "Do a backflip", "Check battery", "Play some jazz".
    *   The system will use Gemini to decide which tool to call on the server.
    *   Conversation history is saved to `chat_history.txt`.

## Troubleshooting

*   If you see connection errors, ensure `server.py` is in the same directory and executable by the python interpreter.
*   If you see API errors, check your `GOOGLE_API_KEY`.
