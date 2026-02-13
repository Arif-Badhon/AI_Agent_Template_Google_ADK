# 🤖 Agentic AI Project Template (Google ADK + uv)

A production-grade Cookiecutter template for building scalable, autonomous AI agents using **Google's Agent Development Kit (ADK)** and **uv** for blazing-fast dependency management.

This template scaffolds a "Fractal" project structure designed for complex multi-agent systems, separating agent behaviors (`src/agents`) from cognitive architecture (`src/core`).

## 🚀 Features

* **⚡ uv Integration:** Pre-configured `pyproject.toml` for instant dependency resolution and locking.
* **🧠 Cognitive Architecture:** Dedicated modules for `memory`, `planning`, and `reasoning` to support advanced agent patterns (ReAct, ToT).
* **🏗️ Production Structure:** clearly separates `configs`, `data`, and source code (`src`) to avoid "script sprawl."
* **🔒 Security First:** Pre-configured `.gitignore` and `.env.example` to prevent API key leaks.
* **🐳 Docker Ready:** Includes a `Dockerfile` for containerizing your agents for cloud deployment.
* **✅ Automated Setup:** Post-generation hooks automatically initialize Git and install dependencies.

## 📂 Project Structure

Your generated project will look like this:

```text
my_agent_project/
├── config/                 # Configuration files (YAML) for agents & models
├── data/                   # Local storage for logs, memory, and knowledge bases
├── src/
│   ├── agents/             # Where your specific agent logic lives (e.g., Reporter, Writer)
│   ├── core/               # Shared cognitive modules (Planner, Memory, Tools)
│   ├── environment/        # Simulation environments for safe testing
│   └── utils/              # Logging, metrics, and helper functions
├── tests/                  # Pytest suite
├── .env.example            # Template for environment variables (API keys)
├── pyproject.toml          # Python dependencies (managed by uv)
└── Dockerfile              # Deployment configuration
```

## 🛠️ Prerequisites

Install **uv** (The modern Python package manager):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install **cookiecutter**:

```bash
uv tool install cookiecutter
```

## ⚡ Quick Start

### 1. Generate a New Project

Run this single command to pull the template and scaffold your new agent:

```bash
# Generate from GitHub (Recommended)
uvx cookiecutter https://github.com/YOUR_USERNAME/ai-agent-template.git

# OR Generate locally if you cloned this repo
uvx cookiecutter .
```

You will be prompted for:

* `project_name`: (e.g., "Newsroom Agents")
* `author_name`: (Your Name)

### 2. Configure Environment

Enter your new project folder and set up your API keys:

```bash
cd newsroom_agents
cp .env.example .env
nano .env  # Add your GOOGLE_API_KEY here
```

### 3. Run the Base Agent

The project comes with a pre-configured "Hello World" agent to verify your setup.

```bash
uv run src/agents/base_agent.py
```

## 📦 Dependency Management

This project uses **uv** for all package management.

* Add a package: `uv add pandas`
* Run a script: `uv run python script.py`
* Sync dependencies: `uv sync`

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have ideas for improving the agent architecture.

## 📄 License

MIT
