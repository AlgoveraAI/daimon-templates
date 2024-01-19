from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    prompt: str = Field(..., title="Prompt")
    system_message: str = Field(default='You are a helpful AI assistant.', title="System Message")
    model: str = Field(default='phi', title="Model")
    api_base: str = Field(default="http://localhost:11434/api/chat", title="API endpoint")
