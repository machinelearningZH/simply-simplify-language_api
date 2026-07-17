from openai import OpenAI, OpenAIError
from pydantic import ValidationError

from config import Settings, load_settings
from logger import logger
from model.structured_data import SimplificationResponse


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
        base_url=settings.openrouter_base_url,
        api_key=settings.openrouter_api_key,
        default_headers=default_headers or None,
        timeout=settings.openrouter_timeout_seconds,
        max_retries=settings.openrouter_max_retries,
    )


class Simplifier:
    def __init__(self, settings: Settings | None = None, client: OpenAI | None = None) -> None:
        self.settings = settings or load_settings()
        self.client = client or create_openai_client(self.settings)

    def close(self) -> None:
        self.client.close()

    def create_prompt(
        self,
        text: str,
        leichte_sprache: bool = False,
    ) -> tuple[str, str]:
        """Create prompt and system message."""
        if leichte_sprache:
            final_prompt = self.settings.prompts.template_ls.format(
                rules=self.settings.prompts.rules_ls,
                completeness=self.settings.prompts.rewrite_complete,
                prompt=text,
            )
            system = self.settings.prompts.system_message_ls
        else:
            final_prompt = self.settings.prompts.template_es.format(
                rules=self.settings.prompts.rules_es,
                completeness=self.settings.prompts.rewrite_complete,
                prompt=text,
            )
            system = self.settings.prompts.system_message_es
        return final_prompt, system

    def invoke_model(
        self,
        text: str,
        leichte_sprache: bool,
        model: str | None = None,
    ) -> SimplificationResponse:
        """Invoke LLM via OpenRouter."""
        final_prompt, system = self.create_prompt(text, leichte_sprache)
        try:
            message = self.client.beta.chat.completions.parse(
                model=model or self.settings.model_name,
                max_tokens=self.settings.max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": final_prompt},
                ],
                response_format=SimplificationResponse,
            )
        except ValidationError as exc:
            logger.warning("Model response failed schema validation", exc_info=True)
            raise ModelResponseError("Model response did not match the expected schema") from exc
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

    def simplify_text(
        self,
        text: str,
        leichte_sprache: bool = False,
        model: str | None = None,
    ) -> SimplificationResponse:
        """Simplify text."""
        return self.invoke_model(text, leichte_sprache, model)
