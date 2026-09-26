
from langchain_core.messages import HumanMessage
from src.graph import app

def run_agent(user_input: str):
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "step_count": 0,
    }
    result = app.invoke(initial_state)
    return result

if __name__ == "__main__":
    user_question = input("Ask the agent something: ")
    final_state = run_agent(user_question)

    print("\n--- Final Answer ---")
    print(final_state["messages"][-1].content)

    print(f"\n(Completed in {final_state['step_count']} agent step(s))")





