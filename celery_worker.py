import sys
import celery
import importlib
from utils import get_logger

logger = get_logger(__name__)

# Add the current directory to the path
sys.path.append("./")

# Set up Celery
celery_app = celery.Celery(
    __name__,
    broker="pyamqp://guest@localhost//",
)


# Celery task to process the job
@celery_app.task(name="execute_job_task")
def execute_job_task(template_name: str, job_data: dict):
    template_path = f"templates.{template_name}"
    main_module = importlib.import_module(f"{template_path}.main")
    main_func = getattr(main_module, "main")
    logger.info(f"Main function: {main_func}")

    # Dynamically load JobRequestSchema from the corresponding template's schemas.py
    schemas_module = importlib.import_module(f"{template_path}.schema")
    JobRequestSchema = getattr(schemas_module, "JobRequestSchema")

    # Validate the job data with the loaded schema
    validated_data = JobRequestSchema(**job_data)

    # Execute the job
    results = main_func(validated_data)

    # Log the results
    logger.info(f"Job {validated_data.name} results: {results}")

    return results
