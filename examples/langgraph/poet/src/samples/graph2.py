# More advanced test of graph

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model


model = init_chat_model(
    "anthropic:claude-3-7-sonnet-latest",
    temperature=0
)

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}


def identity_node(state: State):
    return state



# Example input state: [{"role": "user", "content": "what is the weather in sf"}]
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("identity_node", identity_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "identity_node")
graph_builder.add_edge("identity_node", END)
graph = graph_builder.compile()
