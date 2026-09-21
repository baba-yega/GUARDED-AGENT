
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

_search = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information on a topic.
    Use this when the user asks about recent events, facts you're unsure of,
    or anything requiring up-to-date information beyond your own knowledge.
    Example input: "current weather in Lagos"
    """
    try:
        results = _search.invoke(query)
        if not results:
            return "No search results found."
        return results
    except Exception as e:
        return f"Error: web search failed — {e}"