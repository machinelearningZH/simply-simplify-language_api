import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from config import load_settings
from converter.data_converter import DataConverter
from logger import logger
from model.structured_data import Payload
from simplifier.core import ModelInvocationError, ModelResponseError, Simplifier

settings = load_settings()
app = FastAPI()

if settings.cors_allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=True,
        allow_methods=list(settings.cors_allowed_methods),
        allow_headers=list(settings.cors_allowed_headers),
    )


# Dependency injection.
def get_simplifier() -> Simplifier:
    return Simplifier(settings)


def require_api_token(authorization: Annotated[str | None, Header()] = None) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.removeprefix("Bearer ").strip()
    if not secrets.compare_digest(token, settings.api_auth_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def select_model(model: str | None) -> str:
    selected_model = model or settings.model_name
    if selected_model not in settings.allowed_models:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported model",
        )
    return selected_model


def validate_input_size(payload: Payload) -> None:
    total_chars = sum(len(item.text) for item in payload.data)
    if total_chars > settings.max_chars_input:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=(
                f"Input contains {total_chars} characters; maximum is {settings.max_chars_input}"
            ),
        )


@app.post("/", dependencies=[Depends(require_api_token)])
def simplify(payload: Payload, simplifier: Simplifier = Depends(get_simplifier)):
    model = select_model(payload.model)
    validate_input_size(payload)
    logger.info("Simplifying request with model %s", model)
    converter = DataConverter(payload, simplifier, model)

    try:
        return converter.simplify()
    except ModelInvocationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Model provider request failed",
        ) from exc
    except ModelResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Model provider response was invalid",
        ) from exc
