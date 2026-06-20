import pytest
import os
import google.genai
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.run_config import RunConfig, StreamingMode
import app.agent
from app.agent import DISCOUNT_STORE, root_agent

class MockAioModels:
    def __init__(self):
        self.responses = []
        self.call_count = 0
        self.captured_requests = []

    async def generate_content(self, model, contents, config):
        self.call_count += 1
        self.captured_requests.append((model, contents, config))
        if not self.responses:
            candidate = types.Candidate(
                content=types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="Default mock response")]
                )
            )
            return types.GenerateContentResponse(candidates=[candidate])

        idx = min(self.call_count - 1, len(self.responses) - 1)
        resp = self.responses[idx]
        if callable(resp):
            return resp(model, contents, config)
        return resp

    async def generate_content_stream(self, model, contents, config):
        res = await self.generate_content(model, contents, config)
        async def _stream():
            yield res
        return _stream()

class MockAio:
    def __init__(self, models):
        self.models = models

class MockClient:
    _models_instance = None

    def __init__(self, *args, **kwargs):
        self.aio = MockAio(MockClient._models_instance)
        self.vertexai = False

@pytest.fixture(autouse=True)
def mock_genai_client(monkeypatch):
    models = MockAioModels()
    MockClient._models_instance = models
    monkeypatch.setattr(google.genai, "Client", MockClient)
    for attr in ["api_client", "_live_api_client"]:
        if attr in app.agent.model.__dict__:
            del app.agent.model.__dict__[attr]
    yield models

def run_agent_workflow(prompt_text: str, user_id: str = "test_user") -> list[str]:
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id=user_id, app_name="test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="test")

    message = types.Content(
        role="user", parts=[types.Part.from_text(text=prompt_text)]
    )

    events = list(
        runner.run(
            new_message=message,
            user_id=user_id,
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        )
    )

    responses = []
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    responses.append(part.text)
    return responses

def test_agent_redeem_discount_success(mock_genai_client):
    # Reset store
    DISCOUNT_STORE["WELCOME50"] = False

    # 1. First response: call redeem_discount tool
    func_call = types.FunctionCall(
        name="redeem_discount",
        args={"code": "WELCOME50", "user_id": "user_123"}
    )
    candidate1 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=func_call)]
        )
    )
    resp1 = types.GenerateContentResponse(candidates=[candidate1])

    # 2. Second response: final confirmation
    candidate2 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text="I've successfully redeemed the discount WELCOME50 for you!")]
        )
    )
    resp2 = types.GenerateContentResponse(candidates=[candidate2])

    mock_genai_client.responses = [resp1, resp2]

    results = run_agent_workflow("Redeem WELCOME50 for user_123", user_id="user_123")

    # Verify tool execution & state change
    assert DISCOUNT_STORE["WELCOME50"] is True
    assert any("successfully redeemed" in r.lower() for r in results)

def test_agent_redeem_discount_invalid_code(mock_genai_client):
    func_call = types.FunctionCall(
        name="redeem_discount",
        args={"code": "INVALID99", "user_id": "user_123"}
    )
    candidate1 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=func_call)]
        )
    )
    resp1 = types.GenerateContentResponse(candidates=[candidate1])

    candidate2 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text="Sorry, that is an invalid discount code.")]
        )
    )
    resp2 = types.GenerateContentResponse(candidates=[candidate2])

    mock_genai_client.responses = [resp1, resp2]

    results = run_agent_workflow("Redeem INVALID99 for user_123", user_id="user_123")

    # Verify final response reports the failure
    assert any("invalid discount code" in r.lower() for r in results)

def test_agent_redeem_discount_already_redeemed(mock_genai_client):
    # Set to already redeemed
    DISCOUNT_STORE["WELCOME50"] = True

    func_call = types.FunctionCall(
        name="redeem_discount",
        args={"code": "WELCOME50", "user_id": "user_123"}
    )
    candidate1 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=func_call)]
        )
    )
    resp1 = types.GenerateContentResponse(candidates=[candidate1])

    candidate2 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text="Sorry, that code has already been redeemed.")]
        )
    )
    resp2 = types.GenerateContentResponse(candidates=[candidate2])

    mock_genai_client.responses = [resp1, resp2]

    results = run_agent_workflow("Redeem WELCOME50 for user_123", user_id="user_123")

    # Verify final response reports already redeemed (represented by the second function call response)
    # The runner executes the tool, gets "Error: Discount code has already been redeemed.", and submits it back.
    # We verify the mock client was called twice
    assert mock_genai_client.call_count == 2
    # Verify that the tool response in contents (submitted to second call) contains the error
    _, contents, _ = mock_genai_client.captured_requests[1]
    tool_resp_found = False
    for content in contents:
        for part in content.parts:
            if part.function_response and part.function_response.response:
                val = part.function_response.response.get("result", "")
                if "already been redeemed" in val:
                    tool_resp_found = True
    assert tool_resp_found

def test_agent_redeem_discount_guest_user(mock_genai_client):
    # Reset store
    DISCOUNT_STORE["WELCOME50"] = False

    func_call = types.FunctionCall(
        name="redeem_discount",
        args={"code": "WELCOME50", "user_id": "guest_123"}
    )
    candidate1 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=func_call)]
        )
    )
    resp1 = types.GenerateContentResponse(candidates=[candidate1])

    candidate2 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text="Guest users cannot redeem discounts.")]
        )
    )
    resp2 = types.GenerateContentResponse(candidates=[candidate2])

    mock_genai_client.responses = [resp1, resp2]

    results = run_agent_workflow("Redeem WELCOME50 for guest_123", user_id="guest_123")

    # Verify store remains False
    assert DISCOUNT_STORE["WELCOME50"] is False
    assert mock_genai_client.call_count == 2
    _, contents, _ = mock_genai_client.captured_requests[1]
    tool_resp_found = False
    for content in contents:
        for part in content.parts:
            if part.function_response and part.function_response.response:
                val = part.function_response.response.get("result", "")
                if "Registered user account required" in val:
                    tool_resp_found = True
    assert tool_resp_found

def test_agent_redeem_discount_empty_user(mock_genai_client):
    # Reset store
    DISCOUNT_STORE["WELCOME50"] = False

    func_call = types.FunctionCall(
        name="redeem_discount",
        args={"code": "WELCOME50", "user_id": ""}
    )
    candidate1 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=func_call)]
        )
    )
    resp1 = types.GenerateContentResponse(candidates=[candidate1])

    candidate2 = types.Candidate(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text="A registered user account is required.")]
        )
    )
    resp2 = types.GenerateContentResponse(candidates=[candidate2])

    mock_genai_client.responses = [resp1, resp2]

    results = run_agent_workflow("Redeem WELCOME50 without user ID", user_id="")

    # Verify store remains False
    assert DISCOUNT_STORE["WELCOME50"] is False
    assert mock_genai_client.call_count == 2
    _, contents, _ = mock_genai_client.captured_requests[1]
    tool_resp_found = False
    for content in contents:
        for part in content.parts:
            if part.function_response and part.function_response.response:
                val = part.function_response.response.get("result", "")
                if "Registered user account required" in val:
                    tool_resp_found = True
    assert tool_resp_found
