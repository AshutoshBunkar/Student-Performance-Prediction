from __future__ import annotations

import os
from functools import cached_property

import google.auth
from google.adk.agents import LlmAgent
from google.adk.apps.app import App
from google.adk.models.google_llm import Gemini
from google.adk.workflow import START, Edge, Workflow
from google.auth.credentials import AnonymousCredentials
from google.genai import Client
from pydantic import BaseModel, Field

# Mock google.auth.default for local/offline execution
google.auth.default = lambda *args, **kwargs: (
    AnonymousCredentials(),
    "simulated-project",
)
os.environ["GOOGLE_CLOUD_PROJECT"] = "simulated-project"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


class CustomGemini(Gemini):
    # Declare api_key field so it's a Pydantic field
    api_key: str = Field(default_factory=lambda: os.environ.get("GEMINI_API_KEY", "mock-key-value-12345"))

    @cached_property
    def api_client(self) -> Client:
        from google.genai import Client

        return Client(api_key=self.api_key, vertexai=False)

    @cached_property
    def _live_api_client(self) -> Client:
        from google.genai import Client

        return Client(api_key=self.api_key, vertexai=False)


# Remediation: Load API key from environment variable to avoid hardcoded credentials
model = CustomGemini(
    model="gemini-3.1-flash-lite",
    api_key=os.environ.get("GEMINI_API_KEY", "mock-key-value-12345")
)

# In-memory discount redemption store (simulating database state)
DISCOUNT_STORE: dict[str, bool] = {"WELCOME50": False, "SUMMER20": False}


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


class UpdateDiscountStatusRequest(BaseModel):
    code: str = Field(description="The discount code to update status for.")
    active: bool = Field(
        description="True to activate the discount code, False to deactivate it."
    )
    admin_id: str = Field(
        description="The ID of the administrator performing the action."
    )


def update_discount_status(code: str, active: bool, admin_id: str) -> str:
    """Agent Tool: Update status of a discount code. Only administrators are allowed."""
    if (
        not admin_id
        or admin_id.startswith("guest_")
        or not admin_id.startswith("admin_")
    ):
        return "Error: Administrator account required to update discount status."

    if code not in DISCOUNT_STORE:
        return "Error: Invalid discount code."

    DISCOUNT_STORE[code] = not active
    status_str = "activated" if active else "deactivated"
    return f"Success: Discount code {code} has been {status_str} by administrator {admin_id}."


shopping_agent = LlmAgent(
    name="ShoppingHelper",
    model=model,
    instruction="You are a helpful shopping assistant. Use your tools to redeem discount codes for users.",
    tools=[redeem_discount, update_discount_status],
)

root_workflow = Workflow(
    name="shopping_assistant_workflow",
    edges=[Edge(from_node=START, to_node=shopping_agent)],
)

root_agent = root_workflow

app = App(name="app", root_agent=root_workflow)
