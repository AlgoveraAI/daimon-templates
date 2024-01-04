import requests
from bs4 import BeautifulSoup
from typing import Any
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda,
    Runnable,
)
from langchain_core.output_parsers import StrOutputParser

from research_assistant.prompt import SEARCH_PROMPT, CHOOSE_AGENT_PROMPT, SUMMARY_PROMPT
from research_assistant.utils import load_json

# Constants
RESULTS_PER_QUESTION = 3
ddg_search = DuckDuckGoSearchAPIWrapper()


# Functions
def scrape_text(url: str):
    # Send a GET request to the webpage
    try:
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the request with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract all text from the webpage
            page_text = soup.get_text(separator=" ", strip=True)

            # Print the extracted text
            return page_text
        else:
            return f"Failed to retrieve the webpage: Status code {response.status_code}"
    except Exception as e:
        print(e)
        return f"Failed to retrieve the webpage: {e}"


def web_search(query: str, num_results: int):
    results = ddg_search.results(query, num_results)
    return [r["link"] for r in results]


get_links: Runnable[Any, Any] = RunnablePassthrough() | RunnableLambda(
    lambda x: [
        {"url": url, "question": x["question"]}
        for url in web_search(query=x["question"], num_results=RESULTS_PER_QUESTION)
    ]
)

scrape_and_summarize: Runnable[Any, Any] = (
    RunnableParallel(
        {
            "question": lambda x: x["question"],
            "text": lambda x: scrape_text(x["url"])[:10000],
            "url": lambda x: x["url"],
        }
    )
    | RunnableParallel(
        {
            "summary": SUMMARY_PROMPT | ChatOpenAI(temperature=0) | StrOutputParser(),
            "url": lambda x: x["url"],
        }
    )
    | RunnableLambda(lambda x: f"Source Url: {x['url']}\nSummary: {x['summary']}")
)

choose_agent = (
    CHOOSE_AGENT_PROMPT | ChatOpenAI(temperature=0) | StrOutputParser() | load_json
)
search_query = SEARCH_PROMPT | ChatOpenAI(temperature=0) | StrOutputParser() | load_json
multi_search = get_links | scrape_and_summarize.map() | (lambda x: "\n".join(x))


get_search_queries = (
    RunnablePassthrough().assign(
        agent_prompt=RunnableParallel({"task": lambda x: x})
        | choose_agent
        | (lambda x: x.get("agent_role_prompt"))
    )
    | search_query
)

chain = (
    get_search_queries
    | (lambda x: [{"question": q} for q in x])
    | multi_search.map()
    | (lambda x: "\n\n".join(x))
)
