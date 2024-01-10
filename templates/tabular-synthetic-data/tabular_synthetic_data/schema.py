from pydantic import BaseModel


class JobRequestSchema(BaseModel):
    examples: list
    data_schema: dict
    model: str = "gpt-3.5-turbo"
    subject: str = "synthetic data"
    num_samples: int = 10
