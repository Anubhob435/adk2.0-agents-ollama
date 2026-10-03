from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='validator_agent',
    description='Validates research for accuracy, completeness, and unsupported claims.',
    instruction=(
        'Review the supplied research or draft answer critically. Check factual claims, '
        'identify missing context and contradictions, distinguish evidence from inference, '
        'and report corrections or uncertainty clearly. Do not approve unsupported claims.'
    ),
)
