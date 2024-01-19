# Chat Llego

This is a llego block that implements a simple chat assistant. It uses an LLM via an API to generate responses to messages. It uses litellm as a backend to query the LLM via an API. See litellm's supported models and APIs here: https://docs.litellm.ai/docs/providers

Inputs:

- `system_message` (str): The system message to use. Default: "You are a helpful assistant."
- `prompt` (str): The user message used to initialize the conversation. Default: "Tell me a joke"
- `model` (str): The name of the model to use. The name needs to follow the name of the model in litellm https://docs.litellm.ai/docs/providers. Default: "ollama/phi"
- `api_base` (str): The API endpoint to use. Default: "http://localhost:11434"
