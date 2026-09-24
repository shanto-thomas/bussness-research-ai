from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    ListFlowable,
    ListItem,
)

from business_research_ai.schemas.report import (
    BusinessResearchReport,
)


PDF_DIRECTORY = Path("generated_reports")


def generate_pdf(
    report: BusinessResearchReport,
    filename: str,
) -> str:

    PDF_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    pdf_path = PDF_DIRECTORY / filename

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # --------------------------------
    # Title
    # --------------------------------

    story.append(
        Paragraph(
            report.title,
            title_style,
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # --------------------------------
    # Helper: Add normal section
    # --------------------------------

    def add_section(
        title: str,
        content: str,
    ):
        story.append(
            Paragraph(
                title,
                heading_style,
            )
        )

        story.append(
            Paragraph(
                content or "No information available.",
                body_style,
            )
        )

        story.append(
            Spacer(1, 8)
        )

    # --------------------------------
    # Helper: Add list section
    # --------------------------------

    def add_list_section(
        title: str,
        items: list[str],
    ):
        story.append(
            Paragraph(
                title,
                heading_style,
            )
        )

        if items:

            list_items = [
                ListItem(
                    Paragraph(
                        item,
                        body_style,
                    )
                )
                for item in items
            ]

            story.append(
                ListFlowable(
                    list_items,
                    bulletType="bullet",
                )
            )

        else:

            story.append(
                Paragraph(
                    "None identified.",
                    body_style,
                )
            )

        story.append(
            Spacer(1, 8)
        )

    # --------------------------------
    # Executive Summary
    # --------------------------------

    add_section(
        "Executive Summary",
        report.executive_summary,
    )

    # --------------------------------
    # Business Overview
    # --------------------------------

    add_section(
        "Business Overview",
        report.business_overview,
    )

    # --------------------------------
    # Dynamic Research Sections
    # --------------------------------
    #
    # IMPORTANT:
    # Only selected research areas
    # will appear here.
    #

    for section in report.sections:

        add_section(
            section.title,
            section.content,
        )

    # --------------------------------
    # Opportunities
    # --------------------------------

    add_list_section(
        "Opportunities",
        report.opportunities,
    )

    # --------------------------------
    # Risks
    # --------------------------------

    add_list_section(
        "Risks",
        report.risks,
    )

    # --------------------------------
    # Assumptions
    # --------------------------------

    add_list_section(
        "Assumptions",
        report.assumptions,
    )

    # --------------------------------
    # Missing Information
    # --------------------------------

    add_list_section(
        "Missing Information",
        report.missing_information,
    )

    # --------------------------------
    # Conflicting Information
    # --------------------------------

    add_list_section(
        "Conflicting Information",
        report.conflicting_information,
    )

    # --------------------------------
    # Next Steps
    # --------------------------------

    add_list_section(
        "Next Steps",
        report.next_steps,
    )

    # --------------------------------
    # Generate PDF
    # --------------------------------

    document.build(story)

    return str(pdf_path)