import json
import requests
from run_ollama.schema import JobRequestSchema
from run_ollama.utils import get_logger


logger = get_logger(__name__)


def main(job: JobRequestSchema):

    logger.info(f"Running job: {job}")

    messages = []
    messages.append(
        {'role': 'system', 'content': job.system_message}
    )
    messages.append(
        {'role': 'user', 'content': job.prompt}
    )


    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={
            "model": job.model, 
            "messages": messages, 
            "stream": False},
    )
    r.raise_for_status()
    
    data = json.loads(r.text)
    message = data['message']['content']

    return message


if __name__ == "__main__":
    job = JobRequestSchema(
        prompt="Tell me a joke.",
        system_message="You are a helpful AI assistant.",
        model="mistral",
    )
    print(main(job))