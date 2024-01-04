from pydantic import BaseModel, Field


class JobRequestSchema(BaseModel):
    question: str = Field(..., title="Question", description="Question to be answered")
