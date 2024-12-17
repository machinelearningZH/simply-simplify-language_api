from typing import Optional, List
from pydantic import BaseModel


class SimplificationText(BaseModel):
    text: str


class SimplificationResponse(BaseModel):
    simplifications: list[SimplificationText]


class Payload(BaseModel):
    data: List[SimplificationText]
    leichte_sprache: Optional[bool] = False
    model: Optional[str] = None
