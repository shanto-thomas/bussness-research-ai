from langchain.agents.middleware import (
    AgentMiddleware,
    ModelCallLimitMiddleware,
    SummarizationMiddleware,
    ToolCallLimitMiddleware,
    ToolRetryMiddleware,
)

from business_research_ai.llm.openai import get_openai_model

SEARCH_TOOLS = (
    "web_search",
    "news_search",
    "website_reader",
    "business_search",
)

RUN_MODEL_CALL_LIMIT = 8
RUN_TOOL_CALL_LIMIT = 5
TOOL_MAX_RETRIES = 2
SUMMARY_TOKEN_TRIGGER = 6000
SUMMARY_MESSAGES_TO_KEEP = 6


def build_specialist_middleware() -> list[AgentMiddleware]:
    """
    Middleware for research specialists that call search and page tools.

    Limits apply to a single agent run. Failed search tools are retried, then
    the error is returned to the model so the run can continue. Long histories
    are summarized before the next model call.
    """

    tool_limits = [
        ToolCallLimitMiddleware(
            tool_name=tool_name,
            run_limit=RUN_TOOL_CALL_LIMIT,
            exit_behavior="continue",
        )
        for tool_name in SEARCH_TOOLS
    ]

    return [
        ModelCallLimitMiddleware(
            run_limit=RUN_MODEL_CALL_LIMIT,
            exit_behavior="end",
        ),
        *tool_limits,
        ToolRetryMiddleware(
            max_retries=TOOL_MAX_RETRIES,
            tools=list(SEARCH_TOOLS),
            on_failure="continue",
        ),
        SummarizationMiddleware(
            get_openai_model(),
            trigger=("tokens", SUMMARY_TOKEN_TRIGGER),
            keep=("messages", SUMMARY_MESSAGES_TO_KEEP),
        ),
    ]
