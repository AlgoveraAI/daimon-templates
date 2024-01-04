from pydantic import BaseModel


class JobRequestSchema(BaseModel):
    question: str
