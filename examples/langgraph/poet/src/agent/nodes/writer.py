from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State
from helpers.rymovac_tools import find_rhymes


class WriterResponse(BaseModel):
    # justification: str = Field(None, description="Summary what you wrote and why.")
    poem: str = Field(None, description="The resulting poem")

writer_structured_llm = llm.with_structured_output(WriterResponse)

tools = [find_rhymes]

writer_llm_with_tools = create_react_agent(llm, tools=tools)


async def writer(state: State):
    prompt_template = ChatPromptTemplate([
        ("system", "You are poem writing assistant that writes poems. "
                   "When you are told to write a poem or improve poem by the given feedback, "
                   "you will follow it and write short 4 line poem. "
                   "It should rhyme and be gramatically correct. "
                   "Write in user requested language."),
        # ("human", "{input}"),
        MessagesPlaceholder("messages"),
        ("human", "Now write the poem")
    ])

    iterations = state.get("iterations", 0) + 1

    chain_with_tools = prompt_template | writer_llm_with_tools
    subgraph_output = await chain_with_tools.ainvoke({"messages": state["messages"]})

    system = SystemMessage("Rewrite the message in specified response format.")
    response: WriterResponse = await writer_structured_llm.ainvoke([system, subgraph_output["messages"][-1]])

    # We add this to context so the next runs now the rhymes
    # TODO: this add also calls from previous run
    tools_messages = [message for message in subgraph_output["messages"] if message.type in ["tool", "ai"]]

    # When writing for the first time
    if not state.get("feedback"):
        message = AIMessage("I wrote the first draft: \n\n" + response.poem)
        return {"messages": tools_messages + [message], "poem": response.poem, "iterations": iterations}
    # Improving poem by feedback
    else:
        message = AIMessage("I updated the poem according the feedback: \n\n" + response.poem)
        return {"messages": tools_messages + [message], "poem": response.poem, "iterations": iterations}
