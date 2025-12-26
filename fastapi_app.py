from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from converter.bad_formatting_error import BadFormattingError
from converter.data_converter import DataConverter
from logger import logger
from model.structured_data import Payload
from simplifier.core import Simplifier

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
