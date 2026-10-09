# 🗂️ Autonomous File Organizer Agent

> **Note:** This repository is an educational/learning project developed while studying agentic AI workflows and tool-calling mechanisms from scratch (based on foundational concepts from Lane Wagner's course).

A lightweight, autonomous AI agent that organizes local file workspaces using raw OpenAI function/tool calling. Built with plain Python without heavy agent frameworks (like LangChain or CrewAI) to demonstrate how LLM multi-turn loops, tool schemas, and security sandboxing interact under the hood.

---

## ✨ Features

- **Raw Agentic Loop:** Implements an iterative reasoning loop where the LLM requests actions via JSON schemas, Python executes local functions, and results are fed back into the context window.
- **Autonomous Error Recovery:** Errors (e.g., duplicate directories, non-existent files) are passed back to the model as role-tagged tool outputs, enabling the agent to recover, backtrack, or find alternative strategies autonomously.
- **Sandbox Security (`resolve_inside`):** Enforces strict boundary containment using canonical path resolution (`os.path.realpath` and `os.path.commonpath`), preventing path traversal escapes (e.g., `../../`) and symlink attacks.
- **Minimal Dependencies:** Standard library heavy, relying only on `openai` and `python-dotenv`.

---

## 🛠️ How It Works

```
User Prompt ──> LLM ──> Requests Tool Call (JSON Schema)
                 ▲                      │
                 │                      ▼
          Appends Result       Python Executor (call_function)
                 │                      │
                 └──────── Returns Tool Output / Sandbox Errors
```

1. The user supplies an organization goal via CLI (e.g., _"Group all images into an images folder"_).
2. The agent inspects directory contents with `get_files_info`.
3. It plans actions sequentially, creating necessary directories with `create_folder` and moving items with `move_file`.
4. If a command attempts to operate outside the designated workspace (`files/`), the sandbox raises an exception that is returned to the model, prompting it to adjust its plan safely.

---

## 📂 Project Structure

```text
├── files/                  # Sandboxed workspace directory for file operations
│   └── .gitkeep
├── functions/              # Tool implementations & JSON schema definitions
│   ├── __init__.py
│   ├── call_function.py    # Tool dispatcher and JSON schemas for available tools
│   ├── create_folder.py    # Directory creation tool with boundary checking
│   ├── get_files_info.py   # Directory inspection and metadata tool
│   └── move_file.py        # File moving tool with boundary checking
├── utils.py                # Sandbox containment validator (resolve_inside)
├── main.py                 # CLI entry point, argument parser, and multi-turn agent loop
├── pyproject.toml          # Project configuration and dependency definitions
├── .env.example            # Template for required environment variables
├── .gitignore              # Git ignore rules (protects secrets and caches)
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (or [uv](https://docs.astral.sh/uv/))
- An OpenRouter API Key (or OpenAI API key with corresponding base URL)

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Set Up Environment Variables

Copy the template `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using standard `pip`:

```bash
python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

pip install -e .
# Or directly:
pip install openai python-dotenv
```

---

## 💻 Usage

Place some test files into the `files/` workspace directory:

```bash
# Example files inside files/
# On Linux/macOS:
touch files/notes.txt files/photo.png files/data.csv
# On Windows PowerShell:
New-Item -ItemType File files\notes.txt, files\photo.png, files\data.csv
```

Run the agent:

```bash
# Standard run
python main.py "Check the workspace and group text and CSV files into a folder named documents."

# Verbose mode (inspect each tool call and output in real time)
python main.py -v "Group all images into an images folder."

# Using uv
uv run main.py -v "List all files and summarize what you see."
```

---

## 🛡️ Sandbox & Security Demo

Try instructing the agent to break out of the workspace:

```bash
uv run main.py -v "Move photo.png to ../outside_folder"
```

**Observed behavior:**

1. The agent attempts `move_file` targeting `../outside_folder`.
2. `utils.resolve_inside` detects path boundary escape and throws a `PermissionError`.
3. The error string is piped back into the conversation.
4. The agent reads the error, adapts by creating a local `./outside_folder` inside the workspace instead, and safely completes the task.

---

## 📚 What Was Learned

- How tool-calling schemas are represented in OpenAI-compatible JSON specifications.
- Managing multi-turn conversation arrays (`system` $\rightarrow$ `user` $\rightarrow$ `assistant [tool_calls]` $\rightarrow$ `tool`).
- Why state synchronization and serializing Pydantic models matter in agent loops.
- Preventing path traversal and symlink vulnerabilities in file-manipulating tools.
