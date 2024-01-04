from langchain_core.runnables import RunnablePassthrough
from research_assistant.search import chain as search_chain
from research_assistant.writer import chain as writer_chain
from research_assistant.utils import get_logger
from research_assistant.schema import JobRequestSchema

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


if __name__ == "__main__":
    import sys
    sys.path.append("../")
    job = JobRequestSchema(
        question="What is the best way to learn a new language?",
    )

    print(main(job))
