from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField

from research_assistant.prompt import (
    WRITER_SYSTEM_PROMPT,
    RESEARCH_REPORT_TEMPLATE,
    RESOURCE_REPORT_TEMPLATE,
    OUTLINE_REPORT_TEMPLATE,
)

model = ChatOpenAI(temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", RESEARCH_REPORT_TEMPLATE),
    ]
).configurable_alternatives(
    ConfigurableField("report_type"),
    default_key="research_report",
    resource_report=ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", RESOURCE_REPORT_TEMPLATE),
        ]
    ),
    outline_report=ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", OUTLINE_REPORT_TEMPLATE),
        ]
    ),
)
chain = prompt | model | StrOutputParser()
