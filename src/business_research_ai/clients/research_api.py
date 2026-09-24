import httpx


class ResearchApiError(Exception):
    """The research API returned an error or could not be reached."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class ResearchApiClient:
    """HTTP client for the existing Business Research API."""

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 900.0,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._timeout = httpx.Timeout(timeout, connect=10.0)
        self._client = client or httpx.Client(timeout=self._timeout)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "ResearchApiClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def health(self) -> dict:
        return self._request(
            "GET",
            "/health",
            timeout=httpx.Timeout(3.0, connect=3.0),
        )

    def create_session(self) -> dict:
        return self._request("POST", "/api/v1/research/session")

    def send_message(self, session_id: str, message: str) -> dict:
        return self._request(
            "POST",
            f"/api/v1/research/session/{session_id}/message",
            json={"message": message},
        )

    def get_session(self, session_id: str) -> dict:
        return self._request(
            "GET",
            f"/api/v1/research/session/{session_id}",
        )

    def create_research(self, business_idea: str) -> dict:
        return self._request(
            "POST",
            "/api/v1/research",
            json={"business_idea": business_idea},
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | None = None,
        timeout: httpx.Timeout | None = None,
    ) -> dict:
        try:
            response = self._client.request(
                method,
                f"{self.base_url}{path}",
                json=json,
                timeout=timeout or self._timeout,
            )
        except httpx.RequestError as exc:
            raise ResearchApiError(
                f"Could not reach the API at {self.base_url}."
            ) from exc

        if response.status_code >= 400:
            raise ResearchApiError(
                _error_detail(response),
                status_code=response.status_code,
            )

        return response.json()


def _error_detail(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        text = response.text.strip()
        return text or f"Request failed with status {response.status_code}."

    detail = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(detail, str) and detail:
        return detail
    if isinstance(detail, list):
        messages = [
            item.get("msg", str(item))
            for item in detail
            if isinstance(item, dict)
        ]
        if messages:
            return " ".join(messages)
    return f"Request failed with status {response.status_code}."
