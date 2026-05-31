import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

DEFAULT_CONFIG_PATH = Path("config.yaml")


class ConfigError(RuntimeError):
    """Raised when required runtime configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str
    openrouter_base_url: str
    model_name: str
    max_tokens: int
    api_auth_token: str
    allowed_models: tuple[str, ...]
    cors_allowed_origins: tuple[str, ...]
    cors_allowed_methods: tuple[str, ...]
    cors_allowed_headers: tuple[str, ...]
    site_url: str
    site_name: str
    max_chars_input: int
    openrouter_timeout_seconds: float
    openrouter_max_retries: int


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigError(f"{name} must be set")
    return value.strip()


def _csv_env(name: str) -> tuple[str, ...]:
    raw_value = os.getenv(name, "")
    return tuple(item.strip() for item in raw_value.split(",") if item.strip())


def _get_nested(config: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    value: Any = config
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def _string_setting(
    env_name: str,
    config: dict[str, Any],
    path: tuple[str, ...],
    *,
    required: bool = False,
    default: str = "",
) -> str:
    raw_value = os.getenv(env_name)
    value = raw_value if raw_value is not None else _get_nested(config, path, default)
    if value is None:
        value = ""
    value = str(value).strip()
    if required and not value:
        raise ConfigError(f"{env_name} must be set")
    return value


def _list_setting(
    env_name: str,
    config: dict[str, Any],
    path: tuple[str, ...],
) -> tuple[str, ...]:
    env_value = _csv_env(env_name)
    if env_value:
        return env_value

    value = _get_nested(config, path, ())
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ConfigError(".".join(path) + " must be a list")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _coerce_int(name: str, value: Any, *, minimum: int = 1) -> int:
    try:
        integer_value = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{name} must be an integer") from exc

    if integer_value < minimum:
        raise ConfigError(f"{name} must be at least {minimum}")
    return integer_value


def _int_setting(
    env_name: str,
    config: dict[str, Any],
    path: tuple[str, ...],
    *,
    minimum: int = 1,
) -> int:
    raw_value = os.getenv(env_name)
    value = raw_value if raw_value is not None else _get_nested(config, path)
    if value is None or str(value).strip() == "":
        raise ConfigError(f"{env_name} must be set")
    return _coerce_int(env_name, value, minimum=minimum)


def _float_setting(
    env_name: str,
    config: dict[str, Any],
    path: tuple[str, ...],
    *,
    minimum: float = 0.0,
) -> float:
    raw_value = os.getenv(env_name)
    value = raw_value if raw_value is not None else _get_nested(config, path)
    try:
        float_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{env_name} must be a number") from exc

    if float_value <= minimum:
        raise ConfigError(f"{env_name} must be greater than {minimum}")
    return float_value


def _load_config_file(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise ConfigError(f"{config_path} does not exist")

    try:
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{config_path} is not valid YAML") from exc

    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ConfigError(f"{config_path} must contain a YAML mapping")
    return loaded


def load_settings(
    *,
    config_path: str | Path | None = None,
    load_env_file: bool = True,
) -> Settings:
    if load_env_file:
        load_dotenv()

    config_file = Path(os.getenv("CONFIG_PATH", config_path or DEFAULT_CONFIG_PATH))
    config = _load_config_file(config_file)

    model_name = _string_setting(
        "MODEL_NAME",
        config,
        ("model", "name"),
        required=True,
    )
    allowed_models = _list_setting(
        "ALLOWED_MODELS",
        config,
        ("model", "allowed_models"),
    ) or (model_name,)
    if model_name not in allowed_models:
        raise ConfigError("MODEL_NAME must be included in ALLOWED_MODELS")

    cors_allowed_origins = _list_setting(
        "CORS_ALLOWED_ORIGINS",
        config,
        ("cors", "allowed_origins"),
    )
    if "*" in cors_allowed_origins:
        raise ConfigError("CORS_ALLOWED_ORIGINS must list explicit origins, not '*'")
    cors_allowed_methods = _list_setting(
        "CORS_ALLOWED_METHODS",
        config,
        ("cors", "allowed_methods"),
    )
    cors_allowed_headers = _list_setting(
        "CORS_ALLOWED_HEADERS",
        config,
        ("cors", "allowed_headers"),
    )

    return Settings(
        openrouter_api_key=_required_env("OPENROUTER_API_KEY"),
        openrouter_base_url=_string_setting(
            "OPENROUTER_BASE_URL",
            config,
            ("model", "provider_base_url"),
            required=True,
        ),
        model_name=model_name,
        max_tokens=_int_setting("MAX_TOKENS", config, ("model", "max_tokens")),
        api_auth_token=_required_env("API_AUTH_TOKEN"),
        allowed_models=allowed_models,
        cors_allowed_origins=cors_allowed_origins,
        cors_allowed_methods=cors_allowed_methods,
        cors_allowed_headers=cors_allowed_headers,
        site_url=_string_setting("SITE_URL", config, ("site", "url")),
        site_name=_string_setting("SITE_NAME", config, ("site", "name")),
        max_chars_input=_int_setting(
            "MAX_CHARS_INPUT",
            config,
            ("model", "max_chars_input"),
        ),
        openrouter_timeout_seconds=_float_setting(
            "OPENROUTER_TIMEOUT_SECONDS",
            config,
            ("model", "timeout_seconds"),
        ),
        openrouter_max_retries=_int_setting(
            "OPENROUTER_MAX_RETRIES",
            config,
            ("model", "max_retries"),
            minimum=0,
        ),
    )
