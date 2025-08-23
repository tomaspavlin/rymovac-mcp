from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

llm = init_chat_model(
    "anthropic:claude-3-7-sonnet-latest",
    temperature=0
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages] # add messages means that when return messages from node, they will be appended to the list
    story: str
    poem: str

graph_builder = StateGraph(State)

class IdeatorResponse(BaseModel):
    story_name: str = Field(None, description="The name of the story/poem")
    story: str = Field(None, description="The resulting story in bulletpoints")
    justification: str = Field(
        None, description="Why this story is relevant to the user's request."
    )

ideator_structured_llm = llm.with_structured_output(IdeatorResponse)

def ideator(state: State):
    system: SystemMessage = SystemMessage("You help ideate original poem. When user request poem, you do not write it but write some original story in bullet points what it will be about. Try to be funny or shocking. Write only the bullet points, nothing more.")
    response: IdeatorResponse = ideator_structured_llm.invoke([system] + state["messages"]) # Should I check the type if the LLM really return it?
    return {"story": response.story}

def writer(state: State):
    system: SystemMessage = SystemMessage("When you are given idea for a poem story, you will follow it and write 4-8 line poem.")
    human: HumanMessage = HumanMessage("Write poem about the following:\n " + state["story"])
    # poem = llm.invoke("Write poem about the following:\n " + state["story"])
    poem = llm.invoke([system, human])
    return {"messages": [poem], "poem": poem.content}

graph_builder.add_node("ideator", ideator)
graph_builder.add_node("writer", writer)

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge(START, "ideator")
graph_builder.add_edge("ideator", "writer")
graph_builder.add_edge("writer", END)
graph = graph_builder.compile()
