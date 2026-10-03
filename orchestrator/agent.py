import importlib

from google.adk.agents.llm_agent import Agent


research_agent = importlib.import_module(
    '.research-agent.agent', package=__package__
).root_agent
validator_agent = importlib.import_module(
    '.validator-agent.agent', package=__package__
).root_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=(
        'Coordinate responses to user questions. Delegate information gathering to the '
        'research agent and critical review to the validator agent when appropriate. '
        'Synthesize their work into a clear, accurate final answer and be transparent '
        'about uncertainty.'
        'You have access to research_agent who has access to google_search and validator_agent who can validate the research. Use them when appropriate.'
    ),

    sub_agents=[research_agent, validator_agent],
)
