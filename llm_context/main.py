# Local Context & LLM Context | OpenAI Agent-SDK
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunContextWrapper, function_tool
import rich
from pydantic import BaseModel
# ----------------------------------------------------
load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ----------------------------------------------------
class User_Info(BaseModel):
    name: str
    age: int
    alive: bool
    roll_num: str
# ----------------------------------------------------
my_info = User_Info(name="Farooq", age=22, alive=True, roll_num="abc12345000")
# ----------------------------------------------------
def dynamic_ins(wrapper: RunContextWrapper[User_Info], agent: Agent):
    wrapper.context.name = "Ahmed"

    return f"whenever user ask for a roll_number or name you use given tool user_information to get roll_number of the user, user age is {wrapper.context.age}."
# ----------------------------------------------------
@function_tool
def user_information(wrapper: RunContextWrapper[User_Info]):
    return f"user roll number is {wrapper.context.roll_num} and user name is {wrapper.context.name}"
# ----------------------------------------------------
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

agent = Agent[User_Info](
    name="triage_agent",
    instructions=dynamic_ins,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    tools=[user_information]
    )
# ----------------------------------------------------
result = Runner.run_sync(agent, input="what is the name of user? and what is his roll_number?", context=my_info)
rich.print(result.final_output)