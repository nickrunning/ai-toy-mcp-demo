# 🤖 MCP AI 玩具演示项目

[[English]](README_EN.md)

这是一个基于 Python 的 **Model Context Protocol (MCP)** 深度演示项目。该项目包含一个模拟的 AI 玩具服务端，以及一个集成了 **OpenAI 兼容大模型（如通义千问 Qwen）** 的高性能客户端。

## ✨ 核心特性

- **🚀 一键启动**：通过 `start.sh` 实现自动化环境配置与依赖管理。
- **🛠️ MCP 服务端**：模拟具备多种物理动作与信息查询能力的 AI 玩具。
- **🧠 增强型 LLM 客户端**：使用 OpenAI SDK 完美集成 Qwen/DashScope。
- **📟 类 Shell 交互体验**：基于 `prompt_toolkit` 实现支持输入历史回溯（上下键）的交互终端。
- **📝 上下文持久化**：自动保存与加载对话历史，保持会话连续性。
- **🎯 精准工具调用**：通过优化的 System Prompt 强制模型优先调用实时工具，而非依赖内部陈旧知识。

## 🏗️ 项目结构

- `server.py`: 暴露玩具能力（动作、声音、天气、状态）的 MCP 服务端。
- `client.py`: 处理 LLM 交互、MCP 会话管理及 CLI 界面的核心逻辑。
- `start.sh`: 环境初始化与项目启动的一键式脚本。
- `requirements.txt`: Python 依赖项列表。

## 🚦 快速上手

### 1. 配置环境变量
设置您的 API 密钥与 Endpoint（以通义千问/DashScope 为例）：

```bash
export OPENAI_API_KEY="您的_API_KEY"
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_MODEL_NAME="qwen-plus"
```

### 2. 启动演示
运行自动化启动脚本：

```bash
./start.sh
```
*该脚本会自动创建虚拟环境、安装依赖并启动客户端。*

## 🕹️ 交互示例

连接成功后，尝试输入以下指令：
- `"杭州天气怎么样？"` (触发 `get_weather` 工具)
- `"做一个空翻"` (触发 `perform_move`)
- `"查看电池电量和设备状态"` (触发 `get_battery_status` 与 `get_device_state`)
- `"播放一点音乐"` (触发 `play_sound`)

## 🛠️ 已接入的 MCP 工具

| 工具名称 | 功能描述 |
| :--- | :--- |
| `perform_move` | 执行物理动作（跳舞、招手、空翻）。 |
| `play_sound` | 播放特定声音（犬吠、蜂鸣、音乐）。 |
| `get_battery_status` | 查询当前电池电量及充电状态。 |
| `get_device_state` | 返回玩具的完整内部状态信息。 |
| `get_ip` | 获取设备的当前网络地址。 |
| `get_weather` | 获取指定城市的实时天气数据（模拟）。 |

---
*本项目专注于 Model Context Protocol 的可扩展性与交互性能。*
