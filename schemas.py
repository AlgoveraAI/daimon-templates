from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class JobRequest(BaseModel):
    template_name: str
    job_request_data: Dict

