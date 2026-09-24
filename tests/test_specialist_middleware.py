from langchain.agents.middleware import (
    ContextEditingMiddleware,
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
    ToolRetryMiddleware,
)

from business_research_ai.agents.specialist_middleware import (
    CONTEXT_TOKEN_TRIGGER,
    CONTEXT_TOOL_RESULTS_TO_KEEP,
    RUN_MODEL_CALL_LIMIT,
    RUN_TOOL_CALL_LIMIT,
    SEARCH_TOOLS,
    TOOL_MAX_RETRIES,
    build_specialist_middleware,
)


def test_specialist_middleware_limits_search_tools():
    middleware = build_specialist_middleware()

    model_limit = middleware[0]
    tool_limits = middleware[1 : 1 + len(SEARCH_TOOLS)]
    retry = middleware[-2]
    context = middleware[-1]

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

    assert isinstance(context, ContextEditingMiddleware)
    edit = context.edits[0]
    assert edit.trigger == CONTEXT_TOKEN_TRIGGER
    assert edit.keep == CONTEXT_TOOL_RESULTS_TO_KEEP
