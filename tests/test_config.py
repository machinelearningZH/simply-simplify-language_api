from pathlib import Path

from config import load_settings

TUNABLE_ENV_VARS = (
    "MODEL_NAME",
    "OPENROUTER_BASE_URL",
    "ALLOWED_MODELS",
    "MAX_TOKENS",
    "MAX_CHARS_INPUT",
    "OPENROUTER_TIMEOUT_SECONDS",
    "OPENROUTER_MAX_RETRIES",
    "CORS_ALLOWED_ORIGINS",
    "CORS_ALLOWED_METHODS",
    "CORS_ALLOWED_HEADERS",
    "SITE_URL",
    "SITE_NAME",
)


def clear_tunable_env(monkeypatch) -> None:
    for name in TUNABLE_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def test_loads_operator_tunable_settings_from_config_yaml(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
model:
  name: test-model
  provider_base_url: https://provider.example/api/v1
  allowed_models:
    - test-model
    - other-model
  max_tokens: 512
  max_chars_input: 12345
  timeout_seconds: 12.5
  max_retries: 3
cors:
  allowed_origins:
    - https://client.example
  allowed_methods:
    - POST
  allowed_headers:
    - Authorization
    - Content-Type
site:
  url: https://site.example
  name: Test App
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setenv("API_AUTH_TOKEN", "test-api-token")
    clear_tunable_env(monkeypatch)

    settings = load_settings(config_path=config_path, load_env_file=False)

    assert settings.model_name == "test-model"
    assert settings.openrouter_base_url == "https://provider.example/api/v1"
    assert settings.allowed_models == ("test-model", "other-model")
    assert settings.max_tokens == 512
    assert settings.max_chars_input == 12345
    assert settings.openrouter_timeout_seconds == 12.5
    assert settings.openrouter_max_retries == 3
    assert settings.cors_allowed_origins == ("https://client.example",)
    assert settings.cors_allowed_methods == ("POST",)
    assert settings.cors_allowed_headers == ("Authorization", "Content-Type")
    assert settings.site_url == "https://site.example"
    assert settings.site_name == "Test App"
    assert settings.openrouter_api_key == "test-openrouter-key"
    assert settings.api_auth_token == "test-api-token"


def test_environment_overrides_config_yaml(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
model:
  name: test-model
  provider_base_url: https://provider.example/api/v1
  allowed_models:
    - test-model
  max_tokens: 512
  max_chars_input: 12345
  timeout_seconds: 12.5
  max_retries: 3
cors:
  allowed_origins:
    - https://client.example
  allowed_methods:
    - POST
  allowed_headers:
    - Authorization
    - Content-Type
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setenv("API_AUTH_TOKEN", "test-api-token")
    clear_tunable_env(monkeypatch)
    monkeypatch.setenv("MODEL_NAME", "override-model")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://override.example/api/v1")
    monkeypatch.setenv("ALLOWED_MODELS", "override-model,other-model")
    monkeypatch.setenv("MAX_TOKENS", "1024")
    monkeypatch.setenv("CORS_ALLOWED_METHODS", "POST,OPTIONS")
    monkeypatch.setenv("CORS_ALLOWED_HEADERS", "Authorization,Content-Type,X-Trace-Id")

    settings = load_settings(config_path=config_path, load_env_file=False)

    assert settings.model_name == "override-model"
    assert settings.openrouter_base_url == "https://override.example/api/v1"
    assert settings.allowed_models == ("override-model", "other-model")
    assert settings.max_tokens == 1024
    assert settings.cors_allowed_methods == ("POST", "OPTIONS")
    assert settings.cors_allowed_headers == (
        "Authorization",
        "Content-Type",
        "X-Trace-Id",
    )
