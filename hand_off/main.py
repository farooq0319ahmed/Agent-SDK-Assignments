# Handoff | OpenAI Agent-SDK
from dotenv import load_dotenv
from agents import Agent, Runner, enable_verbose_stdout_logging, Handoff, RunContextWrapper
from agents.extensions import handoff_filters
import rich
from pydantic import BaseModel
# -------------------------------------------------
load_dotenv()
enable_verbose_stdout_logging()
# -------------------------------------------------
billing_agent = Agent(
    name="billing_agent",
    instructions="You handle all billing-related inquiries. Provide clear and concise information regarding billing issues.",
    handoff_description="you support user in billing issues",
    model="deepseek/deepseek-r1-0528:free"
)
# -------------------------------------------------
refund_agent = Agent(
    name="refund_agent",
    instructions="You handle all refund-related processes. Assist users in processing refunds efficiently.",
    model="deepseek/deepseek-r1-0528:free"
)
# -------------------------------------------------
class Model_refund(BaseModel):
    input: str

my_schema = Model_refund.model_json_schema()
my_schema["additionalProperties"] = False
# -------------------------------------------------
async def my_invoke_function(ctx: RunContextWrapper, input: str):
    
    return refund_agent
# -------------------------------------------------
def my_enable_func(ctx: RunContextWrapper, agent: Agent):
    return True
# -------------------------------------------------
refund_agent_handoff = Handoff(
    agent_name="refund_agent",
    tool_name="refund_agent",
    tool_description="you provide support to user on refund process.",
    input_json_schema=my_schema,
    on_invoke_handoff=my_invoke_function,
    # input_filter=handoff_filters.remove_all_tools,
    strick_json_schema=True,
    is_enabled=my_enable_func
)
# -------------------------------------------------
main_agent = Agent(
    name="main_agent",
    instructions="you always delegate task to appropriate agent",
    model="gpt-4.1-mini",
    # handoffs=[billing_agent, refund_agent_handoff]
)
# -------------------------------------------------
result = Runner.run_sync(main_agent, input="hi, i have some refund issues, please call refund_agent", max_turns=2) # Agentic loop
# rich.print("✅",result.final_output)
# rich.print("🤖",result.last_agent.name)
