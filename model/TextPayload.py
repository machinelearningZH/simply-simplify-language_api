from typing import Union, Optional, Dict
from pydantic import BaseModel, Json


class TextPayload(BaseModel):
    data: Union[str, dict] = None
    leichte_sprache: bool
    format: str
    path: Optional[str] = None
    root: Optional[str] = None
    model: Optional[str] = None
