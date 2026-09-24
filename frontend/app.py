import json
import os
from pathlib import Path

import streamlit as st

from business_research_ai.clients.research_api import (
    ResearchApiClient,
    ResearchApiError,
)

AREAS = [
    "market",
    "competitors",
    "customers",
    "pricing",
    "finance",
    "legal",
    "technology",
]

OPTION_LABELS = {
    "market": "Market",
    "competitors": "Competitors",
    "customers": "Customers",
    "pricing": "Pricing",
    "finance": "Finance",
    "legal": "Legal",
    "technology": "Technology",
    "complete_research": "Research all areas",
    "generate_report": "Generate report",
}

OPTION_PROMPTS = {
    "market": "Research the market",
    "competitors": "Research the competitors",
    "customers": "Research the customers",
    "pricing": "Research pricing",
    "finance": "Research the finances",
    "legal": "Research legal requirements",
    "technology": "Research the technology",
    "complete_research": "Do complete research",
    "generate_report": "Generate the final report",
}

REPORT_LISTS = [
    ("opportunities", "Opportunities"),
    ("risks", "Risks"),
    ("assumptions", "Assumptions"),
    ("missing_information", "Missing information"),
    ("conflicting_information", "Conflicting information"),
    ("next_steps", "Next steps"),
]


def main() -> None:
    st.set_page_config(
        page_title="Business Research",
        page_icon="BR",
        layout="wide",
    )
    _init_state()

    st.title("Business Research")
    st.caption(
        "Describe a business idea, choose what to research, "
        "and generate a report through the existing API."
    )

    _render_sidebar()

    guided, full_report = st.tabs(["Guided research", ""])
    
    with guided:
        _render_guided()
    with full_report:
        _render_full_report()


def _init_state() -> None:
    defaults = {
        "api_base_url": os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
        "session_id": None,
        "messages": [],
        "options": [],
        "completed_areas": [],
        "status": None,
        "report": None,
        "pdf_path": None,
        "full_report": None,
        "full_report_idea": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _client() -> ResearchApiClient:
    return ResearchApiClient(st.session_state.api_base_url)


def _render_sidebar() -> None:
    with st.sidebar:
        st.header("API")
        st.session_state.api_base_url = st.text_input(
            "Base URL",
            value=st.session_state.api_base_url,
        )
        _render_health()

        st.divider()
        resume_id = st.text_input(
            "Resume session",
            placeholder="Session id",
        )
        if st.button("Load session", use_container_width=True):
            _resume_session(resume_id.strip())

        if st.button("New research", use_container_width=True):
            _reset_guided_session()
            st.rerun()

        if st.session_state.session_id:
            st.caption(f"Session `{st.session_state.session_id}`")
        if st.session_state.completed_areas:
            st.subheader("Completed")
            for area in st.session_state.completed_areas:
                st.write(OPTION_LABELS.get(area, area.title()))


def _render_health() -> None:
    try:
        with _client() as client:
            payload = client.health()
    except ResearchApiError:
        st.error("API is not reachable.")
        return
    status = payload.get("status", "unknown")
    st.success(f"API {status}")


def _render_guided() -> None:
    if st.session_state.session_id is None:
        _render_idea_form()
        return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.options:
        _render_options(st.session_state.options)

    prompt = st.chat_input("Ask for a research area or a report")
    if prompt:
        _send_guided_message(prompt)

    if st.session_state.report:
        st.divider()
        _render_report(
            st.session_state.report,
            st.session_state.pdf_path,
        )


def _render_idea_form() -> None:
    with st.form("business_idea"):
        idea = st.text_area(
            "Business idea",
            placeholder="A marketplace that helps local shops sell online.",
            height=140,
        )
        submitted = st.form_submit_button("Start research", type="primary")

    if submitted:
        _start_session(idea.strip())


def _render_options(options: list[str]) -> None:
    st.write("Choose a next step")
    columns = st.columns(4)
    for index, option in enumerate(options):
        label = OPTION_LABELS.get(option, option.replace("_", " ").title())
        button_type = "primary" if option == "generate_report" else "secondary"
        with columns[index % 4]:
            if st.button(
                label,
                key=f"option-{option}",
                type=button_type,
                use_container_width=True,
            ):
                _send_guided_message(OPTION_PROMPTS.get(option, label))


def _render_full_report() -> None:
    with st.form("full_research"):
        idea = st.text_area(
            "Business idea",
            value=st.session_state.full_report_idea,
            placeholder="A marketplace that helps local shops sell online.",
            height=140,
        )
        submitted = st.form_submit_button(
            "Run full research",
            type="primary",
        )

    if submitted:
        _run_full_research(idea.strip())

    if st.session_state.full_report:
        st.divider()
        _render_report(st.session_state.full_report, pdf_path=None)


def _start_session(idea: str) -> None:
    if len(idea) < 5:
        st.warning("Enter a business idea of at least 5 characters.")
        return

    try:
        with _client() as client, st.spinner("Starting a research session..."):
            created = client.create_session()
            payload = client.send_message(created["session_id"], idea)
    except ResearchApiError as exc:
        st.error(str(exc))
        return

    st.session_state.session_id = created["session_id"]
    st.session_state.status = created.get("status")
    _apply_message_response(idea, payload)
    st.rerun()


def _send_guided_message(message: str) -> None:
    if not message.strip():
        return

    try:
        with (
            _client() as client,
            st.spinner("Research in progress. This can take several minutes."),
        ):
            payload = client.send_message(
                st.session_state.session_id,
                message,
            )
    except ResearchApiError as exc:
        st.error(str(exc))
        return

    _apply_message_response(message, payload)
    st.rerun()


def _apply_message_response(user_message: str, payload: dict) -> None:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    assistant_message = payload.get("message")
    if not assistant_message and payload.get("status") == "completed":
        assistant_message = "Your business research report has been generated."
    if assistant_message:
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message}
        )

    if "options" in payload:
        st.session_state.options = payload["options"]
    elif payload.get("status") == "completed":
        st.session_state.options = []

    if "completed_areas" in payload:
        st.session_state.completed_areas = payload["completed_areas"]
    if payload.get("report"):
        st.session_state.report = payload["report"]
    if payload.get("pdf_path"):
        st.session_state.pdf_path = payload["pdf_path"]
    if payload.get("status"):
        st.session_state.status = payload["status"]


def _resume_session(session_id: str) -> None:
    if not session_id:
        st.sidebar.warning("Enter a session id.")
        return

    try:
        with _client() as client:
            session = client.get_session(session_id)
    except ResearchApiError as exc:
        st.sidebar.error(str(exc))
        return

    st.session_state.session_id = session["session_id"]
    st.session_state.messages = session.get("conversation_history", [])
    st.session_state.completed_areas = session.get("completed_areas", [])
    st.session_state.status = session.get("status")
    st.session_state.report = session.get("final_report")
    st.session_state.pdf_path = session.get("pdf_path")
    st.session_state.options = _options_from_session(session)
    st.rerun()


def _options_from_session(session: dict) -> list[str]:
    if session.get("status") == "completed" or session.get("final_report"):
        return []
    if not session.get("business_idea"):
        return []

    completed = set(session.get("completed_areas") or [])
    remaining = [area for area in AREAS if area not in completed]
    if not completed:
        return [*AREAS, "complete_research"]
    if not remaining:
        return ["generate_report"]
    return [*remaining, "generate_report"]


def _run_full_research(idea: str) -> None:
    if len(idea) < 5:
        st.warning("Enter a business idea of at least 5 characters.")
        return

    st.session_state.full_report_idea = idea
    try:
        with (
            _client() as client,
            st.spinner("Running full research. This can take several minutes."),
        ):
            payload = client.create_research(idea)
    except ResearchApiError as exc:
        st.error(str(exc))
        return

    st.session_state.full_report = _parse_report(payload.get("response"))
    st.rerun()


def _parse_report(raw_report: str | dict | None) -> dict | None:
    if isinstance(raw_report, dict):
        return raw_report
    if not isinstance(raw_report, str) or not raw_report.strip():
        return None
    try:
        parsed = json.loads(raw_report)
    except json.JSONDecodeError:
        return {"title": "Research result", "executive_summary": raw_report}
    return parsed if isinstance(parsed, dict) else None


def _render_report(report: dict, pdf_path: str | None) -> None:
    st.header(report.get("title") or "Research report")

    if report.get("executive_summary"):
        st.subheader("Executive summary")
        st.write(report["executive_summary"])

    if report.get("business_overview"):
        st.subheader("Business overview")
        st.write(report["business_overview"])

    for section in report.get("sections") or []:
        if not isinstance(section, dict):
            continue
        st.subheader(section.get("title") or "Section")
        st.write(section.get("content") or "")

    for key, label in REPORT_LISTS:
        items = report.get(key) or []
        if not items:
            continue
        st.subheader(label)
        for item in items:
            st.markdown(f"- {item}")

    pdf_file = Path(pdf_path) if pdf_path else None
    if pdf_file and pdf_file.is_file():
        st.download_button(
            "Download PDF",
            data=pdf_file.read_bytes(),
            file_name=pdf_file.name,
            mime="application/pdf",
        )
    elif pdf_path:
        st.caption(f"PDF saved on the API host at `{pdf_path}`.")


def _reset_guided_session() -> None:
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.options = []
    st.session_state.completed_areas = []
    st.session_state.status = None
    st.session_state.report = None
    st.session_state.pdf_path = None


main()
