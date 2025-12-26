from fastapi import HTTPException


class BadFormattingError(HTTPException):
    code = 500
    description = "Bad JSON formatting"
