from langchain_core.runnables import RunnablePassthrough
from search import chain as search_chain
from writer import chain as writer_chain
from utils import get_logger
from schema import JobRequestSchema

logger = get_logger(__name__)


def main(job: JobRequestSchema):
    logger.info(f"Received job: {job}")

    chain_notypes = (
        RunnablePassthrough().assign(research_summary=search_chain) | writer_chain
    )

    report = chain_notypes.invoke(
        {
            "question": job.question,
        }
    )

    logger.info(f"Finished job: {job}")

    return report
