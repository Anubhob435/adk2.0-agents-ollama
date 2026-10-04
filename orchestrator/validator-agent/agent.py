import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

OLLAMA_API_BASE = os.getenv(
    'OLLAMA_API_BASE', 'https://6699-136-85-135-191.ngrok-free.app'
)

root_agent = Agent(
    model=LiteLlm(
        model='ollama_chat/gemma4:12b',
        api_base=OLLAMA_API_BASE,
        extra_headers={'ngrok-skip-browser-warning': 'true'},
    ),
    name='validator_agent',
    description='Validates research for accuracy, completeness, and unsupported claims.',
    instruction=(
        'Review the supplied research or draft answer critically. Check factual claims, '
        'identify missing context and contradictions, distinguish evidence from inference, '
        'and report corrections or uncertainty clearly. Do not approve unsupported claims.'
    ),
)
