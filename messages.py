from pydantic import BaseModel

class SuccessfulMessage(BaseModel):
    message: str


class ErrorMessage(BaseModel):
    error: str

class SuccessfulMessageWithData(BaseModel):
    message: str
    balance : float