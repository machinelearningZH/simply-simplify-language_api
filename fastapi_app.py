from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from model.StructuredData import Payload
from simplifier.core import Simplifier

from converter.BadFormattingError import BadFormattingError
from converter.DataConverter import DataConverter

from logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency injection.
def get_simplifier():
    return Simplifier()


@app.post("/")
async def simplify(payload: Payload, simplifier: Simplifier = Depends(get_simplifier)):
    model = payload.model if payload.model else None
    if isinstance(payload.data, list):
        logger.info(f"Simplifying with model {model}")
        converter = DataConverter(payload, simplifier, model)
        return converter.simplify()
    else:
        raise BadFormattingError(500)
