import json

from business_research_ai.agents.report_agent import report_agent
from business_research_ai.schemas.report import BusinessResearchReport
from business_research_ai.schemas.synthesis import SynthesizedResearch
from business_research_ai.services.synthesis_service import extract_text_content


def generate_report(
    business_idea: str,
    conversation_history: list[dict],
    selected_areas: list[str],
    research: SynthesizedResearch,
) -> BusinessResearchReport:

    report_context = {
        "business_idea": business_idea,
        "conversation_history": conversation_history,
        "selected_areas": selected_areas,
        "synthesized_research": research.model_dump(),
    }

    prompt = f"""
Generate the final business research report.

Selected Research Areas:
{json.dumps(selected_areas, indent=2)}

Use the following information:

{json.dumps(
    report_context,
    indent=2,
)}

IMPORTANT:

Generate detailed report sections ONLY for the selected
research areas.

For example, if selected_areas is:

["customers"]

then the report must contain only:

"Customer Analysis"

Do NOT generate:

- Market Analysis
- Competitor Analysis
- Pricing Analysis
- Financial Analysis
- Legal Analysis
- Technology Analysis


If selected_areas is:

["customers", "competitors", "pricing"]

then the report must contain:

- Customer Analysis
- Competitor Analysis
- Pricing Analysis

and must NOT contain any other detailed research sections.


The report must be based ONLY on the supplied information.

Do not:

- invent facts
- invent competitors
- invent pricing
- invent financial numbers
- invent legal requirements
- invent market statistics
- perform new web searches

Preserve:

- uncertainties
- assumptions
- risks
- missing information
- conflicting information


The JSON structure MUST be:

{{
    "title": "string",
    "executive_summary": "string",
    "business_overview": "string",

    "sections": [
        {{
            "title": "string",
            "content": "string"
        }}
    ],

    "opportunities": ["string"],
    "risks": ["string"],
    "assumptions": ["string"],
    "missing_information": ["string"],
    "conflicting_information": ["string"],
    "next_steps": ["string"]
}}


IMPORTANT JSON RULES:

1. Return ONLY valid JSON.

2. Do not use these as JSON keys:

   - market_analysis
   - competitor_analysis
   - customer_analysis
   - pricing_analysis
   - financial_analysis
   - legal_analysis
   - technology_analysis

3. All detailed research must be inside the "sections" array.

4. Each section MUST have:

   "title": "string"
   "content": "string"

5. Do not create sections for unselected research areas.

6. Do not create additional top-level JSON keys.

7. If information is unavailable, do not invent it.

Return ONLY JSON.
"""

    result = report_agent.invoke(
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
            "Report agent returned invalid JSON:\n"
            f"{response_text}"
        ) from exc

    try:
        return BusinessResearchReport.model_validate(
            parsed
        )

    except Exception as exc:
        raise ValueError(
            "Report agent returned JSON that does "
            "not match BusinessResearchReport schema:\n"
            f"{json.dumps(parsed, indent=2)}"
        ) from exc