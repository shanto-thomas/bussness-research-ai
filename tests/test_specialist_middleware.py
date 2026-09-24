from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    SummarizationMiddleware,
    ToolCallLimitMiddleware,
    ToolRetryMiddleware,
)

from business_research_ai.agents.specialist_middleware import (
    RUN_MODEL_CALL_LIMIT,
    RUN_TOOL_CALL_LIMIT,
    SEARCH_TOOLS,
    SUMMARY_MESSAGES_TO_KEEP,
    SUMMARY_TOKEN_TRIGGER,
    TOOL_MAX_RETRIES,
    build_specialist_middleware,
)


def test_specialist_middleware_limits_search_tools():
    middleware = build_specialist_middleware()

    model_limit = middleware[0]
    tool_limits = middleware[1 : 1 + len(SEARCH_TOOLS)]
    retry = middleware[-2]
    summarizer = middleware[-1]

    assert isinstance(model_limit, ModelCallLimitMiddleware)
    assert model_limit.run_limit == RUN_MODEL_CALL_LIMIT
    assert model_limit.exit_behavior == "end"

    limited_tools = []
    for item in tool_limits:
        assert isinstance(item, ToolCallLimitMiddleware)
        assert item.run_limit == RUN_TOOL_CALL_LIMIT
        assert item.exit_behavior == "continue"
        limited_tools.append(item.tool_name)

    assert tuple(limited_tools) == SEARCH_TOOLS

    assert isinstance(retry, ToolRetryMiddleware)
    assert retry.max_retries == TOOL_MAX_RETRIES
    assert retry._tool_filter == list(SEARCH_TOOLS)
    assert retry.on_failure == "continue"

    assert isinstance(summarizer, SummarizationMiddleware)
    assert summarizer.trigger == ("tokens", SUMMARY_TOKEN_TRIGGER)
    assert summarizer.keep == ("messages", SUMMARY_MESSAGES_TO_KEEP)
