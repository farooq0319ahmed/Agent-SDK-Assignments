# AgentAI Writer
from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

# Load .env file and get API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Check if key exists
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please define it in your .env file.")

# Setup OpenRouter client (like OpenAI, but via OpenRouter)
external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# Choose any OpenRouter-supported model
model = OpenAIChatCompletionsModel(
    model="google/gemma-3-27b-it:free",    # Example model, replace if needed
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
