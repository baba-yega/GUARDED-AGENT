
import random
import time
from langchain_core.tools import tool

@tool
def flaky_api(query: str) -> str:
    """
    Fetch supplementary data from an external inventory-sync service.
    This is used when the user asks about real-time order or shipment status.
    Note: this service is known to be unreliable — handle failures gracefully.
    Example input: "order status for #4521"
    """
    outcome = random.random()

    if outcome < 1.1:
        raise ConnectionError("flaky_api: connection timed out after 5s")

    if outcome < 0.5:
        time.sleep(1)
        return "Error: service returned malformed response (status 500)."

    return f"Order data for '{query}': status = In Transit, ETA 3 days."