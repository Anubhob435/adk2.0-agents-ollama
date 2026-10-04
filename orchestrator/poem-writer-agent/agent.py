import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Ngrok base URL of the remote Ollama server (no trailing slash, no /api/chat).
# Override with OLLAMA_API_BASE in orchestrator/.env since free ngrok URLs change.
OLLAMA_API_BASE = os.getenv(
    'OLLAMA_API_BASE', 'https://6699-136-85-135-191.ngrok-free.app'
)

POEM_FORMS = {
    'haiku': '3 lines with 5, 7, 5 syllables. No rhyme required; focus on nature or a moment.',
    'sonnet': '14 lines in iambic pentameter (10 syllables each), rhyme scheme ABAB CDCD EFEF GG.',
    'limerick': '5 lines, rhyme scheme AABBA. Lines 1, 2, 5 are longer; lines 3, 4 shorter. Humorous tone.',
    'couplet': '2 rhyming lines of similar length.',
    'free verse': 'No fixed rhyme or meter; rely on imagery and line breaks.',
}


def get_poem_form_rules(form: str) -> dict:
    """Looks up the structural rules for a poem form.

    Args:
        form: Name of the poem form, e.g. 'haiku', 'sonnet', 'limerick'.

    Returns:
        A dict with the form name and its rules, or the list of supported forms.
    """
    rules = POEM_FORMS.get(form.strip().lower())
    if rules is None:
        return {'status': 'unknown_form', 'supported_forms': sorted(POEM_FORMS)}
    return {'status': 'ok', 'form': form, 'rules': rules}


root_agent = Agent(
    model=LiteLlm(
        model='ollama_chat/gemma4:12b',
        api_base=OLLAMA_API_BASE,
        # Avoids the ngrok free-tier interstitial page.
        extra_headers={'ngrok-skip-browser-warning': 'true'},
    ),
    name='poem_writer_agent',
    description='Writes original poems on any topic, theme, or style requested.',
    instruction=(
        'You are a poet. Write an original poem based on the topic, mood, or form the '
        'user requests (e.g. haiku, sonnet, free verse). Give the poem a title, keep '
        'imagery vivid, and output only the poem unless asked for commentary. '
        'If the user asks for a specific form, call get_poem_form_rules first and follow it.'
    ),
    tools=[get_poem_form_rules],
)
