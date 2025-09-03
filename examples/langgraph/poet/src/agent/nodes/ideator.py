from langchain_core.messages import SystemMessage, AIMessage
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State


class IdeatorResponse(BaseModel):
    story_name: str = Field(None, description="The name of the story/poem")
    story: str = Field(None, description="The resulting story in bulletpoints")
    justification: str = Field(
        None, description="Why this story is relevant to the user's request."
    )
    ai_message: str = Field("Summarize to user what you just did.")

ideator_structured_llm = llm.with_structured_output(IdeatorResponse)


def ideator(state: State):
    system: SystemMessage = SystemMessage("You help ideate original poem. When user request poem, you do not write it but write some original story in bullet points what it will be about. Try to be funny or shocking. Write in user requested language.")
    response: IdeatorResponse = ideator_structured_llm.invoke([system] + state["messages"]) # TODO: Should I check the type if the LLM really return it?
    message = AIMessage("Ideator (TODO): " + response.ai_message)
    return {"story": response.story, "messages": [message]}
