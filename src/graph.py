
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage

from src.state import AgentState
from src.tools.calculator import calculator
from src.tools.db_lookup import db_lookup
from src.tools.web_search import web_search
from src.tools.flaky_api import flaky_api
from src.logging_utils import get_logger

logger = get_logger()

load_dotenv()

MAX_STEPS = 6

tools = [calculator, db_lookup, web_search, flaky_api]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    step = state["step_count"] + 1

    tool_calls = getattr(response, "tool_calls", None) or []
    if tool_calls:
        for call in tool_calls:
            logger.info(
                "tool_call_requested",
                extra={"data": {"step": step, "tool": call["name"], "args": call["args"]}},
            )
    else:
        logger.info(
            "final_answer",
            extra={"data": {"step": step, "content": response.content}},
        )

    return {
        "messages": [response],
        "step_count": step,
    }

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]

    if state["step_count"] >= MAX_STEPS:
        return "limit_reached"

    if getattr(last_message, "tool_calls", None):
        return "continue"

    return "stop"

def fallback_node(state: AgentState) -> dict:
    fallback_message = AIMessage(
        content=(
            "I wasn't able to fully complete this request within my step limit. "
            "Here's what I found so far, but you may want to rephrase or narrow your question."
        )
    )
    return {"messages": [fallback_message]}
    
tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_node("fallback", fallback_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "stop": END,
        "limit_reached": "fallback",
    },
)

workflow.add_edge("tools", "agent")
workflow.add_edge("fallback", END)

app = workflow.compile()
