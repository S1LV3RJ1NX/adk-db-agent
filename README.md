# DB Agent using Google ADK

This project is a simple example of how to use Google ADK to create a DB Agent with external MCP server.

## Setup

- Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Install dependencies

```bash
uv sync
```

## Run ADK Web UI

```bash
adk web --host 127.0.0.1 --port 8000 src/agents
```

## Run ADK API Server

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
