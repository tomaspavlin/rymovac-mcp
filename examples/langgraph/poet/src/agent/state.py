from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages] # add messages means that when return messages from node, they will be appended to the list
    story: str
    poem: str

    rejected: bool
    feedback: str
