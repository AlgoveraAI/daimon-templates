from typing import Dict
from pydantic import BaseModel


class JobRequest(BaseModel):
    template_name: str
    job_request_data: Dict
