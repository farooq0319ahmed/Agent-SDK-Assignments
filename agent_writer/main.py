# AgentAI Writer
from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

# Load .env file and get API key
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Check if key exists
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY is not set. Please define it in your .env file.")

# Setup OpenRouter client (like OpenAI, but via OpenRouter)
external_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Choose any OpenRouter-supported model
model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-r1-0528:free",    # Example model, replace if needed
    openai_client=external_client
)

# Setup config
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define Agent
agent = Agent(
    name="Writer Agent",
    instructions = "You are a writer agent. Generate stories, poems, essay etc."
)

# Input and run agent
response = Runner.run_sync(
    agent,
    input = "Write a short essay on Quaid-e-Azam in simple English.",
    run_config = config
)

# Output
print(response)
