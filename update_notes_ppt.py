from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).parent
SRC = ROOT / "notes_ppt.docx"
OUT = ROOT / "notes_ppt_updated.docx"


def insert_after(paragraph, parts, style="Normal"):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    new_para.style = style
    for text, bold in parts:
        run = new_para.add_run(text)
        run.bold = bold
    return new_para


def find_paragraph(doc, text):
    return next(p for p in doc.paragraphs if p.text.strip() == text)


def find_next(doc, start_paragraph, text):
    paragraphs = doc.paragraphs
    start = next(i for i, p in enumerate(paragraphs) if p._p is start_paragraph._p)
    return next(p for p in paragraphs[start + 1:] if p.text.strip() == text)


def insert_before_label(doc, section_heading, label, entries):
    heading = find_paragraph(doc, section_heading)
    target = find_next(doc, heading, label)
    previous = Paragraph(target._p.getprevious(), target._parent)
    cursor = previous
    for entry in entries:
        cursor = insert_after(cursor, entry)


def main():
    doc = Document(SRC)

    # Explicit Campfire-tailored title.
    title = doc.paragraphs[0]
    title.text = "Campfire-Tailored Data Engineering System Design and AI ERP Interview Notes"
    title.style = "Title"

    # Add missing company and candidate context to the existing mission/value section.
    insert_before_label(
        doc,
        "Mission, Values, and Engineering Priorities",
        "Key takeaway:",
        [
            [
                ("Company context from the supplied guide: ", True),
                ("Campfire is described as a Series B AI-native ERP backed by Accel and Ribbit Capital, with more than $100M raised, 300+ global customers, and offices in San Francisco, New York City, and London. Use these details to understand the growth stage and global operating context; confirm current figures with Campfire.", False),
            ],
            [
                ("Candidate profile from the supplied guide: ", True),
                ("show low ego, high standards with speed, genuine curiosity, mission alignment, transparent and direct communication, deep customer empathy, and a team-first approach. Demonstrate these traits through specific decisions and outcomes rather than repeating the labels.", False),
            ],
        ],
    )

    # Make the interview process and onsite expectations explicit.
    insert_before_label(
        doc,
        "Interview Logistics and Collaborative Discussion",
        "Key takeaway:",
        [
            [
                ("Interview sequence from the supplied guide: ", True),
                ("Recruiter Screen → Team Chat → virtual assessment over Google Meet or Zoom, followed by an approximately three-hour onsite in San Francisco, New York City, or London when applicable. Treat the stages as collaborative conversations: pause, think aloud, and ask clarifying questions.", False),
            ],
            [
                ("Preparation reminder: ", True),
                ("test camera, microphone, and internet the night before; choose smart casual clothing that feels natural; and prepare two or three outcome-driven stories with customer impact, your specific contribution, measurable results, mistakes, and learning.", False),
            ],
        ],
    )

    # Add explicit attribution and freshness warning to the source section.
    insert_before_label(
        doc,
        "Source Notes and Responsible Use",
        "Key takeaway:",
        [
            [
                ("Campfire attribution and freshness note: ", True),
                ("the company profile, funding, customer count, offices, mission, values, candidate traits, and interview-process details were supplied by the user from a Campfire candidate prep guide. They were not independently verified while updating this document and may change; confirm time-sensitive details with Campfire or current recruiting materials.", False),
            ],
        ],
    )

    # Fill core document metadata, which was empty in the source file.
    props = doc.core_properties
    props.title = "Campfire-Tailored Data Engineering System Design and AI ERP Interview Notes"
    props.subject = "Speaker notes and preparation guidance for senior data engineering and AI-native ERP interviews"
    props.author = "Kiro; source document author retained in document history"
    props.keywords = "Campfire, senior data engineer, system design, AI ERP, accounting, finance, interview notes"
    props.comments = "Updated from notes_ppt.docx using the user-provided Campfire candidate guide summary; original preserved."

    # Keep body typography consistent for inserted text.
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if not run.font.name:
                run.font.name = "Aptos"
            if run.font.size is None and paragraph.style.name == "Normal":
                run.font.size = Pt(10.5)
            if run.font.color.rgb is None and paragraph.style.name == "Normal":
                run.font.color.rgb = RGBColor(37, 48, 66)

    doc.save(OUT)
    print(f"Created {OUT}")
    print(f"Bytes: {OUT.stat().st_size}")


if __name__ == "__main__":
    main()
