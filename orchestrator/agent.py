import importlib
import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Ngrok base URL of the remote Ollama server. Override via OLLAMA_API_BASE in .env.
OLLAMA_API_BASE = os.environ['OLLAMA_API_BASE']

research_agent = importlib.import_module(
    '.research-agent.agent', package=__package__
).root_agent
validator_agent = importlib.import_module(
    '.validator-agent.agent', package=__package__
).root_agent
poem_writer_agent = importlib.import_module(
    '.poem-writer-agent.agent', package=__package__
).root_agent
news_agent = importlib.import_module(
    '.news-agent.agent', package=__package__
).root_agent

root_agent = Agent(
    model=LiteLlm(
        model='ollama_chat/gemma4:12b',
        api_base=OLLAMA_API_BASE,
        extra_headers={'ngrok-skip-browser-warning': 'true'},
    ),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=(
        'Coordinate responses to user questions. Delegate information gathering to the '
        'research agent and critical review to the validator agent when appropriate. '
        'Synthesize their work into a clear, accurate final answer and be transparent '
        'about uncertainty.'
        'You have access to research_agent who has access to google_search and validator_agent who can validate the research. Use them when appropriate. '
        'Delegate poem requests to poem_writer_agent. '
        'Delegate news and current-events requests to news_agent.'
    ),

    sub_agents=[research_agent, validator_agent, poem_writer_agent, news_agent],
)
