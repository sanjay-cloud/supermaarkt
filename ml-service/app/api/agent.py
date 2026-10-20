from fastapi import APIRouter
from app.agents.inventory_agent import run_agentic_loop

router = APIRouter()


@router.post("/check-inventory")
def check_inventory(query : str):
    print(f"query {query}")
    # return "For inventory ID 1 (Product: Houdbare vol melk):\n\n* **Recorded stock:** 11.0\n* **Minimum stock level:** 10\n\n**Action required:**\nAccording to the inventory policy, since the recorded stock is greater than the minimum stock level, no low-stock action is required."
    return run_agentic_loop(query)