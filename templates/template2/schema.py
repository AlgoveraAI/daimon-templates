from pydantic import BaseModel


class JobRequestSchema(BaseModel):
    name: str
    description: str
    param1: int
    param2: int
