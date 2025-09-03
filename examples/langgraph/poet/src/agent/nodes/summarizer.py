from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate

from agent.llm import llm
from agent.state import State


async def summarizer(state: State):
    # TODO: better use of prompt templates
    prompt_template = PromptTemplate.from_template(
        "Given the conversation, summarize to user that you wrote the poem he requested and write the resulting poem. "
        "Be friendly and write briefly about how did you come up with such poem and why. "
        "Write in user language.  \n\n Poem:\n {poem}")
    prompt = await prompt_template.ainvoke({"poem": state["poem"]})

    system: SystemMessage = SystemMessage(str(prompt))
    result = await llm.ainvoke([system] + [message for message in state["messages"] if message.type == "human"])
    return {"messages": [result]}
