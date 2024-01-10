import json
from typing import Any
from pydantic import create_model
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from tabular_synthetic_data.prompt import SYN_DATA_PROMPT
from tabular_synthetic_data.schema import JobRequestSchema
from tabular_synthetic_data.utils import get_logger


logger = get_logger(__name__)


def generate_examples(examples):
    return "\n\n".join([list(example.values())[0] for example in examples])


def create_pydantic_model(schema: dict) -> Any:
    fields = {
        field_name: (field_type, ...) for field_name, field_type in schema.items()
    }
    return create_model("DynamicModel", **fields)


def main(job: JobRequestSchema):
    # Prepare llm
    llm = ChatOpenAI(model=job.model, temperature=1)

    # Prepare prompt
    prompt_template = PromptTemplate(
        input_variables=["subject", "schema", "examples"],
        template=SYN_DATA_PROMPT,
    )

    # Prepare llm chain
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    # Prepare parser
    parser = PydanticOutputParser(
        pydantic_object=create_pydantic_model(job.data_schema)
    )

    data = []
    for i in range(job.num_samples):
        try:
            res = llm_chain.predict(
                subject=job.subject,
                schema=job.data_schema,
                examples=generate_examples(job.examples),
            )
            logger.info(f"Response {i}: {res}")

            data.append(parser.parse(res))

        except Exception as e:
            logger.error(e)
            continue

    data = [d.dict() for d in data]

    return json.dumps(data)


if __name__ == "__main__":
    schema = {
        "patient_id": "int",
        "patient_name": "str",
        "diagnosis_code": "str",
        "procedure_code": "str",
        "total_charge": "float",
        "insurance_claim_amount": "float",
    }

    examples = [
        {
            "example_1": """patient_id: 123456, patient_name: John Doe, diagnosis_code: J20.9, procedure_code: 99203, total_charge: $500, insurance_claim_amount: $350"""
        },
        {
            "example_2": """patient_id: 789012, patient_name: Johnson Smith, diagnosis_code: M54.5, procedure_code: 99213, total_charge: $150, insurance_claim_amount: $120"""
        },
        {
            "example_3": """patient_id: 345678, patient_name: Emily Stone, diagnosis_code:E11.9, procedure_code: 99214, total_charge: $300, insurance_claim_amount: $250"""
        },
    ]

    subject = "medical_billing"

    job = JobRequestSchema(
        examples=examples,
        data_schema=schema,
        subject=subject,
        num_samples=10,
    )

    print(main(job))
