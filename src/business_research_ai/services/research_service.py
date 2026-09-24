import json

from business_research_ai.agents.main_agent import main_agent

from business_research_ai.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)

from business_research_ai.services.synthesis_service import (
    synthesize_research,
)
from business_research_ai.utils.text import extract_text_content

from business_research_ai.services.report_service import (
    generate_report,
)


def research_business(
    request: ResearchRequest,
) -> ResearchResponse:

    # -------------------------------
    # 1. Main Orchestrator
    # -------------------------------

    result = main_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.business_idea,
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    research_text = extract_text_content(
        final_message.content
    )

    # -------------------------------
    # 2. Parse research bundle
    # -------------------------------

    try:
        research_bundle = json.loads(
            research_text
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Main agent returned invalid JSON: "
            f"{research_text}"
        ) from exc

    # -------------------------------
    # 3. Collect specialist research
    # -------------------------------

    research_results = {
        "market_research": research_bundle.get(
            "market_research",
            "",
        ),
        "competitor_research": research_bundle.get(
            "competitor_research",
            "",
        ),
        "customer_research": research_bundle.get(
            "customer_research",
            "",
        ),
        "pricing_research": research_bundle.get(
            "pricing_research",
            "",
        ),
        "financial_analysis": research_bundle.get(
            "financial_analysis",
            "",
        ),
        "legal_research": research_bundle.get(
            "legal_research",
            "",
        ),
        "technology_analysis": research_bundle.get(
            "technology_analysis",
            "",
        ),
    }

    # -------------------------------
    # 4. Selected Areas
    # -------------------------------
    #
    # This is the old one-shot flow,
    # so we consider all research areas
    # selected.

    selected_areas = [
        "market",
        "competitors",
        "customers",
        "pricing",
        "finance",
        "legal",
        "technology",
    ]

    # -------------------------------
    # 5. Phase 7
    # Research Synthesizer
    # -------------------------------

    synthesized_research = synthesize_research(
        business_idea=request.business_idea,
        conversation_history=[],
        research_results=research_results,
        selected_areas=selected_areas,
    )

    # -------------------------------
    # 6. Phase 8
    # Report Generator
    # -------------------------------

    final_report = generate_report(
        business_idea=request.business_idea,
        conversation_history=[],
        selected_areas=selected_areas,
        research=synthesized_research,
    )

    # -------------------------------
    # 7. API response
    # -------------------------------

    return ResearchResponse(
        business_idea=request.business_idea,
        response=final_report.model_dump_json(
            indent=2
        ),
    )