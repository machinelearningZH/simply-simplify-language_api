from typing import Dict

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

from model.TextPayload import TextPayload
from simplifier.core import Simplifier

from converter.BadFormattingError import BadFormattingError
from converter.JsonConverter import JsonConverter
from converter.TextConverter import TextConverter

from logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency injection
def get_simplifier():
    return Simplifier()


@app.post("/")
async def simplify(payload: TextPayload, simplifier: Simplifier = Depends(get_simplifier)):
    model = payload.model if payload.model else None
    if payload.format == 'json':
        if isinstance(payload.data, Dict):
            logger.info(f"Convert json")
            converter = JsonConverter(payload, simplifier, model)
            return converter.simplify()
        else:
            raise BadFormattingError(500)
    else:
        if isinstance(payload.data, str):
            logger.info(f"Convert text")
            converter = TextConverter(payload, simplifier, model)
            return converter.simplify()
        else:
            raise BadFormattingError(500)
