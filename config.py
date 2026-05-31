import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigError(RuntimeError):
    """Raised when required runtime configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str
    model_name: str
    max_tokens: int
    api_auth_token: str
    allowed_models: tuple[str, ...]
    cors_allowed_origins: tuple[str, ...]
    site_url: str = ""
    site_name: str = ""
    max_chars_input: int = 100_000
    openrouter_timeout_seconds: float = 60.0
    openrouter_max_retries: int = 2


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigError(f"{name} must be set")
    return value.strip()


def _csv_env(name: str) -> tuple[str, ...]:
    raw_value = os.getenv(name, "")
    return tuple(item.strip() for item in raw_value.split(",") if item.strip())


def _int_env(name: str, *, default: int | None = None, minimum: int = 1) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or not raw_value.strip():
        if default is None:
            raise ConfigError(f"{name} must be set")
        value = default
    else:
        try:
            value = int(raw_value)
        except ValueError as exc:
            raise ConfigError(f"{name} must be an integer") from exc

    if value < minimum:
        raise ConfigError(f"{name} must be at least {minimum}")
    return value


def _float_env(name: str, *, default: float, minimum: float = 0.0) -> float:
    raw_value = os.getenv(name)
    if raw_value is None or not raw_value.strip():
        value = default
    else:
        try:
            value = float(raw_value)
        except ValueError as exc:
            raise ConfigError(f"{name} must be a number") from exc

    if value <= minimum:
        raise ConfigError(f"{name} must be greater than {minimum}")
    return value


def load_settings(*, load_env_file: bool = True) -> Settings:
    if load_env_file:
        load_dotenv()

    model_name = _required_env("MODEL_NAME")
    allowed_models = _csv_env("ALLOWED_MODELS") or (model_name,)
    if model_name not in allowed_models:
        raise ConfigError("MODEL_NAME must be included in ALLOWED_MODELS")

    cors_allowed_origins = _csv_env("CORS_ALLOWED_ORIGINS")
    if "*" in cors_allowed_origins:
        raise ConfigError("CORS_ALLOWED_ORIGINS must list explicit origins, not '*'")

    return Settings(
        openrouter_api_key=_required_env("OPENROUTER_API_KEY"),
        model_name=model_name,
        max_tokens=_int_env("MAX_TOKENS"),
        api_auth_token=_required_env("API_AUTH_TOKEN"),
        allowed_models=allowed_models,
        cors_allowed_origins=cors_allowed_origins,
        site_url=os.getenv("SITE_URL", "").strip(),
        site_name=os.getenv("SITE_NAME", "").strip(),
        max_chars_input=_int_env("MAX_CHARS_INPUT", default=100_000),
        openrouter_timeout_seconds=_float_env("OPENROUTER_TIMEOUT_SECONDS", default=60.0),
        openrouter_max_retries=_int_env("OPENROUTER_MAX_RETRIES", default=2, minimum=0),
    )
