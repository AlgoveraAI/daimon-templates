import importlib
from fastapi import FastAPI, HTTPException
from schemas import JobRequest
from utils import get_logger
from celery_worker import execute_template_job  # Import the Celery task directly

logger = get_logger(__name__)
app = FastAPI()


@app.post("/execute-job")
async def execute_job(job_request: JobRequest):
    # # Dynamically load JobRequestSchema
    # try:
    #     schemas_module = importlib.import_module(f"templates.{template_name}.schema")
    #     JobRequestSchema = getattr(schemas_module, "JobRequestSchema")
    # except (ImportError, AttributeError):
    #     raise HTTPException(status_code=404, detail="Template or schema not found")

    # validated_data = JobRequestSchema(**job_data)
    # logger.info(f"Validated data: {validated_data}")

    # Send task to Celery using delay
    task = execute_template_job.delay(job_request.dict())
    return {"task_id": task.id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
