import json
from typing import Any

from business_research_ai.agents.synthesis_agent import (
    synthesis_agent,
)
from business_research_ai.schemas.synthesis import (
    SynthesizedResearch,
)


def extract_text_content(content: Any) -> str:

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for block in content:

            if isinstance(block, dict):

                if block.get("type") == "text":

                    text = block.get("text")

                    if text:
                        parts.append(text)

            elif isinstance(block, str):

                parts.append(block)

        return "\n".join(parts)

    return str(content)


def synthesize_research(
    business_idea: str,
    conversation_history: list[dict],
    research_results: dict[str, str],
    selected_areas: list[str],
) -> SynthesizedResearch:

    payload = {
        "business_idea": business_idea,
        "conversation_history": conversation_history,
        "research_results": research_results,
    }

    prompt = f"""
You are now preparing the synthesized research dataset.

Business idea:

{business_idea}


Conversation history:

{json.dumps(
    conversation_history,
    indent=2,
)}


Specialist research:

{json.dumps(
    research_results,
    indent=2,
)}


Use both the conversation history and specialist research.

Important:

- User-provided information must be preserved.
- Specialist research must be preserved.
- Do not invent information.
- Do not perform new research.
- Identify missing information.
- Identify conflicting information.
- Separate assumptions from findings.

Return ONLY valid JSON.
"""

    result = synthesis_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    response_text = extract_text_content(
        final_message.content
    )

    try:

        parsed = json.loads(response_text)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Synthesis agent returned invalid JSON:\n"
            f"{response_text}"
        ) from exc

    try:

        return SynthesizedResearch.model_validate(
            parsed
        )

    except Exception as exc:

        raise ValueError(
            "Synthesis agent returned JSON that does "
            "not match SynthesizedResearch schema:\n"
            f"{json.dumps(parsed, indent=2)}"
        ) from exc