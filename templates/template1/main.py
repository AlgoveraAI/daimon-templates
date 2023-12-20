from .schema import JobRequestSchema
from .utils import get_logger

logger = get_logger(__name__)

def main(job: JobRequestSchema):
    logger.info(f"Running job {job.name}")
    return job.param1 + job.param2