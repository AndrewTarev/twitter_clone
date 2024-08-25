from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_type: str
    error_message: str
