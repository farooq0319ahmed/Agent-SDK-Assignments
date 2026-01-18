# Fast-food Restaurant project | OpenAI Agent-SDK
from dotenv import load_dotenv
from agents import Agent, Runner, enable_verbose_stdout_logging
import rich
from pydantic import BaseModel, Field
from typing import Literal
from order_agent import my_order_agent
# ----------------------------------------------------
load_dotenv()
#enable_verbose_stdout_logging()
# ----------------------------------------------------
class Order_Checker(BaseModel):
    is_order: bool = Field(
        description="Set to True if and only if the user is explicitly placing an order for pizza or burger. Set to False for all other cases, including: questions about menu items, requests for recommendations, inquiries about prices, complaints, general conversation, or any non-ordering requests."
    )

    quantity: int = Field(
        default=0 ,description="The exact number of items (pizza or burger) the user is ordering. If the user does not specify a quantity, default to 1. If is_order is False, set this to 0."
    )

    order_type: Literal["pizza", "burger", "None"] = Field(
        description="Set to 'pizza' if the user is ordering pizza. Set to 'burger' if the user is ordering burger. Set to 'none' if the user is not placing an order, asking about something other than pizza or burger, or making any non-food-related request."
    )

    reason: str = Field(
        description="Provide a single-sentence explanation of the user's request. If the user is placing an order, summarize what they ordered. If the user is asking a question, briefly state the question topic. If the user's request is unrelated to food or the restaurant, clearly state that the request is outside the scope of pizza and burger ordering or inquiries."
    )

    user_question: str = Field(
        description="Copy the user's message verbatim without any modifications, additions, or interpretations. Do not paraphrase or summarize—reproduce the exact text the user provided."
    )
# ----------------------------------------------------
main_agent = Agent(
    name="main_agent",
    instructions=(
        """You are a helpful customer service assistant for a fast food restaurant that exclusively serves pizza and burger.

        Your responsibilities:
        1. Process orders: If the user explicitly states they want to order pizza or burger, extract the order details (item type and quantity).
        2. Answer questions: If the user asks questions about pizza or burger (such as ingredients, prices, sizes, availability), provide accurate and helpful responses.
        3. Handle out-of-scope requests: If the user asks about items other than pizza or burger, or makes non-food-related requests, politely inform them that you can only assist with pizza and burger orders and inquiries.

        Instructions:
        - Always classify whether the user is placing an order or asking a question.
        - Extract the exact quantity if specified; assume 1 if not mentioned.
        - Identify the order type as 'pizza', 'burger', or 'none' based on the user's message.
        - Provide a brief reason summarizing the user's intent.
        - Record the user's exact message without modification.
        - Do not make assumptions beyond what the user explicitly states.
        - Do not offer items outside of pizza and burger."""
    ),
    model="gpt-4.1-mini",
    output_type=Order_Checker,
)
# ----------------------------------------------------
user_input = input("Enter your order: ")
result = Runner.run_sync(main_agent, input=user_input)
rich.print('result: ', result.final_output)

if result.final_output.is_order == True:
    my_order_agent_result = Runner.run_sync(my_order_agent, input=result.to_input_list(), context=result.final_output)
    rich.print('my_order_agent_result: ', my_order_agent_result.final_output)