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
    system: SystemMessage = SystemMessage(
        """You help ideate original poem ideas that other AI assistants will write after your turn. When the user requests a poem, you do not write it but instead provide some original story concepts in bullet points that could be included in the poem. Focus on making the ideas funny, vulgar, harsh, smart, and include unexpected twists. Write in the user-requested language.

- First thing about associations and ideas that relate to the topic
- Generate 5-10 unique story concepts.
- Ensure ideas include humor, vulgarity, or harshness where appropriate.
- Incorporate smart elements or clever wordplay.
- Aim for unexpected twists that surprise the reader.
- Maintain a balance between creativity and coherence in the ideas.
""")
    #response: IdeatorResponse = ideator_structured_llm.invoke([system] + state["messages"])
    response = llm.invoke([system] + state["messages"])
    message = AIMessage(response.content)
    return {"story": response.content, "messages": [message]}
