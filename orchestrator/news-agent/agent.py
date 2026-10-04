import json
import urllib.request
from datetime import datetime

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool


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
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone'),
        }
    except Exception as e:  # noqa: BLE001
        return {'status': 'error', 'error': str(e)}


# google_search is a Gemini-only built-in tool, so this agent uses a Gemini model.
root_agent = Agent(
    model='gemini-2.5-flash',
    name='news_agent',
    description='Finds the latest news and current events, aware of the current date, time and location.',
    instruction=(
        'You report current news. First call get_current_datetime so you know today\'s date, '
        'and call get_current_location when the user wants local news or does not specify a '
        'place. Use google_search to find recent articles, prefer the most recent and reliable '
        'sources, and give a concise summary with headlines, dates and source names. '
        'State clearly if no recent news is found.'
    ),
    tools=[
        GoogleSearchTool(bypass_multi_tools_limit=True),
        get_current_datetime,
        get_current_location,
    ],
)
