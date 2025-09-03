from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State


class WriterResponse(BaseModel):
    # justification: str = Field(None, description="Summary what you wrote and why.")
    poem: str = Field(None, description="The resulting poem")

writer_structured_llm = llm.with_structured_output(WriterResponse)


def writer(state: State):
    system: SystemMessage = SystemMessage(
        "You are poem writing assistant that writes poems. "
        "When you are told to write a poem or improve poem by the given feedback, "
        "you will follow it and write short 4 line poem. "
        "It should rhyme and be gramatically correct. "
        "Write in user requested language.")

    iterations = state.get("iterations", 0) + 1

    # When writing for the first time
    if not state.get("feedback"):
        human: HumanMessage = HumanMessage("Write poem about the following:\n " + state["story"])
        # poem = llm.invoke("Write poem about the following:\n " + state["story"])
        # response: WriterResponse = writer_structured_llm.invoke([system, human])
        response: WriterResponse = writer_structured_llm.invoke([system] + state["messages"])
        # message = AIMessage("Wrote poem draft: " + response.justification)
        message = AIMessage("I wrote the first draft: \n\n" + response.poem)
        return {"messages": [message], "poem": response.poem, "iterations": iterations}
    # Improving poem by feedback
    else:
        # todoo poem story (or some history)
        prompt_template = PromptTemplate.from_template("Apply the feedback to the given poem. \n\n Feedback: {feedback}\n\n Poem:\n {poem}")
        prompt = prompt_template.invoke({"feedback": state["feedback"], "poem": state["poem"]})
        human: HumanMessage = HumanMessage(str(prompt))
        #response: WriterResponse = writer_structured_llm.invoke([system, human])
        response: WriterResponse = writer_structured_llm.invoke([system] + state["messages"])
        message = AIMessage("I updated the poem according the feedback: \n\n" + response.poem)
        return {"messages": [message], "poem": response.poem, "iterations": iterations}
