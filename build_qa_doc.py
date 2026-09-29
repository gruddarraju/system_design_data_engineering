from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).parent
SRC = ROOT / "Senior_Data_Engineer_System_Design_QA.md"
OUT = ROOT / "Campfire_Senior_Data_Engineer_System_Design_QA.docx"

NAVY = "0C1930"
TEAL = "00AAA0"
BLUE = "4385F5"
ORANGE = "FF9F43"
DARK = "253042"
MID = "74849A"
LIGHT = "E4EBF4"
OFFWHITE = "F7F9FC"
WHITE = "FFFFFF"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Page ")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor.from_string(MID)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)


def style_document(doc):
    sec = doc.sections[0]
    sec.top_margin = Inches(0.72)
    sec.bottom_margin = Inches(0.68)
    sec.left_margin = Inches(0.78)
    sec.right_margin = Inches(0.78)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10.2)
    normal.font.color.rgb = RGBColor.from_string(DARK)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08

    for name, size, color, before, after in [
        ("Title", 34, NAVY, 0, 12),
        ("Subtitle", 16, TEAL, 0, 10),
        ("Heading 1", 22, NAVY, 10, 8),
        ("Heading 2", 15, BLUE, 9, 5),
        ("Heading 3", 11, TEAL, 6, 2),
    ]:
        st = doc.styles[name]
        st.font.name = "Aptos Display" if name != "Heading 3" else "Aptos"
        st.font.size = Pt(size)
        st.font.bold = name != "Subtitle"
        st.font.color.rgb = RGBColor.from_string(color)
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.keep_with_next = True

    for name in ("List Bullet", "List Number"):
        st = doc.styles[name]
        st.font.name = "Aptos"
        st.font.size = Pt(10)
        st.font.color.rgb = RGBColor.from_string(DARK)
        st.paragraph_format.space_after = Pt(2)


def add_header_footer(section):
    header = section.header
    p = header.paragraphs[0]
    p.text = "SENIOR DATA ENGINEER  |  SYSTEM DESIGN Q&A"
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in p.runs:
        r.font.name = "Aptos"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = RGBColor.from_string(TEAL)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "5")
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), LIGHT)
    pbdr.append(bottom)
    pPr.append(pbdr)

    footer = section.footer
    add_page_number(footer.paragraphs[0])


def add_cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(85)
    r = p.add_run("SENIOR DATA ENGINEER")
    r.font.name = "Aptos Display"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor.from_string(ORANGE)

    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("System Design\nInterview Guide")

    p = doc.add_paragraph(style="Subtitle")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("28 detailed questions, model answers, AI ERP architecture, and Campfire-focused interview preparation")

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    labels = [("ARCHITECTURE", TEAL), ("MODELING", BLUE), ("RELIABILITY", "855CF8"), ("AI ERP", ORANGE)]
    for cell, (label, color) in zip(table.rows[0].cells, labels):
        set_cell_shading(cell, color)
        set_cell_margins(cell, 100, 100, 100, 100)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(label)
        r.font.name = "Aptos"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(80)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("A practical preparation document for senior-level data engineering interviews")
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor.from_string(MID)

    doc.add_page_break()


def add_contents(doc, text):
    doc.add_heading("Contents", level=1)
    section_names = re.findall(r"^# (Section \d+ — .+)$", text, flags=re.M)
    questions = re.findall(r"^## (Q\d+\. .+)$", text, flags=re.M)
    q_by_section = []
    lines = text.splitlines()
    current = None
    for line in lines:
        if line.startswith("# Section "):
            current = [line[2:], []]
            q_by_section.append(current)
        elif line.startswith("## Q") and current:
            current[1].append(line[3:])
    for sec, qs in q_by_section:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        r = p.add_run(sec)
        r.bold = True
        r.font.color.rgb = RGBColor.from_string(NAVY)
        for q in qs:
            p = doc.add_paragraph(q, style="List Bullet")
            p.paragraph_format.left_indent = Inches(0.25)
    for label in ("Senior-Level Evaluation Rubric", "Final Interview Checklist", "Additional Practice Prompts"):
        p = doc.add_paragraph()
        r = p.add_run(label)
        r.bold = True
        r.font.color.rgb = RGBColor.from_string(NAVY)
    doc.add_page_break()


def add_quote(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.right_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(7)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "EAF9F7")
    pPr.append(shd)
    r = p.add_run(text)
    r.italic = True
    r.font.color.rgb = RGBColor.from_string(NAVY)
    return p


def add_markdown_table(doc, lines):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c or "---") for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell = table.cell(i, j)
            cell.text = row[j] if j < len(row) else ""
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if i == 0:
                set_cell_shading(cell, NAVY)
            elif i % 2 == 0:
                set_cell_shading(cell, OFFWHITE)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Aptos"
                    r.font.size = Pt(8.6)
                    r.font.bold = i == 0
                    r.font.color.rgb = RGBColor(255,255,255) if i == 0 else RGBColor.from_string(DARK)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def process_body(doc, text):
    # Skip markdown title/subtitle metadata; start at How to Use.
    start = text.find("## How to Answer a System-Design Question")
    body = text[start:] if start >= 0 else text
    lines = body.splitlines()
    i = 0
    first_section = True
    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line or line == "---":
            i += 1
            continue
        if line.startswith("|" ):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            add_markdown_table(doc, table_lines)
            continue
        if line.startswith("# Section "):
            if not first_section:
                doc.add_page_break()
            first_section = False
            doc.add_heading(line[2:], level=1)
        elif line.startswith("# "):
            doc.add_page_break()
            doc.add_heading(line[2:], level=1)
        elif line.startswith("## Q"):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:], level=3)
        elif line.startswith("> "):
            add_quote(doc, line[2:].strip("\"") )
        elif re.match(r"^\d+\.\s", line):
            doc.add_paragraph(re.sub(r"^\d+\.\s+", "", line), style="List Number")
        elif line.startswith("- "):
            doc.add_paragraph(line[2:], style="List Bullet")
        elif line.startswith("**") and line.endswith("**"):
            p = doc.add_paragraph()
            r = p.add_run(line.strip("*"))
            r.bold = True
            r.font.color.rgb = RGBColor.from_string(NAVY)
        else:
            p = doc.add_paragraph()
            # Light inline markdown support for **bold**.
            parts = re.split(r"(\*\*[^*]+\*\*)", line)
            for part in parts:
                if not part:
                    continue
                if part.startswith("**") and part.endswith("**"):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                else:
                    p.add_run(part)
        i += 1


def main():
    text = SRC.read_text(encoding="utf-8")
    doc = Document()
    style_document(doc)
    add_header_footer(doc.sections[0])
    add_cover(doc)
    add_contents(doc, text)
    process_body(doc, text)
    doc.core_properties.title = "Senior Data Engineer System Design Interview Guide"
    doc.core_properties.subject = "28 detailed system-design questions, AI ERP scenarios, and Campfire-focused preparation"
    doc.core_properties.author = "Kiro"
    doc.core_properties.keywords = "senior data engineer, system design, interview, data architecture, AI ERP, Campfire"
    doc.core_properties.comments = "Generated from Senior_Data_Engineer_System_Design_QA.md using the user-provided Campfire prep summary"
    doc.save(OUT)
    print(f"Created {OUT}")
    print(f"Bytes: {OUT.stat().st_size}")
    print(f"Questions: {sum(1 for line in text.splitlines() if line.startswith('## Q'))}")


if __name__ == "__main__":
    main()
