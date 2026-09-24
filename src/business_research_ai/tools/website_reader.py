import httpx
from bs4 import BeautifulSoup
from langchain.tools import tool


@tool
def website_reader(url: str) -> str:
    """
    Read and extract useful text content from a website URL.

    Use this when a research agent needs detailed information
    from a specific company or business website.
    """

    if not url.strip():
        return "Website URL cannot be empty."

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/120.0 Safari/537.36"
            )
        }

        with httpx.Client(
            timeout=15.0,
            follow_redirects=True,
            headers=headers,
        ) as client:

            response = client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Remove unnecessary elements.
        for element in soup(
            ["script", "style", "noscript", "svg"]
        ):
            element.decompose()

        title = soup.title.get_text(strip=True) if soup.title else ""

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        # Avoid sending extremely large pages to the LLM.
        text = text[:15000]

        return f"""
Website: {url}

Title:
{title}

Content:
{text}
""".strip()

    except httpx.HTTPError as exc:
        return f"Website request failed: {exc}"

    except Exception as exc:
        return f"Website reading failed: {exc}"