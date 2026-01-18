from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, ModelSettings, RunContextWrapper
import rich
from datetime import datetime, time
# ----------------------------------------------------
load_dotenv()
# ----------------------------------------------------
def is_business_hours():
    now = datetime.now().time()
    business_start = time(9, 0)  # 9:00 AM
    business_end = time(21, 0)   # 9:00 PM
    return (business_start <= now) and (now <= business_end)

# ----------------------------------------------------
def closed_tool_switcher(ctx: RunContextWrapper, agent: Agent)-> bool :
    """Enable shop_closed tool only when shop is closed"""
    return not is_business_hours()

def burger_tool_switcher(ctx: RunContextWrapper, agent: Agent)-> bool :
    if ctx.context.order_type == "burger":
        return True
    return False

def pizza_tool_switcher(ctx: RunContextWrapper, agent: Agent)-> bool :
    if ctx.context.order_type == "pizza":
        return True
    return False
# ----------------------------------------------------
@function_tool(is_enabled=closed_tool_switcher)
def shop_closed()-> str:
    """return a standard shop closed notice"""

    return "shop is closed. please comeback during business hours. (9:00AM to 9:00PM)"
# ----------------------------------------------------
@function_tool(is_enabled=burger_tool_switcher)
def burger_order():
    """provide an update for the status of the user's burger order"""

    return "your Burger is cooking... please wait for just 10 minutes."
# ----------------------------------------------------
@function_tool(is_enabled=pizza_tool_switcher)
def pizza_order():
    """provide an update for the status of the user's pizza order"""

    return "your pizza is cooking... please wait for just 10 minutes."
# ----------------------------------------------------
my_order_agent = Agent(
    name="my_order_agent",
    instructions=""" always first check timing of shop by shop_closed tool if available.
    you are a order taker manager for a fast food restaurant.
    always use available tool provided to you.
    if the shop_closed tool is available use it immediately.
    Never respond with your own text - always use a tool.
    """,
    model="gpt-4.1-mini",
    tools=[burger_order, pizza_order, shop_closed],
    model_settings=ModelSettings(temperature=0.3, tool_choice="required")
)
# ----------------------------------------------------
