from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model='gemini-2.5-flash',
    name='research_agent',
    description='Researches questions and gathers relevant, reliable information.',
    instruction=(
        'Research the user\'s request carefully. Gather relevant facts, compare reliable '
        'sources when available, and return a concise summary with source details and any '
        'remaining uncertainty. Do not present guesses as facts.'
    ),
        tools=[google_search]
)
