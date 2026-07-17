from pydantic import BaseModel, ConfigDict, Field, field_validator


class SimplificationText(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def reject_whitespace_only_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must contain a non-whitespace character")
        return value


class SimplificationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    simplifications: list[SimplificationText] = Field(min_length=1)


class Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data: list[SimplificationText] = Field(min_length=1)
    leichte_sprache: bool = False
    model: str | None = Field(default=None, min_length=1)
