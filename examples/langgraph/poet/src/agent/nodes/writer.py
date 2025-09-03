from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State


class WriterResponse(BaseModel):
    justification: str = Field(None, description="Summary what you wrote and why.")
    poem: str = Field(None, description="The resulting poem")

writer_structured_llm = llm.with_structured_output(WriterResponse)


def writer(state: State):
    if not state.get("feedback"):
        system: SystemMessage = SystemMessage("When you are given idea for a poem story, you will follow it and write short 4 line poem. It should rhyme. Write in user requested language.")
        human: HumanMessage = HumanMessage("Write poem about the following:\n " + state["story"])
        # poem = llm.invoke("Write poem about the following:\n " + state["story"])
        response: WriterResponse = writer_structured_llm.invoke([system, human])
        return {"messages": [AIMessage("Wrote poem draft: " + response.justification)], "poem": response.poem}
    else:
        # system: SystemMessage = SystemMessage("When you are given idea for a poem story, you will follow it and write 4-8 line poem. Output only poem, nothing more.")
        # human: HumanMessage = HumanMessage("Write poem about the following:\n " + state["story"])
        # poem = llm.invoke("Write poem about the following:\n " + state["story"])
        prompt_template = PromptTemplate.from_template("Apply the feedback to the given poem. \n\n Feedback: {feedback}\n\n Poem:\n {poem}")
        prompt = prompt_template.invoke({"feedback": state["feedback"], "poem": state["poem"]})
        response: WriterResponse = writer_structured_llm.invoke(prompt)
        return {"messages": [AIMessage("Applied feedback: " + response.justification)], "poem": response.poem}
