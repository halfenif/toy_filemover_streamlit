from pydantic import BaseModel, Field

class RequestResult(BaseModel):
    result: str = Field("", alias='Result')
    msg: str = Field("", alias='Message')
    method: str = Field("", alias='Method')
