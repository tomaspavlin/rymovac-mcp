from typing import Literal

from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State


class EvaluatorResponse(BaseModel):
    grade: Literal["ok", "not ok"] = Field(description="Whether the evaluation says poem is ok")
    feedback: str = Field(description="Feedback why not ok.")


evaluator_structured_llm = llm.with_structured_output(EvaluatorResponse)


def grammar_evaluator(state: State):
    response: EvaluatorResponse = evaluator_structured_llm.invoke("Evaluate if the following poem is grammatically correct. Provide constructive feedback on what to improve, focusing solely on any potential grammatical errors or issues. Do not write what is correct. Poem: \n\n" + state["poem"])
    if response.grade == "ok":
        success_message = AIMessage(f"I checked that the grammar is correct.")
        return {"rejected": False, "feedback": response.feedback, "messages": [success_message]}
    else:
        reject_message = AIMessage(f"The grammar is not correct: {response.feedback}")
        return {"rejected": True, "feedback": response.feedback, "messages": [reject_message]}
