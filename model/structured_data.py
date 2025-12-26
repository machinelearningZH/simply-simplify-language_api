from pydantic import BaseModel


class SimplificationText(BaseModel):
    text: str


class SimplificationResponse(BaseModel):
    simplifications: list[SimplificationText]


class Payload(BaseModel):
    data: list[SimplificationText]
    leichte_sprache: bool | None = False
    model: str | None = None
