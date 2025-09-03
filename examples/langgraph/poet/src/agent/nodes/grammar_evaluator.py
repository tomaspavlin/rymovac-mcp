from typing import Literal

from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State


class EvaluatorResponse(BaseModel):
    grade: Literal["ok", "not ok"] = Field(description="Whether the evaluation says poem is ok")
    feedback: str = Field(description="Feedback why not ok.")


evaluator_structured_llm = llm.with_structured_output(EvaluatorResponse)


def evaluator1(state: State):
    response: EvaluatorResponse = evaluator_structured_llm.invoke("Evaluate if the following poem is gramatically correct, is clever and funny. And that it has 4 lines. Poem: \n" + state["poem"])
    if response.grade == "ok":
        success_message = AIMessage(f"The resulting and evaluated poem: \n\n {state["poem"]}")
        return {"rejected": False, "feedback": response.feedback, "messages": [success_message]}
    else:
        reject_message = AIMessage(f"I will apply this feedback: {response.feedback}")
        return {"rejected": True, "feedback": response.feedback, "messages": [reject_message]}
