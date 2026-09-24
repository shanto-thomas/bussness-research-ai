import json

import httpx

from business_research_ai.clients.research_api import (
    ResearchApiClient,
    ResearchApiError,
)


def test_session_flow_calls_existing_routes():
    seen: list[tuple[str, str, dict | None]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else None
        seen.append((request.method, request.url.path, body))

        if request.url.path == "/health":
            return httpx.Response(200, json={"status": "healthy"})
        if request.url.path == "/api/v1/research/session":
            return httpx.Response(
                200,
                json={"session_id": "abc", "status": "active"},
            )
        if request.url.path == "/api/v1/research/session/abc/message":
            return httpx.Response(
                200,
                json={
                    "session_id": "abc",
                    "message": "What would you like to research?",
                    "options": ["market"],
                },
            )
        if request.url.path == "/api/v1/research/session/abc":
            return httpx.Response(
                200,
                json={"session_id": "abc", "status": "active"},
            )
        if request.url.path == "/api/v1/research":
            return httpx.Response(
                200,
                json={"business_idea": "A shop", "response": "{}"},
            )
        return httpx.Response(404, json={"detail": "missing"})

    client = ResearchApiClient(
        "http://api.test",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert client.health()["status"] == "healthy"
    created = client.create_session()
    message = client.send_message(created["session_id"], "A local shop")
    session = client.get_session("abc")
    research = client.create_research("A local marketplace")

    assert message["options"] == ["market"]
    assert session["session_id"] == "abc"
    assert research["business_idea"] == "A shop"
    assert seen == [
        ("GET", "/health", None),
        ("POST", "/api/v1/research/session", None),
        (
            "POST",
            "/api/v1/research/session/abc/message",
            {"message": "A local shop"},
        ),
        ("GET", "/api/v1/research/session/abc", None),
        (
            "POST",
            "/api/v1/research",
            {"business_idea": "A local marketplace"},
        ),
    ]


def test_api_error_uses_fastapi_detail():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "Research session not found"})

    client = ResearchApiClient(
        "http://api.test",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    try:
        client.get_session("missing")
    except ResearchApiError as exc:
        assert exc.status_code == 404
        assert str(exc) == "Research session not found"
    else:
        raise AssertionError("expected ResearchApiError")
