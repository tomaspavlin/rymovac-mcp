from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate

from agent.llm import llm
from agent.state import State


async def summarizer(state: State):
    prompt_template = PromptTemplate.from_template("Summarize to user what you have done and write the resulting poem.  \n\n Poem:\n {poem}")
    prompt = await prompt_template.ainvoke({"poem": state["poem"]})

    system: SystemMessage = SystemMessage(str(prompt))
    result = await llm.ainvoke([system] + state["messages"])
    return {"messages": [result]}
