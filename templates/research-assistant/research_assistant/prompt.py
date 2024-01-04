from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

####################################################################################################
####################################### SUMMARY PROMPT #############################################
####################################################################################################

SUMMARY_TEMPLATE = """{text} 

-----------

Using the above text, answer in short the following question: 

> {question}
 
-----------
if the question cannot be answered using the text, imply summarize the text. Include all factual information, numbers, stats etc if available."""  # noqa: E501
SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)


####################################################################################################
####################################### SEARCH PROMPT ##############################################
####################################################################################################

SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "{agent_prompt}"),
        (
            "user",
            "Write 3 google search queries to search online that form an "
            "objective opinion from the following: {question}\n"
            "You must respond with a list of strings in the following format: "
            '["query 1", "query 2", "query 3"].',
        ),
    ]
)

####################################################################################################
####################################### CHOOSE AGENT PROMPT ########################################
####################################################################################################

AUTO_AGENT_INSTRUCTIONS = """
This task involves researching a given topic, regardless of its complexity or the availability of a definitive answer. The research is conducted by a specific agent, defined by its type and role, with each agent requiring distinct instructions.
Agent
The agent is determined by the field of the topic and the specific name of the agent that could be utilized to research the topic provided. Agents are categorized by their area of expertise, and each agent type is associated with a corresponding emoji.

examples:
task: "should I invest in apple stocks?"
response: 
{
    "agent": "💰 Finance Agent",
    "agent_role_prompt: "You are a seasoned finance analyst AI assistant. Your primary goal is to compose comprehensive, astute, impartial, and methodically arranged financial reports based on provided data and trends."
}
task: "could reselling sneakers become profitable?"
response: 
{ 
    "agent":  "📈 Business Analyst Agent",
    "agent_role_prompt": "You are an experienced AI business analyst assistant. Your main objective is to produce comprehensive, insightful, impartial, and systematically structured business reports based on provided business data, market trends, and strategic analysis."
}
task: "what are the most interesting sites in Tel Aviv?"
response:
{
    "agent:  "🌍 Travel Agent",
    "agent_role_prompt": "You are a world-travelled AI tour guide assistant. Your main purpose is to draft engaging, insightful, unbiased, and well-structured travel reports on given locations, including history, attractions, and cultural insights."
}
"""  # noqa: E501
CHOOSE_AGENT_PROMPT = ChatPromptTemplate.from_messages(
    [SystemMessage(content=AUTO_AGENT_INSTRUCTIONS), ("user", "task: {task}")]
)

####################################################################################################
####################################### WRITER PROMPTS #############################################
####################################################################################################

WRITER_SYSTEM_PROMPT = "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."  # noqa: E501


# Report prompts from https://github.com/assafelovic/gpt-researcher/blob/master/gpt_researcher/master/prompts.py
RESEARCH_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Using the above information, answer the following question or topic: "{question}" in a detailed report -- \
The report should focus on the answer to the question, should be well structured, informative, \
in depth, with facts and numbers if available and a minimum of 1,200 words.

You should strive to write the report as long as you can using all relevant and necessary information provided.
You must write the report with markdown syntax.
You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.
Write all used source urls at the end of the report, and make sure to not add duplicated sources, but only one reference for each.
You must write the report in apa format.
Please do your best, this is very important to my career."""  # noqa: E501


RESOURCE_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Based on the above information, generate a bibliography recommendation report for the following question or topic: "{question}". \
The report should provide a detailed analysis of each recommended resource, explaining how each source can contribute to finding answers to the research question. \
Focus on the relevance, reliability, and significance of each source. \
Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax. \
Include relevant facts, figures, and numbers whenever available. \
The report should have a minimum length of 1,200 words.

Please do your best, this is very important to my career."""  # noqa: E501

OUTLINE_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Using the above information, generate an outline for a research report in Markdown syntax for the following question or topic: "{question}". \
The outline should provide a well-structured framework for the research report, including the main sections, subsections, and key points to be covered. \
The research report should be detailed, informative, in-depth, and a minimum of 1,200 words. \
Use appropriate Markdown syntax to format the outline and ensure readability.

Please do your best, this is very important to my career."""  # noqa: E501
