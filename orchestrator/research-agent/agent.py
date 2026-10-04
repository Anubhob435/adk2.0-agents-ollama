import json
import os
import urllib.parse
import urllib.request

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

OLLAMA_API_BASE = os.getenv(
    'OLLAMA_API_BASE', 'https://6699-136-85-135-191.ngrok-free.app'
)


def web_search(query: str) -> dict:
    """Searches Wikipedia for information relevant to a query.

    Args:
        query: The search query.

    Returns:
        A dict with a list of results (title, snippet, url).
    """
    params = urllib.parse.urlencode({
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srlimit': 5,
        'format': 'json',
    })
    req = urllib.request.Request(
        f'https://en.wikipedia.org/w/api.php?{params}',
        headers={'User-Agent': 'orchestrator-research-agent/1.0'},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception as e:  # noqa: BLE001
        return {'status': 'error', 'error': str(e)}
    results = [
        {
            'title': r['title'],
            'snippet': r['snippet'].replace('<span class="searchmatch">', '').replace('</span>', ''),
            'url': 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(r['title'].replace(' ', '_')),
        }
        for r in data.get('query', {}).get('search', [])
    ]
    return {'status': 'ok', 'results': results}


root_agent = Agent(
    model=LiteLlm(
        model='ollama_chat/gemma4:12b',
        api_base=OLLAMA_API_BASE,
        extra_headers={'ngrok-skip-browser-warning': 'true'},
    ),
    name='research_agent',
    description='Researches questions and gathers relevant, reliable information.',
    instruction=(
        'Research the user\'s request carefully. Use the web_search tool to gather relevant '
        'facts, compare reliable sources when available, and return a concise summary with '
        'source details and any remaining uncertainty. Do not present guesses as facts.'
    ),
    tools=[web_search],
)
