import json

from business_research_ai.agents.research_router import (
    research_router,
)
from business_research_ai.services.research_area_service import (
    run_research_area,
)
from business_research_ai.services.session_service import (
    add_message,
    get_session,
    save_session,
)
from business_research_ai.services.synthesis_service import (
    synthesize_research,
)
from business_research_ai.services.report_service import (
    generate_report,
)
from business_research_ai.services.pdf_service import (
    generate_pdf,
)
from business_research_ai.utils.text import extract_text_content


def classify_intent(
    message: str,
) -> str:

    result = research_router.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    text = extract_text_content(
        final_message.content
    )

    try:

        data = json.loads(text)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Router returned invalid JSON: {text}"
        ) from exc

    return data["intent"]


def generate_final_report(
    session,
):
    """
    Phase 7 → Phase 8 → PDF
    """

    # --------------------------------
    # Phase 7
    # --------------------------------

    conversation_history = [
        message.model_dump()
        for message in session.conversation_history
    ]

    synthesized_research = synthesize_research(
        business_idea=session.business_idea,
        conversation_history=conversation_history,
        research_results=session.research_results,
        selected_areas=session.completed_areas,
    )

    session.synthesized_research = (
        synthesized_research.model_dump()
    )

    # --------------------------------
    # Phase 8
    # --------------------------------

    final_report = generate_report(
        business_idea=session.business_idea,
        conversation_history=conversation_history,
        selected_areas=session.completed_areas,
        research=synthesized_research,
    )

    session.final_report = (
        final_report.model_dump()
    )

    # --------------------------------
    # PDF
    # --------------------------------

    filename = (
        f"{session.session_id}.pdf"
    )

    pdf_path = generate_pdf(
        report=final_report,
        filename=filename,
    )

    session.pdf_path = pdf_path

    session.status = "completed"

    session.current_step = "completed"

    save_session(session)

    return {
        "session_id": session.session_id,
        "status": "completed",
        "report": final_report.model_dump(),
        "pdf_path": pdf_path,
    }

def process_message(
    session_id: str,
    message: str,
) -> dict:

    session = get_session(session_id)

    # --------------------------------
    # Save user message
    # --------------------------------

    add_message(
        session=session,
        role="user",
        content=message,
    )

    # --------------------------------
    # First message
    # --------------------------------

    if session.business_idea is None:

        session.business_idea = message

        assistant_message = (
            "Great. I understand your business idea.\n\n"
            "What would you like to research first?"
        )

        add_message(
            session=session,
            role="assistant",
            content=assistant_message,
        )

        session.current_step = "research_selection"

        save_session(session)

        return {
            "session_id": session.session_id,
            "message": assistant_message,
            "options": [
                "market",
                "competitors",
                "customers",
                "pricing",
                "finance",
                "legal",
                "technology",
                "complete_research",
            ],
        }

    # --------------------------------
    # Intent
    # --------------------------------

    intent = classify_intent(message)

    # --------------------------------
    # Individual research
    # --------------------------------

    if intent in {
        "market",
        "competitors",
        "customers",
        "pricing",
        "finance",
        "legal",
        "technology",
    }:

        result = run_research_area(
            area=intent,
            business_idea=session.business_idea,
        )

        session.research_results[
            intent
        ] = result

        if intent not in session.selected_areas:

            session.selected_areas.append(
                intent
            )

        if intent not in session.completed_areas:

            session.completed_areas.append(
                intent
            )

        assistant_message = (
            f"{intent.title()} research completed.\n\n"
            f"{result}\n\n"
            "Would you like to research another area "
            "or generate the final report?"
        )

        add_message(
            session=session,
            role="assistant",
            content=assistant_message,
        )

        session.current_step = "research_selection"

        save_session(session)

        available_areas = [
            area
            for area in [
                "market",
                "competitors",
                "customers",
                "pricing",
                "finance",
                "legal",
                "technology",
            ]
            if area not in session.completed_areas
        ]

        available_areas.append(
            "generate_report"
        )

        return {
            "session_id": session.session_id,
            "message": assistant_message,
            "completed_areas": (
                session.completed_areas
            ),
            "options": available_areas,
        }

    # --------------------------------
    # Complete research
    # --------------------------------

    if intent == "complete_research":

        all_areas = [
            "market",
            "competitors",
            "customers",
            "pricing",
            "finance",
            "legal",
            "technology",
        ]

        for area in all_areas:

            if area in session.completed_areas:
                continue

            result = run_research_area(
                area=area,
                business_idea=session.business_idea,
            )

            session.research_results[
                area
            ] = result

            session.selected_areas.append(
                area
            )

            session.completed_areas.append(
                area
            )

        session.current_step = "research_selection"

        assistant_message = (
            "Complete research has been collected.\n\n"
            "You can now generate the final report."
        )

        add_message(
            session=session,
            role="assistant",
            content=assistant_message,
        )

        save_session(session)

        return {
            "session_id": session.session_id,
            "message": assistant_message,
            "completed_areas": (
                session.completed_areas
            ),
            "options": [
                "generate_report"
            ],
        }

    # --------------------------------
    # Generate report
    # --------------------------------

    if intent == "generate_report":

        if not session.research_results:

            assistant_message = (
                "Please research at least one area "
                "before generating the report."
            )

            add_message(
                session=session,
                role="assistant",
                content=assistant_message,
            )

            save_session(session)

            return {
                "session_id": session.session_id,
                "message": assistant_message,
            }

        result = generate_final_report(
            session
        )

        add_message(
            session=session,
            role="assistant",
            content=(
                "Your business research report "
                "has been generated."
            ),
        )

        return result

    # --------------------------------
    # Unknown
    # --------------------------------

    assistant_message = (
        "I can research the market, competitors, "
        "customers, pricing, finance, legal requirements, "
        "or technology.\n\n"
        "You can also ask me to generate the final report."
    )

    add_message(
        session=session,
        role="assistant",
        content=assistant_message,
    )

    save_session(session)

    return {
        "session_id": session.session_id,
        "message": assistant_message,
    }