from typing import Literal

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from agent.llm import llm
from agent.state import State
from helpers.rymovac_tools import check_rhyme


class EvaluatorResponse(BaseModel):
    grade: Literal["ok", "not ok"] = Field(description="Whether the evaluation says poem is ok")
    feedback: str = Field(description="Feedback why not ok.")


evaluator_structured_llm = llm.with_structured_output(EvaluatorResponse)


# # todo: this throws error
# mcp_client = MultiServerMCPClient(
#     {
#         "rymovac": {
#             "command": "npx",
#             "args": ["-y", "@rymovac/mcp"],
#             "transport": "stdio",
#         },
#     }
# )
# rymovac_tools = await mcp_client.get_tools() # awaits can be inside async functions only, that is why we have the async funcction

rymovac_tools = [check_rhyme]

rhyme_checker_agent = create_react_agent(llm, tools=rymovac_tools)


async def rhymes_evaluator(state: State):
    prompt_template = PromptTemplate.from_template("Evaluate if the given poem rhymes. First, understand, what rhyming scheme is used. Be informative, no bullshit, no verbose. If it does not rhyme, write what does not rhyme. Do not explicitly write if something rhymes. \n\n Poem:\n {poem}")
    prompt = await prompt_template.ainvoke({"poem": state["poem"]})

    # Call llm with tool calling
    subgraph_output = await rhyme_checker_agent.ainvoke({"messages": [HumanMessage(str(prompt))]})
    # subgraph_output = await (await make_rhyme_checker_graph()).ainvoke({"messages": [HumanMessage(str(prompt))]})

    # Convert this tool calling messages to structured output
    # TODO: different approach is possible: https://langchain-ai.github.io/langgraph/how-tos/react-agent-structured-output/
    # TODO: try only last messgege

    system = SystemMessage("Rewrite the message in specified response format.")
    response: EvaluatorResponse = await evaluator_structured_llm.ainvoke([system, subgraph_output["messages"][-1]])

    if response.grade == "ok":
        success_message = AIMessage(f"I checked that the poem rhymes.")
        return {"rejected": False, "feedback": response.feedback, "messages": [success_message]}
    else:
        reject_message = AIMessage(f"{response.feedback}")
        return {"rejected": True, "feedback": response.feedback, "messages": [reject_message]}
