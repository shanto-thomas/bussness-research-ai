from business_research_ai.tools.business_search import business_search
from business_research_ai.tools.news_search import news_search
from business_research_ai.tools.web_search import web_search
from business_research_ai.tools.website_reader import website_reader


def test_web_search():
    result = web_search.invoke(
        {"query": "tea market India"}
    )

    assert isinstance(result, str)
    assert result


def test_news_search():
    result = news_search.invoke(
        {"query": "tea industry India"}
    )

    assert isinstance(result, str)
    assert result


def test_business_search():
    result = business_search.invoke(
        {"query": "tea shops Kochi"}
    )

    assert isinstance(result, str)
    assert result


def test_website_reader():
    result = website_reader.invoke(
        {"url": "https://example.com"}
    )

    assert isinstance(result, str)
    assert result