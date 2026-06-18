from __future__ import annotations
from typing import Any, Dict
import os
import google.auth
from google.auth.credentials import AnonymousCredentials
from functools import cached_property
from google.genai import Client

# Mock google.auth.default for local/offline execution
google.auth.default = lambda *args, **kwargs: (AnonymousCredentials(), "simulated-project")
os.environ["GOOGLE_CLOUD_PROJECT"] = "simulated-project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

from google.adk.agents.context import Context
from google.adk.apps.app import App
from google.adk.events.event import Event
from google.adk.workflow import Edge, Workflow, START
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.workflow import node
from pydantic import BaseModel, Field

class CustomGemini(Gemini):
    # Declare api_key field so it's a Pydantic field
    api_key: str = "AIzaSyD-mock-key-value-12345"

    @cached_property
    def api_client(self) -> Client:
        from google.genai import Client
        return Client(api_key=self.api_key, vertexai=False)

    @cached_property
    def _live_api_client(self) -> Client:
        from google.genai import Client
        return Client(api_key=self.api_key, vertexai=False)

# Simulated vulnerability: Unsafe hardcoded API key introduced in initial draft code
model = CustomGemini(model="gemini-3.1-flash-lite", api_key="AIzaSyD-mock-key-value-12345")

# In-memory discount redemption store (simulating database state)
DISCOUNT_STORE: Dict[str, bool] = {"WELCOME50": False, "SUMMER20": False}

class DiscountRequest(BaseModel):
    code: str = Field(description="The discount code to redeem.")
    user_id: str = Field(description="The ID of the user requesting redemption.")

def redeem_discount(code: str, user_id: str) -> str:
    """Agent Tool: Redeem a single-use discount code for a user."""
    if code not in DISCOUNT_STORE:
        return "Error: Invalid discount code."
    if DISCOUNT_STORE[code]:
        return "Error: Discount code has already been redeemed."
    if not user_id or user_id.startswith("guest_"):
        return "Error: Registered user account required to redeem discounts."
        
    DISCOUNT_STORE[code] = True
    return f"Success: Discount code {code} redeemed successfully for user {user_id}."

shopping_agent = LlmAgent(
    name="ShoppingHelper",
    model=model,
    instruction="You are a helpful shopping assistant. Use your tools to redeem discount codes for users.",
    tools=[redeem_discount]
)

root_workflow = Workflow(
    name="shopping_assistant_workflow",
    edges=[Edge(from_node=START, to_node=shopping_agent)]
)

root_agent = root_workflow

app = App(
    name="shopping_assistant",
    root_agent=root_workflow
)
