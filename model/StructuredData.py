from typing import Optional, List
from pydantic import BaseModel


class SimplificationText(BaseModel):
    text: str


class SimplificationResponse(BaseModel):
    simplifications: list[SimplificationText]


class TextPayload(BaseModel):
    data: List[SimplificationText] = None
    leichte_sprache: bool
    model: Optional[str] = None
