# ADK 2.0 Multi-Agent Orchestrator (Ollama)

A multi-agent system built with [Google ADK](https://google.github.io/adk-docs/) 2.x that runs on a **self-hosted Ollama model** (`gemma4:12b`) through [LiteLLM](https://docs.litellm.ai/). A root agent coordinates specialist sub-agents and delegates work to them.

## Architecture

```
root_agent (orchestrator)
├── research_agent   – Wikipedia search tool (web_search)
├── validator_agent  – critically reviews research for accuracy
├── poem_writer_agent – writes poems; get_poem_form_rules tool (haiku, sonnet, ...)
└── news_agent       – Serper news search, current date/time, IP-based location
```

| Path | Purpose |
|------|---------|
| `orchestrator/agent.py` | Root agent; loads and wires up the sub-agents |
| `orchestrator/*-agent/agent.py` | Individual specialist agents |
| `orchestrator/.env` | Local secrets/config (git-ignored) |
| `test-ollama.py` | Quick connectivity check against the Ollama endpoint |
| `clear.py` | Removes all `__pycache__` folders |

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- A running Ollama server with the `gemma4:12b` model pulled, reachable via URL (e.g. exposed with ngrok)
- (Optional) a [Serper](https://serper.dev) API key for the news agent

## Setup

```bash
uv sync
```

Create `orchestrator/.env` (see `orchestrator/.env.example`):

```env
OLLAMA_API_BASE=https://your-ollama-host.ngrok-free.app
SERPER_API_KEY=your_serper_key
```

`OLLAMA_API_BASE` must be the base URL only (no trailing slash, no `/api/chat`). Free ngrok URLs change on every restart, so update it when they do.

## Run

```bash
# Web UI
uv run adk web

# Terminal chat
uv run adk run orchestrator
```

Run these from the repository root. Example prompts:

- "Write a haiku about monsoon rain"
- "Research the history of the Eiffel Tower and validate the findings"
- "What's the latest news near me?"

## Test the Ollama connection

```bash
OLLAMA_API_BASE=https://your-host.ngrok-free.app uv run python test-ollama.py
```

## Notes

- All agents send the `ngrok-skip-browser-warning` header to bypass ngrok's free-tier interstitial.
- The research agent uses the Wikipedia API (no key needed); the news agent needs `SERPER_API_KEY`.
- Never commit `.env` files — they are git-ignored.
