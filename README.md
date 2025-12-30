# 🤖 MCP AI Toy Demo

A sophisticated demonstration of the **Model Context Protocol (MCP)** using Python. This project features a simulated AI Toy server and a high-performance client integrated with **OpenAI-compatible LLMs (e.g., Qwen)**.

## ✨ Key Features

- **🚀 One-Click Startup**: Fully automated environment setup and dependency management via `start.sh`.
- **🛠️ MCP Server**: Simulates an AI Toy with multiple physical and informational capabilities.
- **🧠 Advanced LLM Client**: Uses OpenAI SDK for seamless integration with Qwen/DashScope.
- **📟 Shell-like Experience**: Interactive CLI with persistent search history (up/down arrow keys) powered by `prompt_toolkit`.
- **📝 Context Preservation**: Automated saving and loading of chat history for continuity across sessions.
- **🎯 Precise Tooling**: Optimized system prompts ensure the model prioritizes real-time tool usage over internal knowledge.

## 🏗️ Project Structure

- `server.py`: The MCP Server exposing toy capabilities (Move, Sound, Weather, Status).
- `client.py`: The core logic for LLM interaction, MCP session management, and CLI interface.
- `start.sh`: The master control script for environment setup and execution.
- `requirements.txt`: Python dependencies.

## 🚦 Quick Start

### 1. Configure the Environment
Set your API key and endpoint (example for Qwen/DashScope):

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_MODEL_NAME="qwen-plus"
```

### 2. Launch the Demo
Run the automated startup script:

```bash
./start.sh
```
*The script will automatically create a virtual environment, install dependencies, and launch the client.*

## 🕹️ Interaction Examples

Once connected, try commands like:
- `"杭州天气怎么样？"` (Triggers the `get_weather` tool)
- `"做一个空翻"` (Triggers `perform_move`)
- `"查看电池电量和设备状态"` (Triggers `get_battery_status` & `get_device_state`)
- `"播放一点音乐"` (Triggers `play_sound`)

## 🛠️ MCP Tools Exposed

| Tool Name | Description |
| :--- | :--- |
| `perform_move` | Executes movements (dance, wave, backflip). |
| `play_sound` | Plays specific sounds (bark, beep, music). |
| `get_battery_status` | Retrieves current battery % and charging status. |
| `get_device_state` | Returns full internal state of the toy. |
| `get_ip` | Retrieves the device's network address. |
| `get_weather` | Fetches real-time weather data for a specified city. |

---
*Developed with focus on Model Context Protocol extensibility.*
