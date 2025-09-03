from langgraph.graph import StateGraph, START, END

from agent.nodes.grammar_evaluator import evaluator1
from agent.nodes.ideator import ideator
from agent.nodes.rhymes_evaluator import rhymes_evaluator
from agent.nodes.summarizer import summarizer
from agent.nodes.writer import writer
from agent.state import State


MAX_ITERATIONS = 5

async def make_graph():

    graph_builder = StateGraph(State)

    def route_evaluation(state: State):
        if state["iterations"] >= MAX_ITERATIONS:
            return "accepted" # TODO: return other states

        if state["rejected"]:
            return "rejected"
        else:
            return "accepted"


    graph_builder.add_node("ideator", ideator)
    graph_builder.add_node("writer", writer)
    graph_builder.add_node("evaluator1", evaluator1)
    graph_builder.add_node("rhymes_evaluator", rhymes_evaluator)
    graph_builder.add_node("summarizer", summarizer)

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
        "accepted": "summarizer"
    })

    graph_builder.add_edge("summarizer", END)

    #graph_builder.add_edge("writer", END)
    graph = graph_builder.compile()
    return graph
