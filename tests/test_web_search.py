from business_research_ai.tools.web_search import web_search


def test_web_search():
    result = web_search.invoke(
        {
            "query": "premium tea shops in Kochi"
        }
    )
    assert isinstance(result, str)
    assert len(result) > 0