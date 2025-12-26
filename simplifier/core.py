from dotenv import load_dotenv
from openai import OpenAI

from config import (
    MAX_TOKENS,
    MODEL_NAME,
    OPENROUTER_API_KEY,
    SITE_NAME,
    SITE_URL,
)
from model.structured_data import SimplificationResponse
from simplifier.utils_prompts import (
    OPENAI_TEMPLATE_ES,
    OPENAI_TEMPLATE_LS,
    REWRITE_COMPLETE,
    RULES_ES,
    RULES_LS,
    SYSTEM_MESSAGE_ES,
    SYSTEM_MESSAGE_LS,
)

OPENAI_TEMPLATES = [
    OPENAI_TEMPLATE_ES,
    OPENAI_TEMPLATE_LS,
]

# ---------------------------------------------------------------
# Constants

load_dotenv()

# Initialize OpenRouter client
default_headers = {}
if SITE_URL:
    default_headers["HTTP-Referer"] = SITE_URL
if SITE_NAME:
    default_headers["X-Title"] = SITE_NAME

openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers=default_headers if default_headers else None,
)

MAX_TOKENS = int(MAX_TOKENS)

# From our testing we derive a sensible temperature of 0.5 as a good trade-off between creativity and coherence.
# Adjust this to your needs.
TEMPERATURE = 0.5

# Maximum number of characters for the input text.
# This is way below the context window size of the GPT-4o model. Adjust to your needs.
MAX_CHARS_INPUT = 100_000


class Simplifier:
    def __init__(self):
        self.model = MODEL_NAME

    def set_model(self, value):
        if not isinstance(value, str):
            raise ValueError("Model must be a string")
        self.model = value

    def create_prompt(self, text, prompt_es, prompt_ls, leichte_sprache=False):
        """Create prompt and system message."""
        if leichte_sprache:
            final_prompt = prompt_ls.format(
                rules=RULES_LS, completeness=REWRITE_COMPLETE, prompt=text
            )
            system = SYSTEM_MESSAGE_LS
        else:
            final_prompt = prompt_es.format(
                rules=RULES_ES, completeness=REWRITE_COMPLETE, prompt=text
            )
            system = SYSTEM_MESSAGE_ES
        return final_prompt, system

    def invoke_model(self, text, leichte_sprache):
        """Invoke LLM via OpenRouter."""
        final_prompt, system = self.create_prompt(text, *OPENAI_TEMPLATES, leichte_sprache)
        try:
            message = openai_client.beta.chat.completions.parse(
                model=self.model,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": final_prompt},
                ],
                response_format=SimplificationResponse,
            )
            return True, message.choices[0].message.parsed
        except Exception as e:
            from logger import logger

            logger.error(f"Error invoking model via OpenRouter: {e}")
            return False, e

    def simplify_text(self, text, leichte_sprache=False):
        """Simplify text."""
        if len(text) > MAX_CHARS_INPUT:
            return f"Error: Dein Text ist zu lang für das System. Bitte kürze ihn auf {MAX_CHARS_INPUT} Zeichen oder weniger."
        success, response = self.invoke_model(text, leichte_sprache)
        if success:
            return response
        else:
            return response
