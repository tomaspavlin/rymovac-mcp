from typing import Annotated, Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from helpers.rymovac_tools import check_rhyme


async def make_graph():
    llm = init_chat_model(
        "anthropic:claude-3-7-sonnet-latest",
        temperature=0
    )

    class State(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages] # add messages means that when return messages from node, they will be appended to the list
        story: str
        poem: str

        rejected: bool
        feedback: str

    graph_builder = StateGraph(State)

    class IdeatorResponse(BaseModel):
        story_name: str = Field(None, description="The name of the story/poem")
        story: str = Field(None, description="The resulting story in bulletpoints")
        justification: str = Field(
            None, description="Why this story is relevant to the user's request."
        )
        ai_message: str = Field("Summarize to user what you just did.")

    ideator_structured_llm = llm.with_structured_output(IdeatorResponse)

    class WriterResponse(BaseModel):
        justification: str = Field(None, description="Summary what you wrote and why.")
        poem: str = Field(None, description="The resulting poem")

    writer_structured_llm = llm.with_structured_output(WriterResponse)

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

    def ideator(state: State):
        system: SystemMessage = SystemMessage("You help ideate original poem. When user request poem, you do not write it but write some original story in bullet points what it will be about. Try to be funny or shocking. Write in user requested language.")
        response: IdeatorResponse = ideator_structured_llm.invoke([system] + state["messages"]) # Should I check the type if the LLM really return it?
        return {"story": response.story, "messages": [AIMessage("Ideator: " + response.ai_message)]}

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

    def evaluator1(state: State):
        response: EvaluatorResponse = evaluator_structured_llm.invoke("Evaluate if the following poem is gramatically correct, is clever and funny. And that it has 4 lines. Poem: \n" + state["poem"])
        if response.grade == "ok":
            success_message = AIMessage(f"The resulting and evaluated poem: \n\n {state["poem"]}")
            return {"rejected": False, "feedback": response.feedback, "messages": [success_message]}
        else:
            reject_message = AIMessage(f"I will apply this feedback: {response.feedback}")
            return {"rejected": True, "feedback": response.feedback, "messages": [reject_message]}

    async def rhymes_evaluator(state: State):
        prompt_template = PromptTemplate.from_template("Evaluate if the given poem rhymes. Be informative, no bullshit, no verbose. If it does not rhyme, write what does not rhyme.  \n\n Poem:\n {poem}")
        prompt = await prompt_template.ainvoke({"poem": state["poem"]})

        # Call llm with tool calling
        subgraph_output = await rhyme_checker_agent.ainvoke({"messages": [HumanMessage(str(prompt))]})
        # subgraph_output = await (await make_rhyme_checker_graph()).ainvoke({"messages": [HumanMessage(str(prompt))]})

        # Convert this tool calling messages to structured output
        # TODO: different approach is possible: https://langchain-ai.github.io/langgraph/how-tos/react-agent-structured-output/
        # TODO: try only last messgege
        response: EvaluatorResponse = await evaluator_structured_llm.ainvoke(subgraph_output["messages"])

        if response.grade == "ok":
            success_message = AIMessage(f"The poem rhymes.")
            return {"rejected": False, "feedback": response.feedback, "messages": [success_message]}
        else:
            reject_message = AIMessage(f"The poem does not rhyme. I will apply this feedback: {response.feedback}")
            return {"rejected": True, "feedback": response.feedback, "messages": [reject_message]}

    def route_evaluation(state: State):
        if state["rejected"]:
            return "rejected"
        else:
            return "accepted"

    graph_builder.add_node("ideator", ideator)
    graph_builder.add_node("writer", writer)
    graph_builder.add_node("evaluator1", evaluator1)
    graph_builder.add_node("rhymes_evaluator", rhymes_evaluator)

    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge(START, "ideator")
    graph_builder.add_edge("ideator", "writer")

    graph_builder.add_edge("writer", "evaluator1")
    graph_builder.add_conditional_edges("evaluator1", route_evaluation, {
        "rejected": "writer",
        "accepted": "rhymes_evaluator"
    })
    graph_builder.add_conditional_edges("rhymes_evaluator", route_evaluation, {
        "rejected": "writer",
        "accepted": END
    })

    #graph_builder.add_edge("writer", END)
    graph = graph_builder.compile()
    return graph
