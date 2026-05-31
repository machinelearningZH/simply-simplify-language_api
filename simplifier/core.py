from openai import OpenAI, OpenAIError

from config import Settings, load_settings
from logger import logger
from model.structured_data import SimplificationResponse
from simplifier.utils_prompts import (
    PROMPT_TEMPLATE_ES,
    PROMPT_TEMPLATE_LS,
    REWRITE_COMPLETE,
    RULES_ES,
    RULES_LS,
    SYSTEM_MESSAGE_ES,
    SYSTEM_MESSAGE_LS,
)

PROMPT_TEMPLATES = [
    PROMPT_TEMPLATE_ES,
    PROMPT_TEMPLATE_LS,
]


class ModelInvocationError(RuntimeError):
    """Raised when the model provider request fails."""


class ModelResponseError(RuntimeError):
    """Raised when the model provider returns an unusable response."""


def create_openai_client(settings: Settings) -> OpenAI:
    default_headers = {}
    if settings.site_url:
        default_headers["HTTP-Referer"] = settings.site_url
    if settings.site_name:
        default_headers["X-Title"] = settings.site_name

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
        default_headers=default_headers or None,
        timeout=settings.openrouter_timeout_seconds,
        max_retries=settings.openrouter_max_retries,
    )


class Simplifier:
    def __init__(self, settings: Settings | None = None, client: OpenAI | None = None) -> None:
        self.settings = settings or load_settings()
        self.model = self.settings.model_name
        self.client = client or create_openai_client(self.settings)

    def set_model(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Model must be a string")
        self.model = value

    def create_prompt(
        self,
        text: str,
        prompt_es: str,
        prompt_ls: str,
        leichte_sprache: bool = False,
    ) -> tuple[str, str]:
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

    def invoke_model(self, text: str, leichte_sprache: bool) -> SimplificationResponse:
        """Invoke LLM via OpenRouter."""
        final_prompt, system = self.create_prompt(text, *PROMPT_TEMPLATES, leichte_sprache)
        try:
            message = self.client.beta.chat.completions.parse(
                model=self.model,
                max_tokens=self.settings.max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": final_prompt},
                ],
                response_format=SimplificationResponse,
            )
        except OpenAIError as exc:
            logger.exception("Error invoking model via OpenRouter")
            raise ModelInvocationError("OpenRouter request failed") from exc

        try:
            parsed = message.choices[0].message.parsed
        except (AttributeError, IndexError) as exc:
            raise ModelResponseError("Model response did not include a parsed payload") from exc

        if not isinstance(parsed, SimplificationResponse):
            raise ModelResponseError("Model response did not match the expected schema")

        return parsed

    def simplify_text(self, text: str, leichte_sprache: bool = False) -> SimplificationResponse:
        """Simplify text."""
        return self.invoke_model(text, leichte_sprache)
