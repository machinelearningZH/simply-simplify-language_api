from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Union, Optional, Dict
from pydantic import BaseModel, Json

from converter.BadFormattingError import BadFormattingError
from converter.JsonConverter import JsonConverter
from converter.TextConverter import TextConverter

from logger import logger
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextPayload(BaseModel):
    data: Union[str, dict] = None
    leichte_sprache: bool
    format: str
    path: Optional[str] = None
    root: Optional[str] = None


@app.post("/")
async def simplify(payload: TextPayload):
    logger.info(payload.format)
    if payload.format == 'json':
        logger.info(f"Convert json")

        if isinstance(payload.data, Dict):
            converter = JsonConverter(payload.data, payload.path, payload.root, bool(payload.leichte_sprache))
            return converter.simplify()
        else:
            raise BadFormattingError(500)
    else:
        logger.info(f"Convert text")
        converter = TextConverter(payload.data, bool(payload.leichte_sprache))
        return converter.simplify()
