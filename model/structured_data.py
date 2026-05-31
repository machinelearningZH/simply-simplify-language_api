from pydantic import BaseModel, ConfigDict, Field


class SimplificationText(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)


class SimplificationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    simplifications: list[SimplificationText]


class Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data: list[SimplificationText] = Field(min_length=1)
    leichte_sprache: bool = False
    model: str | None = Field(default=None, min_length=1)
