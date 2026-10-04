import json
import os
import urllib.request
from datetime import datetime

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

OLLAMA_API_BASE = os.getenv(
    'OLLAMA_API_BASE', 'https://6699-136-85-135-191.ngrok-free.app'
)


def search_news(query: str, country: str = 'in', time_range: str = 'w') -> dict:
    """Searches recent news on a topic using the Serper search API.

    Args:
        query: The news topic or search query, e.g. 'apple inc'.
        country: Two-letter country code to localise results, e.g. 'in', 'us'.
        time_range: Recency filter: 'h' past hour, 'd' past day, 'w' past week,
            'm' past month, 'y' past year.

    Returns:
        A dict with the search results (titles, snippets, links, dates), or an error.
    """
    api_key = os.getenv('SERPER_API_KEY')
    if not api_key:
        return {'status': 'error', 'error': 'SERPER_API_KEY is not set'}
    payload = json.dumps({
        'q': query,
        'gl': country,
        'tbs': f'qdr:{time_range}',
    }).encode()
    req = urllib.request.Request(
        'https://google.serper.dev/search',
        data=payload,
        headers={'X-API-KEY': api_key, 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return {'status': 'ok', **json.load(resp)}
    except Exception as e:  # noqa: BLE001
        return {'status': 'error', 'error': str(e)}


def get_current_datetime() -> dict:
    """Gets the current local date, time and timezone of the machine.

    Returns:
        A dict with the ISO timestamp, readable date/time and timezone.
    """
    now = datetime.now().astimezone()
    return {
        'status': 'ok',
        'iso': now.isoformat(),
        'readable': now.strftime('%A, %d %B %Y, %I:%M %p'),
        'timezone': str(now.tzinfo),
    }


def get_current_location() -> dict:
    """Gets the approximate current location (city, region, country) from the IP address.

    Returns:
        A dict with city, region, country and coordinates, or an error.
    """
    try:
        with urllib.request.urlopen('https://ipapi.co/json/', timeout=10) as resp:
            data = json.load(resp)
        return {
            'status': 'ok',
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country_name'),
            'country_code': data.get('country_code'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone'),
        }
    except Exception as e:  # noqa: BLE001
        return {'status': 'error', 'error': str(e)}


root_agent = Agent(
    model=LiteLlm(
        model='ollama_chat/gemma4:12b',
        api_base=OLLAMA_API_BASE,
        extra_headers={'ngrok-skip-browser-warning': 'true'},
    ),
    name='news_agent',
    description='Finds the latest news and current events, aware of the current date, time and location.',
    instruction=(
        'You report current news. First call get_current_datetime so you know today\'s date, '
        'and call get_current_location when the user wants local news or does not specify a '
        'place (use its country_code as the country for search_news). Use search_news to find '
        'recent articles, prefer the most recent and reliable sources, and give a concise '
        'summary with headlines, dates and source names. State clearly if no recent news is found.'
    ),
    tools=[search_news, get_current_datetime, get_current_location],
)
