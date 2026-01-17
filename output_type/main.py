# Structured Output type with Pydantic Example AgentAI
from dotenv import load_dotenv
from agents import Agent, Runner
import rich
from pydantic import BaseModel, Field
# ----------------------------------------------------
load_dotenv()
# ----------------------------------------------------
class Name_Check(BaseModel):
    is_name: bool = Field(description="if user name is available it's value will be True otherwise it will be False")
    user_name: str = Field(default=None ,description="user name if available, otherwise value will be None")
    age: int = Field(default=1, gt=0 ,description="user age must be in this field")
# ----------------------------------------------------
agent = Agent(
    name="triage_agent",
    instructions="you are a helpful assistant",
    model="gpt-4o-mini",# model="openai/gpt-oss-20b:free",
    output_type=Name_Check
)
# ----------------------------------------------------
result = Runner.run_sync(agent, input="hi, nice to meet you, i am Farooq and me barah saal ka hun, who are you?")
# ----------------------------------------------------
if result.final_output.is_name == True:

    if result.final_output.user_name:
        print(f"hello {result.final_output.user_name}")

    if result.final_output.age > 0:
        print(f"your age is {result.final_output.age}")