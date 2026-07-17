import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
repo_root = str(REPO_ROOT)
if repo_root in sys.path:
    sys.path.remove(repo_root)
sys.path.insert(0, repo_root)

# Application settings are loaded during test collection, before fixtures can isolate them.
# Set the complete API test environment explicitly so a developer's shell or .env cannot leak in.
os.environ.update(
    {
        "OPENROUTER_API_KEY": "test-openrouter-key",
        "OPENROUTER_BASE_URL": "https://provider.example/api/v1",
        "MODEL_NAME": "test-model",
        "MAX_TOKENS": "256",
        "MAX_CHARS_INPUT": "100000",
        "OPENROUTER_TIMEOUT_SECONDS": "60",
        "OPENROUTER_MAX_RETRIES": "2",
        "API_AUTH_TOKEN": "test-api-token",
        "ALLOWED_MODELS": "test-model,other-model",
        "CORS_ALLOWED_ORIGINS": "https://client.example",
        "CORS_ALLOWED_METHODS": "POST",
        "CORS_ALLOWED_HEADERS": "Authorization,Content-Type",
        "CORS_ALLOW_CREDENTIALS": "false",
        "LOG_LEVEL": "INFO",
    }
)
os.environ.pop("CONFIG_PATH", None)
for name in (
    "PROMPT_SYSTEM_MESSAGE_ES",
    "PROMPT_SYSTEM_MESSAGE_LS",
    "PROMPT_RULES_ES",
    "PROMPT_RULES_LS",
    "PROMPT_REWRITE_COMPLETE",
    "PROMPT_TEMPLATE_ES",
    "PROMPT_TEMPLATE_LS",
):
    os.environ.pop(name, None)


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    import fastapi_app

    fastapi_app.app.dependency_overrides.clear()
    yield
    fastapi_app.app.dependency_overrides.clear()
