from pydantic import BaseModel, Field


class JobRequestSchema(BaseModel):
    prompt: str = Field(..., title="Prompt")
    system_message: str = Field(default='You are a helpful AI assistant.', title="System Message")
    model: str = Field(default='mistrla', title="Model")
