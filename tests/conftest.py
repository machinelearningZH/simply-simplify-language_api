import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
repo_root = str(REPO_ROOT)
if repo_root in sys.path:
    sys.path.remove(repo_root)
sys.path.insert(0, repo_root)

os.environ.setdefault("OPENROUTER_API_KEY", "test-openrouter-key")
os.environ.setdefault("MODEL_NAME", "test-model")
os.environ.setdefault("MAX_TOKENS", "256")
os.environ.setdefault("API_AUTH_TOKEN", "test-api-token")
os.environ.setdefault("ALLOWED_MODELS", "test-model,other-model")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "https://client.example")


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    import fastapi_app

    fastapi_app.app.dependency_overrides.clear()
    yield
    fastapi_app.app.dependency_overrides.clear()
