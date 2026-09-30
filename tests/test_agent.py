# tests/test_agent.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.graph import should_continue, MAX_STEPS
from langchain_core.messages import AIMessage


def make_state(tool_calls, step_count):
    message = AIMessage(content="", tool_calls=tool_calls)
    return {"messages": [message], "step_count": step_count}


def test_stops_when_no_tool_calls():
    state = make_state(tool_calls=[], step_count=1)
    assert should_continue(state) == "stop"


def test_continues_when_tool_called_and_under_limit():
    state = make_state(
        tool_calls=[{"name": "calculator", "args": {"expression": "1+1"}, "id": "1"}],
        step_count=1,
    )
    assert should_continue(state) == "continue"


def test_limit_reached_when_step_count_at_max():
    state = make_state(
        tool_calls=[{"name": "calculator", "args": {"expression": "1+1"}, "id": "1"}],
        step_count=MAX_STEPS,
    )
    assert should_continue(state) == "limit_reached"


def test_stops_even_at_limit_if_no_tool_calls():
    state = make_state(tool_calls=[], step_count=MAX_STEPS)
    assert should_continue(state) == "stop"