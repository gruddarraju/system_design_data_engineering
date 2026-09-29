from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE

OUT = Path(__file__).with_name("Campfire_Data_Engineering_System_Design_Playbook.pptx")

# ---------- Theme ----------
NAVY = RGBColor(12, 25, 48)
NAVY_2 = RGBColor(20, 40, 70)
TEAL = RGBColor(0, 170, 160)
TEAL_DARK = RGBColor(0, 120, 116)
ORANGE = RGBColor(255, 159, 67)
BLUE = RGBColor(67, 133, 245)
PURPLE = RGBColor(133, 92, 248)
GREEN = RGBColor(57, 181, 74)
RED = RGBColor(227, 76, 89)
YELLOW = RGBColor(255, 205, 64)
WHITE = RGBColor(255, 255, 255)
OFFWHITE = RGBColor(247, 249, 252)
LIGHT = RGBColor(228, 235, 244)
MID = RGBColor(116, 132, 154)
DARK = RGBColor(37, 48, 66)
CODE_BG = RGBColor(18, 28, 45)
BRONZE = RGBColor(177, 111, 63)
SILVER = RGBColor(154, 164, 176)
GOLD = RGBColor(214, 162, 42)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def set_bg(slide, color=OFFWHITE):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, x, y, w, h, fill, radius=True, line=None, line_width=1):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(line_width)
    return shape


def add_text(slide, text, x, y, w, h, size=18, color=DARK, bold=False,
             font="Aptos", align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
             margin=0.05, italic=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return box


def add_rich_lines(slide, lines, x, y, w, h, size=18, color=DARK, bullet=True,
                   bullet_color=None, spacing=7, font="Aptos"):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.margin_left = Inches(0.07)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)
    for i, item in enumerate(lines):
        if isinstance(item, tuple):
            head, body = item
        else:
            head, body = "", item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(spacing)
        p.line_spacing = 1.05
        if bullet:
            p.text = "• "
            p.runs[0].font.color.rgb = bullet_color or TEAL
            p.runs[0].font.bold = True
        if head:
            r = p.add_run()
            r.text = head
            r.font.bold = True
            r.font.color.rgb = color
            r.font.name = font
            r.font.size = Pt(size)
        r = p.add_run()
        r.text = body
        r.font.color.rgb = color
        r.font.name = font
        r.font.size = Pt(size)
    return box


def add_title(slide, title, subtitle=None, section=None, dark=False):
    color = WHITE if dark else NAVY
    if section:
        add_text(slide, section.upper(), 0.55, 0.18, 3.2, 0.27, 9, TEAL if not dark else ORANGE, True)
    add_text(slide, title, 0.55, 0.48 if section else 0.3, 12.1, 0.55, 26, color, True)
    if subtitle:
        add_text(slide, subtitle, 0.57, 1.03, 12.0, 0.4, 11, MID if not dark else LIGHT)
    # accent
    add_rect(slide, 0.55, 1.42 if subtitle else 1.03, 1.05, 0.055, TEAL, False)


def add_footer(slide, num, source=None, dark=False):
    line_color = RGBColor(60, 80, 105) if dark else LIGHT
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.55), Inches(7.16), Inches(12.78), Inches(7.16))
    line.line.color.rgb = line_color
    line.line.width = Pt(0.7)
    footer_color = LIGHT if dark else MID
    if source:
        add_text(slide, source, 0.57, 7.2, 11.5, 0.2, 7.5, footer_color)
    add_text(slide, f"{num:02d}", 12.25, 7.18, 0.5, 0.22, 8, footer_color, True, align=PP_ALIGN.RIGHT)


def add_slide(title, subtitle=None, section=None, bg=OFFWHITE, source=None):
    slide = prs.slides.add_slide(BLANK)
    set_bg(slide, bg)
    dark = bg == NAVY or bg == NAVY_2 or bg == CODE_BG
    add_title(slide, title, subtitle, section, dark)
    add_footer(slide, len(prs.slides), source, dark)
    return slide


def card(slide, x, y, w, h, title, body, accent=TEAL, number=None, title_size=16, body_size=11):
    add_rect(slide, x, y, w, h, WHITE, True, LIGHT, 0.8)
    add_rect(slide, x, y, 0.07, h, accent, False)
    if number is not None:
        add_rect(slide, x+0.18, y+0.16, 0.42, 0.42, accent, True)
        add_text(slide, str(number), x+0.18, y+0.2, 0.42, 0.25, 11, WHITE, True, align=PP_ALIGN.CENTER)
        tx = x+0.72
        tw = w-0.9
    else:
        tx = x+0.23
        tw = w-0.4
    add_text(slide, title, tx, y+0.14, tw, 0.35, title_size, NAVY, True)
    add_text(slide, body, x+0.23, y+0.65, w-0.43, h-0.78, body_size, DARK)


def add_chip(slide, text, x, y, w, fill=LIGHT, color=NAVY):
    add_rect(slide, x, y, w, 0.34, fill, True)
    add_text(slide, text, x, y+0.055, w, 0.2, 9, color, True, align=PP_ALIGN.CENTER)


def arrow(slide, x1, y1, x2, y2, color=TEAL, width=2, dashed=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    c.line.end_arrowhead = True
    if dashed:
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return c


def node(slide, x, y, w, h, title, subtitle="", fill=WHITE, accent=TEAL, title_size=13):
    add_rect(slide, x, y, w, h, fill, True, accent, 1.2)
    add_text(slide, title, x+0.12, y+0.12, w-0.24, 0.28, title_size, NAVY, True, align=PP_ALIGN.CENTER)
    if subtitle:
        add_text(slide, subtitle, x+0.12, y+0.47, w-0.24, h-0.55, 9, DARK, align=PP_ALIGN.CENTER)


def add_table(slide, rows, x, y, w, h, col_widths=None, header_fill=NAVY, font_size=10):
    nrows, ncols = len(rows), len(rows[0])
    shape = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(h))
    table = shape.table
    if col_widths:
        for i, cw in enumerate(col_widths):
            table.columns[i].width = Inches(cw)
    for r in range(nrows):
        for c in range(ncols):
            cell = table.cell(r, c)
            cell.text = str(rows[r][c])
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.03)
            cell.fill.solid()
            cell.fill.fore_color.rgb = header_fill if r == 0 else (WHITE if r % 2 else OFFWHITE)
            cell.border_top = None
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.vertical_anchor = MSO_ANCHOR.MIDDLE
            for run in p.runs:
                run.font.name = "Aptos"
                run.font.size = Pt(font_size if r else font_size-0.5)
                run.font.bold = r == 0
                run.font.color.rgb = WHITE if r == 0 else DARK
    return table


def add_code(slide, code, x, y, w, h, label=None, size=10.2):
    add_rect(slide, x, y, w, h, CODE_BG, True)
    if label:
        add_rect(slide, x+0.18, y+0.12, 1.2, 0.28, TEAL_DARK, True)
        add_text(slide, label, x+0.18, y+0.17, 1.2, 0.15, 8, WHITE, True, align=PP_ALIGN.CENTER)
        top = y+0.5
        height = h-0.58
    else:
        top = y+0.16
        height = h-0.25
    box = slide.shapes.add_textbox(Inches(x+0.18), Inches(top), Inches(w-0.36), Inches(height))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = code
    p.line_spacing = 1.0
    for r in p.runs:
        r.font.name = "Cascadia Mono"
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(221, 231, 242)
    return box


def add_callout(slide, text, x, y, w, h, fill=RGBColor(230, 249, 247), accent=TEAL, size=11):
    add_rect(slide, x, y, w, h, fill, True, accent, 1)
    add_text(slide, text, x+0.16, y+0.13, w-0.3, h-0.2, size, NAVY, True)


# ---------- Slides ----------
# 1. Cover
slide = prs.slides.add_slide(BLANK)
set_bg(slide, NAVY)
add_rect(slide, 0, 0, 13.333, 0.11, TEAL, False)
add_text(slide, "DATA ENGINEERING", 0.78, 0.74, 3.7, 0.3, 11, ORANGE, True)
add_text(slide, "System Design\nInterview Playbook", 0.75, 1.25, 8.0, 1.65, 36, WHITE, True)
add_text(slide, "A practical, end-to-end method for turning ambiguity into a scalable, reliable data platform", 0.8, 3.2, 6.8, 0.75, 16, LIGHT)
for i, (label, color) in enumerate([("REQUIREMENTS", TEAL), ("ARCHITECTURE", BLUE), ("MODELING", PURPLE), ("OPERATIONS", ORANGE)]):
    add_chip(slide, label, 0.8+i*1.62, 4.35, 1.42, color, WHITE)
add_callout(slide, "INCLUDES CAMPFIRE-TAILORED AI ERP PREP + COMPLEX INTERVIEW Q&As", 0.8, 5.15, 6.65, 0.62, RGBColor(35, 58, 84), ORANGE, 9.8)
# right-side visual pipeline
xs = [8.1, 9.45, 10.8, 12.15]
labels = [("01", "Ingest"), ("02", "Transform"), ("03", "Store"), ("04", "Serve")]
for i, (num, lab) in enumerate(labels):
    add_rect(slide, xs[i], 1.55+i*0.85, 0.86, 0.86, [TEAL, BLUE, PURPLE, ORANGE][i], True)
    add_text(slide, num, xs[i], 1.7+i*0.85, 0.86, 0.2, 11, WHITE, True, align=PP_ALIGN.CENTER)
    add_text(slide, lab, xs[i]-0.12, 2.43+i*0.85, 1.1, 0.22, 9, LIGHT, True, align=PP_ALIGN.CENTER)
    if i < 3:
        arrow(slide, xs[i]+0.88, 1.98+i*0.85, xs[i+1]-0.03, 2.83+i*0.85, LIGHT, 1.5)
add_text(slide, "Based on the six-step framework described in Afaque Ahmad’s video", 0.8, 6.52, 8.0, 0.28, 9, MID)
add_footer(slide, 1, "Source: user-provided summary of https://www.youtube.com/watch?v=r58Cf_kc_bY", True)

# 2
slide = add_slide("What you will be able to do", "Use this deck as a study guide, design template, and interview narration script.", "Orientation")
items = [
    ("Frame the problem", "Clarify users, outputs, SLAs, volume, retention, compliance, and failure tolerance before choosing tools."),
    ("Estimate the system", "Convert users and events into throughput, storage, partition counts, compute needs, and cost pressure."),
    ("Choose deliberately", "Select batch vs. streaming, architecture style, serving layer, file format, and data model by trade-off."),
    ("Design for reality", "Build in quality, observability, idempotency, replay, schema evolution, scaling, and disaster recovery."),
]
for i, (t, b) in enumerate(items):
    card(slide, 0.7+(i%2)*6.15, 1.75+(i//2)*2.2, 5.75, 1.75, t, b, [TEAL, BLUE, PURPLE, ORANGE][i], i+1)
add_callout(slide, "Core principle: architecture is the consequence of requirements—not a collection of favorite technologies.", 2.05, 6.28, 9.2, 0.55)

# 3
slide = add_slide("System design is an argument, not a diagram", "Interviewers evaluate how you reason under ambiguity and explain trade-offs.", "Mindset", bg=NAVY)
add_text(slide, "A strong answer repeatedly connects:", 0.75, 1.72, 4.0, 0.35, 16, WHITE, True)
sequence = [("Requirement", TEAL), ("Constraint", BLUE), ("Decision", PURPLE), ("Trade-off", ORANGE), ("Risk control", GREEN)]
for i, (lab, c) in enumerate(sequence):
    x = 0.78+i*2.47
    add_rect(slide, x, 2.38, 1.86, 0.72, c, True)
    add_text(slide, lab, x, 2.61, 1.86, 0.2, 12, WHITE, True, align=PP_ALIGN.CENTER)
    if i < len(sequence)-1:
        arrow(slide, x+1.87, 2.74, x+2.38, 2.74, LIGHT, 1.5)
add_text(slide, "Example narration", 0.8, 3.7, 2.5, 0.3, 14, ORANGE, True)
quote = "“Restaurant dashboards need <2-minute freshness, so I’ll use a streaming path. That raises operational complexity, so I’ll isolate stateful logic, checkpoint progress, retain Kafka events for replay, and keep the daily executive path on the lakehouse.”"
add_text(slide, quote, 0.82, 4.14, 11.65, 1.15, 18, WHITE, False, italic=True)
add_callout(slide, "Weak: name tools first.  Strong: state assumption → quantify → decide → acknowledge downside → mitigate.", 1.55, 5.75, 10.2, 0.62, RGBColor(35, 58, 84), ORANGE, 12)

# 4
slide = add_slide("The six-step mental map", "Keep this order visible while you design; revisit earlier steps when assumptions change.", "Framework")
steps = [
    ("Requirements", "Who, what, how, SLA, scale", TEAL),
    ("Pipeline", "Batch/stream; orchestration", BLUE),
    ("Model", "Medallion, facts, dimensions", PURPLE),
    ("Storage", "Formats, tables, layout", ORANGE),
    ("Quality", "Contracts, tests, telemetry", GREEN),
    ("Operations", "Replay, scale, DR, cost", RED),
]
for i, (t, b, c) in enumerate(steps):
    x = 0.7+(i%3)*4.2
    y = 1.75+(i//3)*2.15
    card(slide, x, y, 3.8, 1.55, t, b, c, i+1, 15, 11)
    if i in [0,1,3,4]:
        arrow(slide, x+3.83, y+0.78, x+4.12, y+0.78, MID, 1.4)
arrow(slide, 11.9, 3.32, 11.9, 3.77, MID, 1.4)
add_callout(slide, "At every step ask: What fails? How do I detect it? How do I recover without corrupting data?", 1.65, 6.25, 10.05, 0.55)

# 5
slide = add_slide("A practical 45-minute interview cadence", "Time-box detail so the architecture is complete before you dive deep.", "Framework")
phases = [
    ("0–7 min", "Clarify", "Users, outputs, SLAs, volume, retention", TEAL),
    ("7–12", "Estimate", "Events/sec, bytes/day, peak factor, growth", BLUE),
    ("12–23", "High level", "Sources → ingest → process → store → serve", PURPLE),
    ("23–33", "Deep dive", "Model, partitions, state, delivery semantics", ORANGE),
    ("33–40", "Reliability", "Quality, replay, backfill, schema, DR", GREEN),
    ("40–45", "Trade-offs", "Bottlenecks, cost, 10× scale, summary", RED),
]
for i, (time, t, b, c) in enumerate(phases):
    x = 0.75+i*2.06
    add_rect(slide, x, 2.0, 1.72, 2.8, WHITE, True, LIGHT, 0.8)
    add_rect(slide, x, 2.0, 1.72, 0.62, c, True)
    add_text(slide, time, x, 2.2, 1.72, 0.2, 11, WHITE, True, align=PP_ALIGN.CENTER)
    add_text(slide, t, x+0.12, 2.88, 1.48, 0.3, 14, NAVY, True, align=PP_ALIGN.CENTER)
    add_text(slide, b, x+0.13, 3.45, 1.46, 0.9, 10, DARK, align=PP_ALIGN.CENTER)
add_callout(slide, "Checkpoint at minute 20: the interviewer should already see an end-to-end data flow and understand why it meets the SLAs.", 1.4, 5.55, 10.5, 0.65)

# 6
slide = add_slide("Step 1 — Requirements canvas", "Do not draw architecture until these questions are sufficiently answered.", "Requirements")
qs = [
    ("WHO", "Who consumes it? Analysts, applications, ML, partners?", TEAL),
    ("WHAT", "Raw events, metrics, dimensions, features, alerts?", BLUE),
    ("HOW", "SQL, BI, API, file export, reverse ETL, feature store?", PURPLE),
    ("WHEN", "Real-time, <2 min, hourly, daily? Event vs. processing time?", ORANGE),
    ("HOW MUCH", "Average/peak throughput, event size, growth, cardinality?", GREEN),
    ("HOW LONG", "Retention, replay window, legal deletion, RPO/RTO?", RED),
]
for i, (t,b,c) in enumerate(qs):
    card(slide, 0.7+(i%3)*4.2, 1.7+(i//3)*2.25, 3.8, 1.72, t, b, c, title_size=15, body_size=11)
add_text(slide, "Write assumptions explicitly. Example: “I’ll assume 3× peak over average and 30-day Kafka retention; we can revise if needed.”", 0.85, 6.32, 11.7, 0.4, 11, NAVY, True, align=PP_ALIGN.CENTER)

# 7
slide = add_slide("Functional vs. non-functional requirements", "Functional defines outcomes; non-functional constraints shape every component choice.", "Requirements")
rows = [
    ["Area", "Questions to ask", "Example acceptance criterion"],
    ["Consumers & outputs", "Who reads what, through which interface?", "Restaurant KPI dashboard + executive daily report"],
    ["Freshness / latency", "End-to-end SLA or per-stage? p95 or average?", "p95 event-to-dashboard < 120 seconds"],
    ["Correctness", "Exactly-once outcome? Late data? Revisions?", "Final daily totals reconcile to source within 0.1%"],
    ["Availability", "Can consumers tolerate stale data or downtime?", "99.9% serving availability; stale badge after 5 min"],
    ["Retention & replay", "What must be retained, deleted, or reproduced?", "2 years analytics; 14 days event-bus replay"],
    ["Security & governance", "PII, residency, access, audit, deletion?", "Encrypt; RBAC; delete subject data within 30 days"],
    ["Cost & operability", "Budget, team skill, managed vs. self-hosted?", "Prefer managed services; cap steady-state compute"],
]
add_table(slide, rows, 0.65, 1.67, 12.05, 4.95, [2.2, 5.0, 4.85], font_size=9.7)
add_text(slide, "Tip: convert vague words (“real time”, “large”, “reliable”) into measurable SLOs.", 0.75, 6.72, 11.8, 0.25, 10, TEAL_DARK, True, align=PP_ALIGN.CENTER)

# 8
slide = add_slide("Back-of-the-envelope math: e-commerce events", "Show the arithmetic, state assumptions, and round conservatively.", "Requirements")
add_rect(slide, 0.7, 1.72, 7.6, 4.85, WHITE, True, LIGHT, 0.8)
math_lines = [
    ("Events/day", "5M DAU × 2 sessions/day × 30 events/session = 300M"),
    ("Average rate", "300M ÷ 86,400 ≈ 3,472 events/sec"),
    ("Peak rate", "Assume 4× peak ≈ 13,900 events/sec"),
    ("Raw volume", "300M × 700 bytes ≈ 210 GB/day ≈ 6.3 TB/month"),
    ("12-month raw", "210 GB × 365 ≈ 76.7 TB before replication"),
    ("Compressed lake", "At 2–5× compression ≈ 15–38 TB, plus table metadata"),
]
add_rich_lines(slide, math_lines, 1.05, 2.08, 6.9, 3.95, 15, DARK, True, TEAL, 11)
card(slide, 8.65, 1.72, 3.95, 1.35, "Capacity consequence", "Design partitions and consumers for peak—not the daily average.", ORANGE, title_size=15, body_size=11)
card(slide, 8.65, 3.28, 3.95, 1.35, "Compute consequence", "Single-node memory is unsafe; use distributed processing and incremental reads.", BLUE, title_size=15, body_size=11)
card(slide, 8.65, 4.84, 3.95, 1.35, "Cost consequence", "Compression, retention tiers, compaction, and scan pruning are first-class design decisions.", GREEN, title_size=15, body_size=11)

# 9
slide = add_slide("Translate estimates into design constraints", "Numbers matter only when they change a decision.", "Requirements")
rows = [
    ["Estimate", "Design implication", "What to validate next"],
    ["~14K peak events/sec", "Partition event bus for parallelism + headroom", "Per-partition sustainable rate; key skew"],
    ["~210 GB raw/day", "Object storage + incremental processing", "Compression ratio; small-file rate"],
    ["High key cardinality", "Avoid hot partitions; choose stable distribution key", "Top keys and concentration at peak"],
    ["<2-minute dashboard SLA", "Continuous processing + low-latency serving store", "State size; sink write latency"],
    ["12–24 month retention", "Lifecycle older data to colder tiers; preserve replay metadata", "Compliance deletion and restore time"],
    ["10× future growth", "Decouple stages, autoscale consumers, pre-plan quotas", "Service limits and cost curve"],
]
add_table(slide, rows, 0.7, 1.75, 11.95, 4.8, [2.65, 4.55, 4.75], font_size=10)
add_callout(slide, "Useful formulas: throughput = events ÷ seconds • storage = events × bytes × retention × replication ÷ compression", 1.0, 6.45, 11.3, 0.55)

# 10
slide = add_slide("Step 2 — Choose batch or streaming from the SLA", "Prefer the simplest processing model that satisfies the business requirement.", "Pipeline Design")
# decision tree
node(slide, 0.65, 2.15, 2.2, 0.95, "Freshness needed?", "Start with end-to-end SLA", WHITE, TEAL)
arrow(slide, 2.88, 2.62, 4.05, 1.98, TEAL)
arrow(slide, 2.88, 2.62, 4.05, 3.7, TEAL)
add_text(slide, "minutes", 3.18, 1.95, 0.8, 0.2, 9, MID, True)
add_text(slide, "hours/days", 3.18, 3.48, 0.8, 0.2, 9, MID, True)
node(slide, 4.1, 1.45, 2.3, 1.05, "Streaming", "Kafka + Flink / Spark", RGBColor(235, 248, 255), BLUE)
node(slide, 4.1, 3.25, 2.3, 1.05, "Batch", "Scheduler + Spark / SQL", RGBColor(238, 251, 247), GREEN)
arrow(slide, 6.45, 1.98, 7.55, 1.98, BLUE)
arrow(slide, 6.45, 3.78, 7.55, 3.78, GREEN)
node(slide, 7.6, 1.45, 2.35, 1.05, "Stateful?", "Windows, joins, dedupe", WHITE, PURPLE)
node(slide, 7.6, 3.25, 2.35, 1.05, "Incremental?", "Process only changed data", WHITE, PURPLE)
arrow(slide, 10.0, 1.98, 11.0, 1.98, PURPLE)
arrow(slide, 10.0, 3.78, 11.0, 3.78, PURPLE)
node(slide, 11.05, 1.45, 1.65, 1.05, "Plan state", "TTL + checkpoint", RGBColor(249, 243, 255), PURPLE, 11)
node(slide, 11.05, 3.25, 1.65, 1.05, "Plan replay", "Partitions + ledger", RGBColor(249, 243, 255), PURPLE, 11)
add_callout(slide, "Streaming is not “better batch.” It introduces event-time semantics, out-of-order data, state, checkpoints, replay, and more operational load.", 1.1, 5.45, 11.1, 0.75, RGBColor(255, 246, 234), ORANGE, 12)

# 11
slide = add_slide("Batch vs. streaming: explicit trade-offs", "Hybrid systems are common because different consumers have different SLAs.", "Pipeline Design")
rows = [
    ["Dimension", "Batch", "Streaming"],
    ["Best fit", "Hourly/daily analytics; historical recompute", "Alerts, operations, online features, live KPIs"],
    ["Latency", "Minutes to days", "Milliseconds to minutes"],
    ["Cost profile", "Elastic scheduled compute; often lower", "Always-on compute + event infrastructure"],
    ["Complexity", "Retries and partitions are easier to reason about", "Event time, watermarks, state, ordering, replay"],
    ["Correctness", "Closed data windows simplify finality", "Late data can revise prior results"],
    ["Recovery", "Rerun partitions / replace ranges", "Restore checkpoint or replay offsets"],
    ["Serving", "Warehouse/lakehouse tables", "Key-value/OLAP serving + durable lakehouse"],
]
add_table(slide, rows, 0.7, 1.72, 11.95, 4.85, [2.3, 4.8, 4.85], font_size=10)
add_callout(slide, "Decision rule: if the SLA is daily, start with batch. Add streaming only for a named use case that cannot tolerate batch latency.", 1.0, 6.47, 11.3, 0.55)

# 12
slide = add_slide("Lambda, Kappa, and Lakehouse patterns", "Architecture style describes how processing paths and durable truth are organized.", "Pipeline Design")
patterns = [
    ("Lambda", "Batch truth + speed path\n\n+ Low latency and accurate recompute\n− Duplicate logic and reconciliation", BLUE),
    ("Kappa", "One streaming path; replay log\n\n+ One processing model\n− Long replays and state complexity", PURPLE),
    ("Lakehouse-centric", "Durable object store + ACID tables\n\n+ Unified batch/stream data plane\n− Table maintenance and engine tuning", TEAL),
]
for i,(t,b,c) in enumerate(patterns):
    x=0.7+i*4.2
    add_rect(slide,x,1.78,3.75,3.8,WHITE,True,LIGHT,0.8)
    add_rect(slide,x,1.78,3.75,0.65,c,True)
    add_text(slide,t,x,1.98,3.75,0.24,15,WHITE,True,align=PP_ALIGN.CENTER)
    # mini diagram
    if i==0:
        node(slide,x+0.25,2.75,0.9,0.6,"Source","",WHITE,c,10); node(slide,x+1.45,2.58,0.95,0.55,"Speed","",WHITE,c,10); node(slide,x+1.45,3.32,0.95,0.55,"Batch","",WHITE,c,10); node(slide,x+2.72,2.95,0.78,0.6,"Serve","",WHITE,c,10)
        arrow(slide,x+1.16,3.05,x+1.4,2.85,c,1); arrow(slide,x+1.16,3.05,x+1.4,3.58,c,1); arrow(slide,x+2.42,2.85,x+2.68,3.18,c,1); arrow(slide,x+2.42,3.58,x+2.68,3.18,c,1)
    elif i==1:
        node(slide,x+0.25,2.92,0.9,0.6,"Source","",WHITE,c,10); node(slide,x+1.44,2.92,0.9,0.6,"Log","",WHITE,c,10); node(slide,x+2.63,2.92,0.9,0.6,"Stream","",WHITE,c,10)
        arrow(slide,x+1.16,3.22,x+1.4,3.22,c,1); arrow(slide,x+2.36,3.22,x+2.59,3.22,c,1)
    else:
        node(slide,x+0.22,2.92,0.8,0.6,"Ingest","",WHITE,c,9); node(slide,x+1.25,2.92,1.05,0.6,"ACID lake","",WHITE,c,9); node(slide,x+2.55,2.92,0.95,0.6,"Engines","",WHITE,c,9)
        arrow(slide,x+1.03,3.22,x+1.21,3.22,c,1); arrow(slide,x+2.32,3.22,x+2.51,3.22,c,1)
    add_text(slide,b,x+0.3,4.0,3.15,1.25,11,DARK,align=PP_ALIGN.CENTER)
add_callout(slide, "Choose by recovery model and team ownership—not by trend. Ask where durable truth lives and how every path is replayed.", 1.25, 6.15, 10.8, 0.62)

# 13
slide = add_slide("Reference architecture: explain left to right", "Separate concerns so each stage can scale, fail, and recover independently.", "Pipeline Design")
columns = [
    ("SOURCES", ["Apps/events", "DB CDC", "SaaS/files"], TEAL),
    ("INGEST", ["Kafka / Kinesis", "Object landing", "Schema registry"], BLUE),
    ("PROCESS", ["Flink / Spark", "Batch SQL", "Orchestrator"], PURPLE),
    ("STORE", ["Bronze/Silver", "Delta / Iceberg", "Catalog"], ORANGE),
    ("SERVE", ["Warehouse/OLAP", "Redis / API", "BI / ML"], GREEN),
]
for i,(head,vals,c) in enumerate(columns):
    x=0.48+i*2.56
    add_rect(slide,x,1.72,2.22,4.45,WHITE,True,LIGHT,0.8)
    add_rect(slide,x,1.72,2.22,0.62,c,True)
    add_text(slide,head,x,1.94,2.22,0.18,11,WHITE,True,align=PP_ALIGN.CENTER)
    for j,v in enumerate(vals):
        node(slide,x+0.25,2.7+j*0.93,1.72,0.61,v,"",RGBColor(249,251,254),c,10)
    if i<4:
        arrow(slide,x+2.23,3.88,x+2.5,3.88,MID,1.5)
add_text(slide, "Cross-cutting: security • metadata/lineage • quality • observability • cost controls • CI/CD", 1.1, 6.4, 11.1, 0.35, 11, NAVY, True, align=PP_ALIGN.CENTER)

# Senior deep dive — event backbone
slide = add_slide("Design the event backbone: identity, ordering, and partitions", "Partitioning is a correctness and recovery decision—not only a throughput setting.", "Pipeline Design")
backbone = [
    ("EVENT IDENTITY", "Stable event_id plus source transaction/row identity. Consumers assume duplicates and deduplicate at the intended grain.", TEAL),
    ("ORDERING SCOPE", "Avoid global order. Preserve order only where required: order, account, tenant + ledger, or another business aggregate.", BLUE),
    ("PARTITION KEY", "Choose a key that preserves local order and distributes peak load. Detect hot tenants/keys and sub-shard only when semantics allow.", PURPLE),
    ("CAPACITY + REPLAY", "Size from measured peak bytes/records, consumer rate, backlog-drain target, retention, growth, and service quotas.", ORANGE),
]
for i,(t,b,c) in enumerate(backbone):
    card(slide,0.68+(i%2)*6.12,1.68+(i//2)*2.13,5.72,1.65,t,b,c,i+1,13,10.2)
add_callout(slide,"Versioned envelope: event_id • tenant • aggregate_id • event type • occurred/produced time • source offset • schema version • trace ID",0.95,6.15,11.45,0.68)

# Senior deep dive — serving choices
slide = add_slide("Choose the serving layer from the access pattern", "Shared governed truth can feed several stores; each serving copy needs refresh, correction, and fallback behavior.", "Pipeline Design")
rows = [
    ["Consumer", "Query pattern / target", "Typical fit", "Required controls"],
    ["BI / finance", "Scans, joins, aggregates; seconds", "Warehouse, lakehouse SQL, OLAP", "Semantic metrics, concurrency, finality"],
    ["Operational dashboard", "Recent filters/aggregates; sub-second to seconds", "Real-time OLAP, materialized views", "Freshness, update/retraction, stale label"],
    ["Application API", "Point/range lookups; milliseconds", "Key-value, relational, search", "Consistency, idempotent refresh, fallback"],
    ["Machine learning", "Offline scans + online point features", "Lakehouse + feature store", "Point-in-time joins, online/offline parity"],
    ["ERP copilot", "Authorized SQL + document retrieval; interactive", "Semantic layer + vector/search + AI gateway", "Tenant/ACL filters, citations, cache isolation"],
]
add_table(slide,rows,0.58,1.68,12.18,4.72,[2.2,3.15,3.2,3.63],font_size=9.25)
add_callout(slide,"Avoid a store per use case by default. Add a serving copy only when its latency, concurrency, or access pattern justifies synchronization cost.",1.0,6.42,11.3,0.58)

# 14
slide = add_slide("Step 3 — Medallion data progression", "Each layer has a distinct contract, failure policy, and consumer boundary.", "Data Modeling")
layers = [
    ("BRONZE", "Immutable landing", "Raw payload + ingest metadata\nPreserve source fidelity\nQuarantine malformed records", BRONZE),
    ("SILVER", "Trusted entities", "Parse, cast, deduplicate\nApply keys and conformance\nFacts + dimensions", SILVER),
    ("GOLD", "Business products", "Stable metrics and aggregates\nConsumer-specific models\nPerformance + semantic contract", GOLD),
]
for i,(name,sub,body,c) in enumerate(layers):
    x=0.8+i*4.18
    add_rect(slide,x,1.82,3.55,3.9,WHITE,True,c,1.5)
    add_rect(slide,x,1.82,3.55,0.72,c,True)
    add_text(slide,name,x,2.05,3.55,0.22,16,WHITE if i!=1 else NAVY,True,align=PP_ALIGN.CENTER)
    add_text(slide,sub,x+0.25,2.83,3.05,0.32,15,NAVY,True,align=PP_ALIGN.CENTER)
    add_text(slide,body,x+0.35,3.5,2.85,1.35,12,DARK,align=PP_ALIGN.CENTER)
    add_chip(slide,["Permissive", "Enforced", "Versioned"][i],x+1.15,5.08,1.25,c,WHITE if i!=1 else NAVY)
    if i<2: arrow(slide,x+3.58,3.77,x+4.08,3.77,c,2)
add_callout(slide, "Bronze is recoverability. Silver is reusable truth. Gold is a documented data product—not simply “the final table.”", 1.15, 6.2, 11.0, 0.62)

# 15
slide = add_slide("Design facts and dimensions from the grain", "State the grain before listing columns: one row represents exactly what?", "Data Modeling")
# star schema visual
node(slide, 5.15, 2.6, 3.05, 1.35, "fact_order_event", "grain: one order lifecycle event\nmeasures: amount, duration", RGBColor(238,248,255), BLUE, 16)
dims = [
    (0.75,1.72,"dim_customer","customer_key • segment"),
    (0.75,4.65,"dim_restaurant","restaurant_key • cuisine"),
    (9.55,1.72,"dim_date","date_key • week • month"),
    (9.55,4.65,"dim_location","location_key • city • region"),
]
for x,y,t,s in dims:
    node(slide,x,y,2.85,0.95,t,s,WHITE,PURPLE,12)
    if x<5: arrow(slide,x+2.88,y+0.48,5.1,3.28,PURPLE,1.5)
    else: arrow(slide,x,y+0.48,8.25,3.28,PURPLE,1.5)
add_callout(slide, "Design sequence: business process → grain → dimensions → facts/measures → keys → late-arriving behavior → SCD strategy.", 1.3, 6.2, 10.7, 0.62)

# 16
slide = add_slide("Star, snowflake, or one big table?", "Choose by consumer behavior, governance needs, update patterns, and engine performance.", "Data Modeling")
rows = [
    ["Model", "Advantages", "Costs / risks", "Use when"],
    ["Star schema", "Clear grain; reusable dimensions; governed metrics", "Joins; surrogate-key and SCD management", "BI, semantic layers, many related analyses"],
    ["Snowflake", "Less duplication; normalized hierarchies", "More joins; harder for users", "Complex shared hierarchies with strong governance"],
    ["One big table", "Simple queries; fewer runtime joins", "Duplication, wide scans, update anomalies", "Stable narrow use case; query engine benefits"],
    ["Data Vault", "Auditability; change tolerance; source traceability", "Model complexity; business marts still needed", "Large integration programs and regulated history"],
]
add_table(slide, rows, 0.65, 1.78, 12.05, 4.3, [2.0, 3.35, 3.35, 3.35], font_size=9.7)
add_callout(slide, "Interview answer: propose a default, then name the condition that would make you switch. Example: star for governed BI; OBT only for a proven hot query path.", 0.95, 6.2, 11.45, 0.7)

# 17
slide = add_slide("Slowly Changing Dimensions (SCD)", "Select history behavior per attribute—not necessarily once for the entire dimension.", "Data Modeling")
rows = [
    ["Type", "Behavior", "Example", "Trade-off"],
    ["SCD 1", "Overwrite current value", "Correct misspelled customer name", "Simple; no prior history"],
    ["SCD 2", "Insert new version with effective range", "Track customer loyalty tier over time", "Full history; joins and late updates are harder"],
    ["SCD 3", "Keep limited prior value in extra column", "Current and previous sales territory", "Simple comparison; only limited history"],
]
add_table(slide, rows, 0.75, 1.78, 11.85, 2.55, [1.7, 3.3, 3.6, 3.25], font_size=10.5)
add_text(slide, "SCD 2 record shape", 0.85, 4.72, 2.2, 0.3, 14, NAVY, True)
scd = [
    ["customer_key", "customer_id", "tier", "effective_from", "effective_to", "is_current"],
    ["101", "C55", "SILVER", "2026-01-01", "2026-09-23", "false"],
    ["145", "C55", "GOLD", "2026-09-24", "NULL", "true"],
]
add_table(slide, scd, 0.8, 5.05, 11.7, 1.25, [1.7,1.7,1.3,2.1,2.1,1.3], header_fill=PURPLE, font_size=9.5)
add_text(slide, "Protect against overlapping effective ranges; define how late-arriving facts choose the correct dimension version.", 1.0, 6.52, 11.3, 0.28, 10, TEAL_DARK, True, align=PP_ALIGN.CENTER)

# 18
slide = add_slide("Step 4 — File format decision matrix", "Serialization format and table format solve different problems.", "Storage")
rows = [
    ["Format", "Layout", "Strength", "Best fit", "Watch-outs"],
    ["CSV / JSON", "Text / row-like", "Human-readable; universal", "Landing, interchange, debugging", "Large; weak typing; slow analytics"],
    ["Avro", "Row-oriented binary", "Fast record serialization; schema support", "Event payloads, write-heavy exchange", "Not optimal for analytical scans"],
    ["Parquet", "Columnar", "Column pruning, encoding, compression", "Lakehouse analytics and large scans", "Small files; update semantics need table layer"],
    ["ORC", "Columnar", "Strong compression and predicate filtering", "Hive-centric analytics", "Ecosystem preference may vary"],
    ["Delta / Iceberg", "Table metadata over data files", "ACID, snapshots, schema/partition evolution", "Managed analytical tables", "Metadata/compaction/version compatibility"],
]
add_table(slide, rows, 0.6, 1.72, 12.15, 4.75, [1.7,1.65,3.15,3.0,2.65], font_size=9.3)
add_callout(slide, "Common pairing: Avro/Protobuf on the event bus → Parquet data files inside Delta Lake or Iceberg tables.", 1.35, 6.42, 10.6, 0.57)

# 19
slide = add_slide("Storage layout: optimize for access patterns", "Partitioning is a pruning strategy, not a default checkbox.", "Storage")
layout_cards = [
    ("Partitioning", "Use low/medium-cardinality columns frequently used in filters (often date). Avoid millions of tiny partitions.", TEAL),
    ("Clustering / sorting", "Co-locate frequently filtered keys without rigid directory explosion; benefits depend on engine and workload.", BLUE),
    ("Compaction", "Combine small files to improve listing, planning, and read efficiency; schedule around ingestion patterns.", PURPLE),
    ("Metadata maintenance", "Expire snapshots safely, vacuum only beyond replay/time-travel needs, and monitor manifest/log growth.", ORANGE),
]
for i,(t,b,c) in enumerate(layout_cards):
    card(slide,0.7+(i%2)*6.15,1.72+(i//2)*2.15,5.75,1.65,t,b,c,title_size=15,body_size=10.5)
add_callout(slide, "Explain the read path: filter → partition pruning → file/data skipping → column pruning → decompression. Then show how layout reduces bytes scanned.", 1.1, 6.15, 11.1, 0.68)

# 20
slide = add_slide("Step 5 — Data quality by layer", "Quality checks should have owners, thresholds, actions, and measured outcomes.", "Quality & Observability")
checks = [
    ("BRONZE", "Can we ingest and replay?", ["Parse success rate", "Required envelope fields", "Source count / checksum", "Quarantine malformed data"], BRONZE),
    ("SILVER", "Is it trustworthy?", ["Uniqueness and dedupe", "Type/domain validity", "Referential integrity", "Freshness and completeness"], SILVER),
    ("GOLD", "Is it fit for business?", ["Metric reconciliation", "Business invariants", "SLA and anomaly checks", "Consumer contract tests"], GOLD),
]
for i,(name,q,vals,c) in enumerate(checks):
    x=0.7+i*4.2
    add_rect(slide,x,1.75,3.8,4.45,WHITE,True,c,1.3)
    add_rect(slide,x,1.75,3.8,0.64,c,True)
    add_text(slide,name,x,1.96,3.8,0.2,14,WHITE if i!=1 else NAVY,True,align=PP_ALIGN.CENTER)
    add_text(slide,q,x+0.25,2.7,3.3,0.55,13,NAVY,True,align=PP_ALIGN.CENTER)
    add_rich_lines(slide,vals,x+0.42,3.55,3.05,1.85,11,DARK,True,c,8)
    add_chip(slide,["Alert + retain", "Block/quarantine", "Hold publication"][i],x+1.03,5.62,1.75,c,WHITE if i!=1 else NAVY)
add_text(slide, "Dimensions: completeness • accuracy • consistency • freshness • uniqueness • validity", 1.0, 6.47, 11.3, 0.27, 10.5, TEAL_DARK, True, align=PP_ALIGN.CENTER)

# 21
slide = add_slide("Data contracts shift failures left", "A contract aligns producers and consumers before incompatible data reaches production.", "Quality & Observability")
left = [
    ("Schema", "Field names, types, nullability, compatibility mode"),
    ("Semantics", "Meaning, units, event lifecycle, allowed values"),
    ("SLOs", "Freshness, completeness, availability, support hours"),
    ("Ownership", "Producer, consumer, escalation, change approval"),
]
for i,(t,b) in enumerate(left):
    card(slide,0.7,1.68+i*1.15,5.5,0.95,t,b,[TEAL,BLUE,PURPLE,ORANGE][i],title_size=13,body_size=9.5)
# contract flow
add_text(slide, "Contract enforcement path", 6.75, 1.75, 5.6, 0.32, 15, NAVY, True, align=PP_ALIGN.CENTER)
node(slide,7.0,2.42,1.35,0.8,"Producer","CI validation",WHITE,TEAL,11)
node(slide,9.0,2.42,1.35,0.8,"Registry","compatibility",WHITE,BLUE,11)
node(slide,11.0,2.42,1.35,0.8,"Consumer","contract test",WHITE,PURPLE,11)
arrow(slide,8.38,2.82,8.95,2.82,TEAL,1.5); arrow(slide,10.38,2.82,10.95,2.82,BLUE,1.5)
add_callout(slide, "Breaking change? Create a new version, dual-publish during migration, measure consumer adoption, then retire the old contract.", 6.75, 3.75, 5.7, 1.0, RGBColor(255,246,234), ORANGE, 11)
add_callout(slide, "A schema registry validates structure; a full data contract also captures semantics, SLOs, ownership, and change policy.", 6.75, 5.15, 5.7, 0.9, RGBColor(235,248,255), BLUE, 11)

# 22
slide = add_slide("Observability: detect, explain, and recover", "Monitor the data product, the pipeline, and the infrastructure together.", "Quality & Observability")
obs = [
    ("DATA", ["Freshness lag", "Row/event counts", "Null/duplicate rate", "Distribution drift"], TEAL),
    ("PIPELINE", ["DAG / batch duration", "Consumer lag", "Watermark delay", "Retries / DLQ volume"], BLUE),
    ("PLATFORM", ["CPU / memory / disk", "Shuffle and spill", "Checkpoint latency", "Quota / throttling"], PURPLE),
    ("BUSINESS", ["Orders vs. source", "Revenue anomalies", "Dashboard usage", "SLO error budget"], ORANGE),
]
for i,(t,vals,c) in enumerate(obs):
    x=0.65+i*3.15
    add_rect(slide,x,1.73,2.82,3.95,WHITE,True,LIGHT,0.8)
    add_rect(slide,x,1.73,2.82,0.62,c,True)
    add_text(slide,t,x,1.94,2.82,0.2,12,WHITE,True,align=PP_ALIGN.CENTER)
    add_rich_lines(slide,vals,x+0.28,2.75,2.3,2.1,11,DARK,True,c,9)
    add_chip(slide,"owner + runbook",x+0.75,5.03,1.32,c,WHITE)
add_callout(slide, "Alert on user impact and actionable symptoms. Every page should link to lineage, recent deployments, affected partitions, and a recovery runbook.", 1.0, 6.1, 11.3, 0.72)

# 23
slide = add_slide("Step 6 — Idempotency is an end-to-end property", "Rerunning the same logical input should produce the same observable outcome.", "Operations")
principles = [
    ("Stable identity", "Define event_id or a compound business key. Validate uniqueness at the intended grain.", TEAL),
    ("Deterministic transform", "Avoid nondeterministic timestamps/random values unless derived from source or controlled.", BLUE),
    ("Atomic write", "Use MERGE, partition replacement, or transactional commit—not blind append.", PURPLE),
    ("Progress tracking", "Persist source offsets, file IDs, batch IDs, code version, and target commit together.", ORANGE),
    ("Safe retry", "Retry transient errors; quarantine poison data; never advance progress before commit.", GREEN),
    ("Reconciliation", "Compare source, accepted, rejected, and target counts; expose mismatches.", RED),
]
for i,(t,b,c) in enumerate(principles):
    card(slide,0.7+(i%3)*4.2,1.68+(i//3)*2.2,3.8,1.68,t,b,c,i+1,14,10.5)
add_callout(slide, "Delivery may be at-least-once while the resulting table is effectively exactly-once through dedupe + transactional upsert.", 1.1, 6.15, 11.1, 0.65)

# 24
slide = add_slide("Idempotent batch upsert with Delta MERGE", "Deduplicate the source first; MERGE behavior is ambiguous if multiple source rows match one target row.", "Delta Lake + Spark", bg=NAVY)
code = '''from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql.window import Window

incoming = spark.read.json(batch_path)
key = ["order_id", "event_timestamp"]
w = Window.partitionBy(*key).orderBy(F.col("updated_at").desc())
source = (incoming
    .withColumn("_rn", F.row_number().over(w))
    .filter("_rn = 1").drop("_rn"))

target = DeltaTable.forPath(spark, silver_path)
(target.alias("t").merge(
    source.alias("s"),
    "t.order_id=s.order_id AND t.event_timestamp=s.event_timestamp")
 .whenMatchedUpdateAll(condition="s.updated_at >= t.updated_at")
 .whenNotMatchedInsertAll()
 .execute())'''
add_code(slide,code,0.68,1.62,8.0,4.95,"PYSPARK",10.1)
add_text(slide, "Why this is safe", 9.05, 1.75, 3.55, 0.32, 16, WHITE, True)
add_rich_lines(slide,[
    ("Stable key: ","order + event timestamp identifies the grain."),
    ("Source dedupe: ","one winning row per merge key."),
    ("Monotonic update: ","older arrivals cannot overwrite newer state."),
    ("Atomic commit: ","readers see the old or new snapshot, not a partial write."),
],9.05,2.35,3.55,2.8,11.5,LIGHT,True,TEAL,11)
add_callout(slide,"Still define delete behavior, null-safe matching, concurrency policy, and reconciliation metrics.",8.95,5.45,3.72,0.9,RGBColor(35,58,84),ORANGE,10.5)

# 25
slide = add_slide("Backfills with atomic partition replacement", "Recompute bounded slices using the same transformation code as the normal path.", "Delta Lake + Spark", bg=NAVY)
code = '''start, end = "2026-09-01", "2026-09-15"
predicate = f"event_date >= '{start}' AND event_date <= '{end}'"

backfill = (spark.table("bronze_events")
    .where(predicate)
    .transform(build_silver_events))

(backfill.write.format("delta")
    .mode("overwrite")
    .option("replaceWhere", predicate)
    .save(silver_path))'''
add_code(slide,code,0.7,1.72,6.5,3.8,"PYSPARK",11)
add_text(slide,"Backfill runbook",7.6,1.75,4.7,0.35,16,WHITE,True)
add_rich_lines(slide,[
    ("1. Scope", " immutable input range and expected outputs."),
    ("2. Isolate", " run ID, code version, compute, and temporary validation."),
    ("3. Validate", " counts, checksums, business totals, and sample diffs."),
    ("4. Publish", " atomically replace only the intended predicate."),
    ("5. Observe", " downstream refresh, lineage, and cost; record audit."),
],7.58,2.3,4.8,3.4,11,LIGHT,True,TEAL,9)
add_callout(slide,"Guardrail: verify every output row satisfies replaceWhere; otherwise fail rather than silently writing outside the requested range.",1.4,5.95,10.6,0.68,RGBColor(35,58,84),ORANGE,10.5)

# 26
slide = add_slide("Streaming idempotency: checkpoint + deterministic MERGE", "Use micro-batch IDs as audit signals; correctness comes from deterministic upsert and committed progress.", "Delta Lake + Spark", bg=NAVY)
code = '''def upsert_batch(df, batch_id):
    clean = dedupe_by_event_id(df)
    target = DeltaTable.forPath(spark, silver_path)
    (target.alias("t").merge(clean.alias("s"), "t.event_id=s.event_id")
      .whenMatchedUpdateAll(condition="s.updated_at >= t.updated_at")
      .whenNotMatchedInsertAll()
      .execute())
    # Optional: record batch_id + target version in an audit ledger.

query = (spark.readStream.format("kafka")
    .options(**kafka_options).load()
    .transform(parse_and_validate)
    .writeStream.foreachBatch(upsert_batch)
    .option("checkpointLocation", checkpoint_path)
    .start())'''
add_code(slide,code,0.65,1.62,7.6,5.1,"PYSPARK",10)
add_text(slide,"Important correction",8.65,1.75,3.8,0.35,16,ORANGE,True)
add_text(slide,"The supplied sample chains .option(\"txnAppId\", …) onto a Delta MERGE builder. That is not the normal DeltaMergeBuilder API.",8.65,2.3,3.85,1.15,11.5,LIGHT)
add_rich_lines(slide,[
    ("For MERGE: ","checkpoint source progress and make the merge key/logic idempotent."),
    ("For direct Delta writes: ","transaction app/version writer options may be used where the runtime supports them."),
    ("For multiple sinks: ","use an audit ledger/outbox pattern; no checkpoint makes two systems one transaction."),
],8.65,3.7,3.85,2.3,10.5,LIGHT,True,TEAL,8)

# 27
slide = add_slide("Schema evolution: permissive edge, strict core", "Treat schema change as a governed migration—not an accidental side effect.", "Delta Lake + Spark")
stages = [
    ("BRONZE", "Absorb", "Keep raw payload, schema ID, ingest time, rescued data. Alert on drift.", BRONZE),
    ("SILVER", "Validate", "Explicit expected schema, casts, defaults, quarantine, compatibility tests.", SILVER),
    ("GOLD", "Contract", "Stable names/types/semantics. Version views or products for breaking changes.", GOLD),
]
for i,(t,v,b,c) in enumerate(stages):
    x=0.7+i*4.2
    add_rect(slide,x,1.73,3.8,3.55,WHITE,True,c,1.3)
    add_rect(slide,x,1.73,3.8,0.62,c,True)
    add_text(slide,t,x,1.94,3.8,0.2,14,WHITE if i!=1 else NAVY,True,align=PP_ALIGN.CENTER)
    add_text(slide,v,x,2.65,3.8,0.35,19,NAVY,True,align=PP_ALIGN.CENTER)
    add_text(slide,b,x+0.35,3.35,3.1,1.05,11,DARK,align=PP_ALIGN.CENTER)
    add_chip(slide,["do not lose data","do not surprise users","do not break consumers"][i],x+0.77,4.68,2.25,c,WHITE if i!=1 else NAVY)
    if i<2: arrow(slide,x+3.82,3.5,x+4.1,3.5,c,1.5)
add_text(slide,"Compatibility policy",0.85,5.72,2.25,0.3,14,NAVY,True)
add_text(slide,"Add nullable field → usually backward-compatible  |  Rename/drop/type change → version + migrate  |  Semantic change → new metric/product",0.85,6.12,11.65,0.45,11,DARK,align=PP_ALIGN.CENTER)

# 28
slide = add_slide("Controlled schema evolution in Spark + Delta", "Enable evolution narrowly, validate overlap, and never let convenience replace a migration policy.", "Delta Lake + Spark", bg=NAVY)
code1='''# Bronze: capture unexpected fields
bronze = (spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", schema_path)
  .option("rescuedDataColumn", "_rescued_data")
  .load(landing_path))'''
code2='''# Additive write after explicit validation
assert_required_columns(incoming, required)
assert_compatible_types(incoming.schema, target_schema)

(incoming.write.format("delta").mode("append")
  .option("mergeSchema", "true")
  .save(silver_path))'''
add_code(slide,code1,0.7,1.65,5.85,3.55,"BRONZE",10.5)
add_code(slide,code2,6.78,1.65,5.85,3.55,"SILVER",10.5)
add_callout(slide,"Avoid global auto-merge as the default: overly permissive evolution can accept columns with little or no meaningful overlap and push surprises downstream.",0.85,5.55,11.65,0.75,RGBColor(35,58,84),ORANGE,11)
add_text(slide,"Production gate: contract compatibility test → owner approval → migration → consumer validation → rollout → drift monitoring",1.0,6.52,11.3,0.28,10,LIGHT,True,align=PP_ALIGN.CENTER)

# 29
slide = add_slide("Resilience, disaster recovery, and 10× scale", "Name the failure domain, detection signal, recovery action, and data-loss boundary.", "Operations")
rows = [
    ["Failure / pressure", "Design response", "Recovery proof"],
    ["Consumer crash", "Checkpoint offsets and state in durable storage", "Restart and compare no-gap/no-duplicate outcomes"],
    ["Poison record", "Quarantine/DLQ with raw payload and reason", "Replay corrected records through the same contract"],
    ["Region outage", "Replicated object data/catalog; documented failover", "Exercise restore; measure actual RPO and RTO"],
    ["10× traffic", "Increase partitions; autoscale consumers; eliminate hot keys", "Load test peak + headroom; inspect lag and throttling"],
    ["Bad deployment", "Versioned jobs/tables; canary; snapshot rollback", "Rollback while preserving committed source progress"],
    ["Corrupt output", "Time travel/snapshots + bounded rebuild from Bronze", "Reconcile totals and republish atomically"],
]
add_table(slide,rows,0.65,1.72,12.05,4.85,[2.5,5.1,4.45],font_size=9.6)
add_text(slide,"RPO = acceptable data loss • RTO = acceptable recovery time • both must be validated by drills, not assumed from product features",0.8,6.65,11.75,0.27,9.5,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 30
slide = add_slide("Case study — Real-time food-delivery analytics", "Two consumers, two SLAs, one durable source of truth.", "End-to-End Example")
card(slide,0.7,1.72,5.8,1.7,"Restaurant operations","Live active orders, cancellations, prep time, and delivery delay. p95 freshness <2 minutes; 50K active restaurants.",TEAL,1,15,11)
card(slide,6.8,1.72,5.8,1.7,"Executive analytics","Daily revenue, cohorts, geographic trends, and partner performance. Next-day SLA; history must be reproducible.",PURPLE,2,15,11)
add_rect(slide,0.7,3.75,11.9,2.3,WHITE,True,LIGHT,0.8)
add_text(slide,"Sizing assumptions",0.95,4.0,2.2,0.3,15,NAVY,True)
metrics=[("30M","events/day","5M orders × 6 lifecycle events"),("~350","events/sec","average across the day"),("~833","events/sec","given dinner-rush peak"),("30 GB","raw/day","at ~1 KB per event"),("~22 TB","2-year raw","before compression"),("~50 MB","Redis state","50K restaurants × ~1 KB")]
for i,(v,l,s) in enumerate(metrics):
    x=0.95+i*1.88
    add_text(slide,v,x,4.65,1.6,0.4,20,[TEAL,BLUE,PURPLE,ORANGE,GREEN,RED][i],True,align=PP_ALIGN.CENTER)
    add_text(slide,l,x,5.08,1.6,0.2,9,NAVY,True,align=PP_ALIGN.CENTER)
    add_text(slide,s,x,5.42,1.6,0.32,7.7,MID,align=PP_ALIGN.CENTER)
add_callout(slide,"Challenge the peak assumption: 833/sec is only ~2.4× average; ask whether promotions, region concentration, retries, and growth require more headroom.",1.1,6.25,11.1,0.62)

# 31
slide = add_slide("Food delivery: proposed architecture", "A streaming operational path and a durable lakehouse path share the event backbone.", "End-to-End Example")
# nodes
node(slide,0.45,2.25,1.45,1.0,"Order services","status events",WHITE,TEAL,11)
node(slide,2.25,2.25,1.55,1.0,"Kafka","key: order_id",WHITE,BLUE,13)
arrow(slide,1.92,2.75,2.2,2.75,TEAL,1.7)
# split
node(slide,4.35,1.55,2.05,1.0,"Spark streaming","parse • dedupe • window",WHITE,PURPLE,12)
node(slide,4.35,3.55,2.05,1.0,"Object landing","raw event archive",WHITE,ORANGE,12)
arrow(slide,3.82,2.75,4.3,2.05,BLUE,1.7); arrow(slide,3.82,2.75,4.3,4.05,BLUE,1.7)
node(slide,7.0,1.2,1.55,0.85,"Redis / OLAP","live KPIs",WHITE,TEAL,11)
node(slide,7.0,2.55,1.55,0.85,"Delta Bronze","immutable",WHITE,BRONZE,11)
node(slide,9.05,2.55,1.55,0.85,"Delta Silver","conformed",WHITE,SILVER,11)
node(slide,11.1,2.55,1.55,0.85,"Delta Gold","metrics",WHITE,GOLD,11)
arrow(slide,6.42,2.05,6.95,1.63,PURPLE,1.7); arrow(slide,6.42,2.05,6.95,2.98,PURPLE,1.7); arrow(slide,6.42,4.05,6.95,2.98,ORANGE,1.7)
arrow(slide,8.57,2.98,9.0,2.98,MID,1.7); arrow(slide,10.62,2.98,11.05,2.98,MID,1.7)
node(slide,9.05,4.25,1.55,0.85,"Warehouse / BI","executives",WHITE,PURPLE,11)
node(slide,11.1,4.25,1.55,0.85,"Partner API","restaurants",WHITE,TEAL,11)
arrow(slide,11.88,3.43,9.83,4.2,GOLD,1.5); arrow(slide,8.55,1.63,11.05,4.65,TEAL,1.5)
# cross cutting
add_rect(slide,1.05,5.75,11.25,0.58,NAVY,True)
add_text(slide,"Contracts + catalog + lineage + quality + observability + checkpoints + replay + RBAC",1.05,5.95,11.25,0.18,10,WHITE,True,align=PP_ALIGN.CENTER)
add_text(slide,"Operational truth is revised as late events arrive; finalized daily Gold is reconciled against durable Bronze.",1.0,6.54,11.3,0.25,9.7,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 32
slide = add_slide("Walk the critical behaviors", "Architecture becomes credible when you explain normal flow, late data, failures, replay, and scale.", "End-to-End Example")
behaviors=[
    ("Normal event", "Producer validates contract → Kafka → stream dedupe/window → live store; raw copy lands in Bronze.", TEAL),
    ("Late / out-of-order", "Use event time + watermark; update recent live windows; retain raw event for final batch reconciliation.", BLUE),
    ("Duplicate delivery", "event_id/business key dedupe; transactional MERGE keeps the observable table idempotent.", PURPLE),
    ("Bad schema", "Registry blocks known incompatibility; Bronze rescues drift; Silver quarantines; owner receives alert.", ORANGE),
    ("Backfill", "Read immutable Bronze for bounded dates → same transforms → validate → atomically replace affected outputs.", GREEN),
    ("10× dinner rush", "Increase partitions/consumers; test key skew; autoscale; degrade gracefully by serving stale-but-labeled data.", RED),
]
for i,(t,b,c) in enumerate(behaviors):
    card(slide,0.7+(i%2)*6.15,1.62+(i//2)*1.55,5.75,1.18,t,b,c,title_size=13,body_size=9.5)
add_callout(slide,"Final check: can you trace one event from producer to dashboard, then replay that same event without creating a duplicate or losing auditability?",1.1,6.38,11.1,0.6)

# 33
slide = add_slide("How to narrate your design", "Use a repeated sentence structure so every choice is defensible.", "Interview Execution", bg=NAVY)
formula=[("Because…","requirement / estimate",TEAL),("I choose…","component / pattern",BLUE),("This gives…","desired property",PURPLE),("It costs…","complexity / money / latency",ORANGE),("I mitigate…","control / fallback",GREEN)]
for i,(a,b,c) in enumerate(formula):
    x=0.55+i*2.55
    add_rect(slide,x,1.85,2.17,1.45,c,True)
    add_text(slide,a,x,2.15,2.17,0.25,15,WHITE,True,align=PP_ALIGN.CENTER)
    add_text(slide,b,x+0.15,2.65,1.87,0.3,9,WHITE,align=PP_ALIGN.CENTER)
    if i<4: arrow(slide,x+2.18,2.58,x+2.47,2.58,LIGHT,1.4)
add_text(slide,"Worked example",0.75,3.9,2.0,0.3,14,ORANGE,True)
example="Because partner dashboards need p95 <2-minute freshness, I choose a Kafka + streaming aggregation path into a low-latency serving store. This gives continuous updates and decouples producers from consumers. It costs always-on compute and state management, so I mitigate with bounded windows, checkpoints, lag alerts, replay retention, and a lakehouse reconciliation path."
add_text(slide,example,0.78,4.35,11.75,1.25,17,WHITE,False,italic=True)
add_callout(slide,"Say what you are deliberately not solving yet. Prioritize the critical path, then deepen only where the interviewer probes.",1.35,6.05,10.65,0.64,RGBColor(35,58,84),TEAL,11)

# 34
slide = add_slide("Self-review scorecard", "Before finishing, verify that each category has a concrete answer.", "Interview Execution")
score=[
    ("Requirements",["Named consumers and outputs","Measurable latency/availability","Retention/security assumptions"],TEAL),
    ("Scale",["Average + peak throughput","Storage and growth math","Hot keys/cardinality considered"],BLUE),
    ("Architecture",["End-to-end data flow","Batch/stream rationale","Serving choice tied to query"],PURPLE),
    ("Data design",["Grain, keys, model","Formats and layout","Late data and SCD policy"],ORANGE),
    ("Reliability",["Quality + contracts","Idempotency + replay","Backfill, schema, DR"],GREEN),
    ("Trade-offs",["Cost and complexity","Bottleneck at 10×","Alternative and switch condition"],RED),
]
for i,(t,vals,c) in enumerate(score):
    x=0.65+(i%3)*4.22; y=1.65+(i//3)*2.35
    add_rect(slide,x,y,3.85,1.85,WHITE,True,LIGHT,0.8)
    add_rect(slide,x,y,3.85,0.5,c,True)
    add_text(slide,t,x,y+0.16,3.85,0.17,12,WHITE,True,align=PP_ALIGN.CENTER)
    lines=["☐ "+v for v in vals]
    add_rich_lines(slide,lines,x+0.25,y+0.75,3.35,0.9,10.5,DARK,False,c,6)
add_text(slide,"If one box is weak, state it as an open question and describe how you would validate it.",1.1,6.48,11.1,0.3,10.5,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 35
slide = add_slide("Reusable one-page design template", "Copy this structure onto the whiteboard before solving any data system design prompt.", "Interview Execution")
sections=[
    ("1. USERS + OUTPUTS","Consumers • use cases • interfaces • key queries",TEAL),
    ("2. SLOs + CONSTRAINTS","Freshness • availability • retention • security • cost",BLUE),
    ("3. SCALE MATH","events/sec avg+peak • bytes/day • growth • cardinality",PURPLE),
    ("4. DATA FLOW","sources → ingest → process → store → serve",ORANGE),
    ("5. DATA DESIGN","grain • keys • model • format • partition/layout",GREEN),
    ("6. OPERATIONS","quality • observability • replay • backfill • schema • DR",RED),
]
for i,(t,b,c) in enumerate(sections):
    x=0.65+(i%2)*6.2; y=1.58+(i//2)*1.62
    add_rect(slide,x,y,5.85,1.25,WHITE,True,LIGHT,0.8)
    add_rect(slide,x,y,0.12,1.25,c,False)
    add_text(slide,t,x+0.3,y+0.18,5.2,0.25,12,NAVY,True)
    add_text(slide,b,x+0.3,y+0.63,5.2,0.3,10,DARK)
add_callout(slide,"Finish with: bottleneck at 10× • biggest correctness risk • biggest cost driver • alternative architecture • unresolved assumptions",1.0,6.48,11.3,0.5)

# 36
slide = add_slide("Key takeaways", "A complete design is measurable, explainable, recoverable, and operable.", "Summary", bg=NAVY)
takeaways=[
    ("Start with people and SLAs", "Consumers and measurable outcomes determine the architecture.", TEAL),
    ("Calculate before selecting tools", "Peak rate, bytes, retention, and cardinality reveal constraints.", BLUE),
    ("Prefer simple, then justify complexity", "Batch by default; streaming only for a real latency need.", PURPLE),
    ("Model for meaning and access", "State grain, history, schema contracts, and serving queries.", ORANGE),
    ("Design the rerun before the first run", "Idempotency, replay, backfill, and schema migration are core paths.", GREEN),
    ("Narrate every trade-off", "Requirement → decision → benefit → cost → mitigation.", RED),
]
for i,(t,b,c) in enumerate(takeaways):
    x=0.75+(i%2)*6.05; y=1.55+(i//2)*1.62
    add_rect(slide,x,y,5.55,1.22,RGBColor(27,47,74),True,c,1)
    add_rect(slide,x+0.2,y+0.25,0.5,0.5,c,True)
    add_text(slide,str(i+1),x+0.2,y+0.41,0.5,0.16,10,WHITE,True,align=PP_ALIGN.CENTER)
    add_text(slide,t,x+0.9,y+0.18,4.35,0.27,13,WHITE,True)
    add_text(slide,b,x+0.9,y+0.63,4.35,0.36,9.5,LIGHT)
add_text(slide,"The best design is not the most sophisticated—it is the simplest design that meets the stated requirements and has a credible failure story.",1.0,6.55,11.3,0.34,12,ORANGE,True,align=PP_ALIGN.CENTER)

# 37 — AI ERP specialization
slide = add_slide("AI-powered ERP changes the design problem", "ERP combines financial correctness, tenant isolation, operational freshness, and governed AI.", "AI ERP Specialization", bg=NAVY)
pillars = [
    ("SYSTEM OF RECORD", "Orders, invoices, journals, payroll, inventory\nCorrectness and auditability first", TEAL),
    ("MULTI-TENANT SAAS", "Shared platform, isolated customers\nNo cross-tenant data exposure", BLUE),
    ("OPERATIONAL ANALYTICS", "Live close, cash, supply, workforce\nFresh and explainable metrics", PURPLE),
    ("AI COPILOTS", "Forecast, explain, recommend, automate\nGrounded and permission-aware", ORANGE),
]
for i,(t,b,c) in enumerate(pillars):
    x=0.68+(i%2)*6.1; y=1.68+(i//2)*2.05
    add_rect(slide,x,y,5.7,1.58,RGBColor(27,47,74),True,c,1.1)
    add_rect(slide,x+0.22,y+0.25,0.55,0.55,c,True)
    add_text(slide,str(i+1),x+0.22,y+0.43,0.55,0.18,11,WHITE,True,align=PP_ALIGN.CENTER)
    add_text(slide,t,x+0.95,y+0.2,4.45,0.3,14,WHITE,True)
    add_text(slide,b,x+0.95,y+0.72,4.45,0.55,10.5,LIGHT)
add_callout(slide,"ERP design rule: an AI answer is only as trustworthy as the transactional data, business semantics, permissions, and lineage behind it.",1.0,6.1,11.3,0.72,RGBColor(35,58,84),ORANGE,11.5)

# 38
slide = add_slide("AI ERP workloads and service levels", "One platform supports very different correctness, latency, and serving requirements.", "AI ERP Specialization")
rows = [
    ["Workload", "Typical output", "Target", "Primary design pressure"],
    ["Financial close", "Trial balance, consolidation, exceptions", "Minutes to hourly; final must reconcile", "Correctness, restatement, audit trail"],
    ["Operations", "Inventory, order, fulfillment dashboards", "Seconds to <5 minutes", "CDC lag, hot keys, serving latency"],
    ["Planning / forecasting", "Demand, cash, workforce forecasts", "Daily/weekly plus scenario runs", "Point-in-time features, reproducibility"],
    ["ERP copilot / RAG", "Answers with citations and actions", "Interactive, often <5 seconds", "Authorization, grounding, freshness"],
    ["Regulatory / audit", "Evidence, lineage, access history", "On demand; immutable retention", "Completeness, legal holds, residency"],
]
add_table(slide,rows,0.62,1.72,12.1,4.65,[2.15,3.25,2.45,4.25],font_size=9.5)
add_callout(slide,"Do not force every workload into one store. Share governed data and semantics, then use serving systems suited to each access pattern.",1.0,6.42,11.3,0.62)

# 39
slide = add_slide("Reference architecture for an AI ERP platform", "Separate transactional authority, analytical truth, and AI serving while preserving lineage.", "AI ERP Specialization")
node(slide,0.4,2.15,1.5,1.0,"ERP modules","finance • HR • SCM",WHITE,TEAL,11)
node(slide,0.4,4.0,1.5,0.85,"Documents","contracts • invoices",WHITE,ORANGE,11)
node(slide,2.3,2.15,1.5,1.0,"CDC + events","LSN/offset + schema",WHITE,BLUE,11)
node(slide,2.3,4.0,1.5,0.85,"Document ingest","OCR • parse • classify",WHITE,BLUE,10)
arrow(slide,1.92,2.65,2.25,2.65,TEAL,1.6); arrow(slide,1.92,4.42,2.25,4.42,ORANGE,1.6)
node(slide,4.25,1.62,1.65,0.85,"Bronze","immutable tenant data",WHITE,BRONZE,11)
node(slide,4.25,2.85,1.65,0.85,"Silver","canonical ERP entities",WHITE,SILVER,11)
node(slide,4.25,4.08,1.65,0.85,"Gold","metrics + features",WHITE,GOLD,11)
arrow(slide,3.82,2.65,4.2,2.05,BLUE,1.5); arrow(slide,3.82,4.42,4.2,4.5,BLUE,1.5)
arrow(slide,5.08,2.5,5.08,2.8,MID,1.3); arrow(slide,5.08,3.73,5.08,4.03,MID,1.3)
node(slide,6.45,1.55,1.65,0.85,"Semantic layer","governed measures",WHITE,PURPLE,10)
node(slide,6.45,2.78,1.65,0.85,"Feature store","point-in-time",WHITE,PURPLE,10)
node(slide,6.45,4.01,1.65,0.85,"Vector index","tenant + ACL filters",WHITE,PURPLE,10)
arrow(slide,5.92,2.05,6.4,1.97,GOLD,1.4); arrow(slide,5.92,3.28,6.4,3.2,SILVER,1.4); arrow(slide,5.92,4.5,6.4,4.43,ORANGE,1.4)
node(slide,8.65,1.55,1.7,0.85,"Warehouse / BI","finance + operations",WHITE,GREEN,10)
node(slide,8.65,2.78,1.7,0.85,"ML platform","train • registry • score",WHITE,GREEN,10)
node(slide,8.65,4.01,1.7,0.85,"AI gateway","retrieve • policy • cite",WHITE,GREEN,10)
arrow(slide,8.12,1.97,8.6,1.97,PURPLE,1.4); arrow(slide,8.12,3.2,8.6,3.2,PURPLE,1.4); arrow(slide,8.12,4.43,8.6,4.43,PURPLE,1.4)
node(slide,10.9,1.55,1.95,0.85,"Dashboards","tenant analytics",WHITE,TEAL,10)
node(slide,10.9,2.78,1.95,0.85,"Predictions","forecast • anomaly",WHITE,TEAL,10)
node(slide,10.9,4.01,1.95,0.85,"Copilot / actions","answer • propose • approve",WHITE,TEAL,10)
arrow(slide,10.37,1.97,10.85,1.97,GREEN,1.4); arrow(slide,10.37,3.2,10.85,3.2,GREEN,1.4); arrow(slide,10.37,4.43,10.85,4.43,GREEN,1.4)
add_rect(slide,1.0,5.65,11.3,0.62,NAVY,True)
add_text(slide,"Tenant identity • RBAC/ABAC • catalog/lineage • contracts • quality • observability • audit • cost attribution",1.0,5.86,11.3,0.2,9.5,WHITE,True,align=PP_ALIGN.CENTER)

# 40
slide = add_slide("Multi-tenant isolation is a data-plane decision", "Carry tenant identity through every key, partition, policy, cache, vector lookup, and audit event.", "AI ERP Specialization")
rows = [
    ["Pattern", "Isolation", "Advantages", "Trade-offs / fit"],
    ["Shared tables", "tenant_id + row/column policies", "Efficient, simple fleet, good for many small tenants", "Highest policy-test burden; noisy-neighbor controls required"],
    ["Schema/database per tenant", "Logical or physical namespace", "Clearer boundaries and restore operations", "Metadata and migration overhead at large tenant counts"],
    ["Dedicated stack", "Separate compute/storage/account", "Strongest isolation and custom controls", "Highest cost; use for regulated or very large tenants"],
    ["Tiered hybrid", "Route tenant by risk/size/tier", "Balances cost and isolation", "Provisioning, routing, and consistent governance are harder"],
]
add_table(slide,rows,0.6,1.68,12.15,3.7,[2.25,2.7,3.45,3.75],font_size=9.35)
add_text(slide,"Non-negotiable controls",0.72,5.7,2.25,0.3,14,NAVY,True)
for i,(t,c) in enumerate([("Tenant-scoped encryption",TEAL),("Policy tests in CI",BLUE),("Per-tenant quotas",PURPLE),("Tenant-aware caches",ORANGE),("Vector ACL filters",GREEN),("Break-glass audit",RED)]):
    add_chip(slide,t,0.75+i*2.05,6.16,1.82,c,WHITE)

# 41
slide = add_slide("CDC and financial correctness", "Capture database changes without confusing technical delivery with business truth.", "AI ERP Specialization")
# pipeline
node(slide,0.55,2.1,1.55,1.0,"OLTP ledger","ACID journal entries",WHITE,TEAL,11)
node(slide,2.55,2.1,1.55,1.0,"CDC log","LSN + transaction ID",WHITE,BLUE,11)
node(slide,4.55,2.1,1.65,1.0,"Raw change log","before/after + op",WHITE,BRONZE,11)
node(slide,6.65,2.1,1.65,1.0,"Canonical ledger","dedupe + sequence",WHITE,SILVER,11)
node(slide,8.75,2.1,1.65,1.0,"Balanced facts","debit = credit",WHITE,GOLD,11)
node(slide,10.85,2.1,1.85,1.0,"Reports / AI","as-of view + lineage",WHITE,PURPLE,11)
for x,c in [(2.12,TEAL),(4.12,BLUE),(6.22,BRONZE),(8.32,SILVER),(10.42,GOLD)]: arrow(slide,x,2.6,x+0.38,2.6,c,1.5)
checks=[
    ("Order changes", "Preserve source transaction order; partition by stable aggregate such as company + ledger."),
    ("Idempotency", "Use source transaction/row identity and LSN; record consumed range with target commit."),
    ("Corrections", "Post reversals or new versions; do not erase closed-period history."),
    ("Reconciliation", "Compare source counts, control totals, debit/credit, and period balances."),
]
for i,(t,b) in enumerate(checks):
    card(slide,0.7+(i%2)*6.15,3.75+(i//2)*1.18,5.75,0.95,t,b,[TEAL,BLUE,PURPLE,ORANGE][i],title_size=12,body_size=9)
add_text(slide,"Exactly-once business outcome = ordered source identity + idempotent target + atomic progress + reconciliation",1.0,6.46,11.3,0.28,10.5,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 42
slide = add_slide("Canonical ERP semantics and the AI/RAG data plane", "AI must use the same governed definitions and permissions as reports and workflows.", "AI ERP Specialization")
# left canonical model
add_rect(slide,0.65,1.67,5.65,4.75,WHITE,True,LIGHT,0.8)
add_text(slide,"Canonical ERP model",0.9,1.95,5.15,0.3,16,NAVY,True,align=PP_ALIGN.CENTER)
entities=[("Party","customer • supplier • worker"),("Legal entity","company • book • currency"),("Transaction","order • invoice • payment"),("Resource","item • asset • inventory"),("Accounting","journal • account • period")]
for i,(t,b) in enumerate(entities):
    node(slide,1.0+(i%2)*2.55,2.55+(i//2)*1.05,2.15,0.72,t,b,RGBColor(249,251,254),[TEAL,BLUE,PURPLE,ORANGE,GREEN][i],10)
# right AI flow
add_rect(slide,6.65,1.67,6.05,4.75,WHITE,True,LIGHT,0.8)
add_text(slide,"Permission-aware AI retrieval",6.9,1.95,5.55,0.3,16,NAVY,True,align=PP_ALIGN.CENTER)
node(slide,7.0,2.6,1.35,0.82,"User question","tenant + role",WHITE,TEAL,10)
node(slide,8.72,2.6,1.35,0.82,"Policy check","row + field ACL",WHITE,BLUE,10)
node(slide,10.44,2.6,1.75,0.82,"Hybrid retrieval","SQL + vector + metadata",WHITE,PURPLE,10)
arrow(slide,8.37,3.01,8.67,3.01,TEAL,1.3); arrow(slide,10.09,3.01,10.39,3.01,BLUE,1.3)
node(slide,7.0,4.15,1.6,0.82,"Grounded context","freshness + citations",WHITE,ORANGE,10)
node(slide,9.05,4.15,1.5,0.82,"LLM gateway","prompt + guardrails",WHITE,GREEN,10)
node(slide,11.0,4.15,1.2,0.82,"Answer","cite or abstain",WHITE,RED,10)
arrow(slide,11.3,3.45,8.0,4.1,PURPLE,1.3); arrow(slide,8.62,4.56,9.0,4.56,ORANGE,1.3); arrow(slide,10.57,4.56,10.95,4.56,GREEN,1.3)
add_text(slide,"Never put unrestricted tenant data into prompts, caches, traces, or vector indexes.",7.0,5.55,5.25,0.35,10.5,RED,True,align=PP_ALIGN.CENTER)

# 43
slide = add_slide("Govern the AI lifecycle like a data product", "Trace every answer and prediction to authorized data, model version, policy, and evaluation result.", "AI ERP Specialization")
stages=[
    ("INGEST", "contract • consent • classification", TEAL),
    ("CURATE", "quality • lineage • point-in-time", BLUE),
    ("TRAIN / INDEX", "dataset snapshot • model/embed version", PURPLE),
    ("SERVE", "tenant policy • prompt • retrieval • cache", ORANGE),
    ("EVALUATE", "groundedness • accuracy • fairness • drift", GREEN),
    ("ACT", "approval • idempotency • audit • rollback", RED),
]
for i,(t,b,c) in enumerate(stages):
    x=0.55+i*2.1
    add_rect(slide,x,1.8,1.75,3.35,WHITE,True,c,1)
    add_rect(slide,x,1.8,1.75,0.57,c,True)
    add_text(slide,t,x,2.0,1.75,0.18,10.5,WHITE,True,align=PP_ALIGN.CENTER)
    add_text(slide,b,x+0.17,2.72,1.41,1.3,10,DARK,align=PP_ALIGN.CENTER)
    add_chip(slide,str(i+1),x+0.62,4.47,0.5,c,WHITE)
    if i<5: arrow(slide,x+1.76,3.46,x+2.03,3.46,MID,1.2)
add_callout(slide,"For write-back automation, treat the LLM as an untrusted planner: validate against ERP rules, require approval by risk tier, use an idempotency key, and log before/after state.",0.9,5.62,11.5,0.88,RGBColor(255,246,234),ORANGE,11)

# 44
slide = add_slide("Tenant-aware sizing, month-end scale, and resilience", "Capacity planning must consider both fleet totals and the largest tenant or legal entity.", "AI ERP Specialization")
add_rect(slide,0.65,1.68,6.2,4.65,WHITE,True,LIGHT,0.8)
add_text(slide,"Illustrative sizing",0.95,1.95,5.6,0.3,15,NAVY,True)
add_rich_lines(slide,[
    ("Fleet events/day: ","8,000 tenants × 250K changes ≈ 2B changes/day"),
    ("Average ingest: ","2B ÷ 86,400 ≈ 23K changes/sec"),
    ("Month-end peak: ","assume 6× ≈ 139K changes/sec"),
    ("Raw storage: ","2B × 1.2 KB ≈ 2.4 TB/day before compression"),
    ("Largest tenant: ","may be 10–20% of peak; isolate hot keys and quotas"),
],0.98,2.52,5.55,2.95,13,DARK,True,TEAL,10)
add_text(slide,"Resilience decisions",7.25,1.95,5.15,0.3,15,NAVY,True)
for i,(t,b,c) in enumerate([
    ("Burst control","buffer in log; autoscale consumers; reserve month-end capacity",TEAL),
    ("Fairness","tenant quotas and weighted scheduling prevent noisy neighbors",BLUE),
    ("Regional design","respect data residency; replicate metadata and allowed data",PURPLE),
    ("Recovery","tier RPO/RTO for ledger, analytics, indexes, and derived AI outputs",ORANGE),
]):
    card(slide,7.2,2.48+i*0.93,5.15,0.75,t,b,c,title_size=11,body_size=8.4)
add_callout(slide,"Derived embeddings and predictions can usually be rebuilt; source transactions, audit evidence, and policy history require stronger protection.",1.2,6.48,10.9,0.48)

# 45
slide = add_slide("How to answer an AI ERP system-design prompt", "Lead with business invariants, then connect data and AI choices to tenant and financial risk.", "AI ERP Interview")
steps=[
    ("1", "Clarify modules + users", "Finance, HR, SCM, planners, auditors, copilots", TEAL),
    ("2", "State invariants", "Tenant isolation, balanced ledger, as-of accuracy", BLUE),
    ("3", "Set SLOs", "CDC lag, report finality, AI response, RPO/RTO", PURPLE),
    ("4", "Size fleet + tenant", "Average, month-end peak, largest tenant, documents", ORANGE),
    ("5", "Draw 3 planes", "Transactional, analytical, and AI serving", GREEN),
    ("6", "Explain semantics", "Canonical entities, dimensions, metric definitions", RED),
    ("7", "Prove recovery", "Replay, reconciliation, backfill, schema migration", TEAL_DARK),
    ("8", "Prove AI safety", "Authorization, grounding, evaluation, approval, audit", NAVY_2),
]
for i,(n,t,b,c) in enumerate(steps):
    x=0.65+(i%2)*6.2; y=1.55+(i//2)*1.28
    add_rect(slide,x,y,5.85,0.98,WHITE,True,LIGHT,0.8)
    add_rect(slide,x+0.18,y+0.2,0.5,0.5,c,True)
    add_text(slide,n,x+0.18,y+0.36,0.5,0.17,10,WHITE,True,align=PP_ALIGN.CENTER)
    add_text(slide,t,x+0.9,y+0.12,2.0,0.24,12,NAVY,True)
    add_text(slide,b,x+2.9,y+0.17,2.7,0.48,9,DARK)
add_text(slide,"Close with the highest-risk trade-off: correctness vs. freshness, isolation vs. cost, or automation vs. control.",1.0,6.65,11.3,0.28,10.5,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 46
slide = add_slide("Complex AI ERP interview Q&A — 1 to 4", "Use the short answer on the slide; use speaker notes for a deeper model response.", "AI ERP Interview")
qa1=[
    ("1. Design near-real-time analytics for 10K tenants", "Shared CDC + lakehouse with tenant-keyed records, policy enforcement, per-tenant lag/SLOs, workload isolation, and optional dedicated tiers.", TEAL),
    ("2. Guarantee exactly-once financial reporting", "Preserve source transaction identity/order, idempotently merge, atomically track progress, enforce accounting invariants, and reconcile control totals.", BLUE),
    ("3. Support tenant custom fields at scale", "Stable core schema plus typed extension/JSON map in Bronze-Silver; promote governed fields selectively; never create uncontrolled columns per tenant.", PURPLE),
    ("4. Handle closed-period corrections", "Retain immutable history, post reversal/adjustment entries, version as-of facts, rebuild affected aggregates, and expose restatement lineage.", ORANGE),
]
for i,(q,a,c) in enumerate(qa1):
    card(slide,0.65+(i%2)*6.2,1.55+(i//2)*2.38,5.85,1.9,q,a,c,title_size=13,body_size=10.2)
add_text(slide,"What interviewers are testing: tenant isolation • ordering • idempotency • extensibility • auditability",1.0,6.55,11.3,0.28,10,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 47
slide = add_slide("Complex AI ERP interview Q&A — 5 to 8", "AI features add authorization, point-in-time correctness, grounding, and evaluation requirements.", "AI ERP Interview")
qa2=[
    ("5. Build an ERP copilot over tables and documents", "Use governed SQL plus permission-filtered hybrid retrieval, freshness metadata, citations, an AI gateway, and abstention when evidence is weak.", TEAL),
    ("6. Prevent cross-tenant leakage in RAG", "Separate namespaces or mandatory tenant filters, propagate ACLs to chunks, tenant-aware caches, adversarial tests, and audited policy decisions.", BLUE),
    ("7. Create forecasting features without leakage", "Event-time snapshots, point-in-time joins, versioned feature definitions, reproducible training sets, and online/offline consistency checks.", PURPLE),
    ("8. Measure whether AI answers are trustworthy", "Evaluate retrieval recall, citation correctness, groundedness, business-rule accuracy, freshness, abstention, and outcome quality by tenant/use case.", ORANGE),
]
for i,(q,a,c) in enumerate(qa2):
    card(slide,0.65+(i%2)*6.2,1.55+(i//2)*2.38,5.85,1.9,q,a,c,title_size=13,body_size=10.2)
add_text(slide,"What interviewers are testing: secure retrieval • data/ML lineage • evaluation • semantic correctness",1.0,6.55,11.3,0.28,10,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# 48
slide = add_slide("Complex AI ERP interview Q&A — 9 to 12", "The strongest answers explain deletion, backfill, month-end scaling, and regional recovery together.", "AI ERP Interview")
qa3=[
    ("9. Delete personal data but retain required audit evidence", "Classify fields, tokenize identities, apply purpose-specific retention, delete from derived stores/indexes, and preserve legally required non-PII evidence with approval.", TEAL),
    ("10. Backfill two years without hurting live workloads", "Use immutable snapshots, isolated compute and quotas, partitioned incremental publication, validation/control totals, and resumable audited run manifests.", BLUE),
    ("11. Survive a 10× month-end close spike", "Buffer CDC, pre-scale, isolate hot tenants/legal entities, prioritize critical ledgers, use fair scheduling, and serve labeled stale analytics if necessary.", PURPLE),
    ("12. Recover from a region outage with residency rules", "Define data-class RPO/RTO, keep allowed regional copies, replicate catalog/code/checkpoints, rebuild derived AI indexes, and regularly exercise failover.", ORANGE),
]
for i,(q,a,c) in enumerate(qa3):
    card(slide,0.65+(i%2)*6.2,1.55+(i//2)*2.38,5.85,1.9,q,a,c,title_size=13,body_size=10.2)
add_text(slide,"What interviewers are testing: privacy • operability • capacity planning • disaster recovery • compliance trade-offs",1.0,6.55,11.3,0.28,10,TEAL_DARK,True,align=PP_ALIGN.CENTER)

# Campfire specialization — based on the user-provided candidate guide summary
slide = add_slide("Campfire interview lens", "Connect senior data engineering decisions to customer value, accounting trust, and rapid delivery.", "Campfire Preparation", bg=NAVY)
add_text(slide,"MISSION FROM SUPPLIED GUIDE",0.75,1.58,3.5,0.28,10,ORANGE,True)
add_text(slide,"Give accounting and finance teams superpowers",0.75,2.0,6.15,0.55,24,WHITE,True)
add_text(slide,"Automate repetitive work, deliver timely financial insight, and free teams for higher-value decisions through delightful experiences.",0.78,2.77,5.95,0.95,14,LIGHT)
values=[("TRANSPARENT\nACCOUNTABILITY",TEAL),("CUSTOMER-CENTRIC\nINNOVATION",BLUE),("GROWTH\nMINDSET",PURPLE),("QUALITY WITH\nVELOCITY",ORANGE),("COLLABORATIVE\nEXCELLENCE",GREEN)]
for i,(t,c) in enumerate(values):
    x=0.72+i*2.48
    add_rect(slide,x,4.25,2.12,1.05,RGBColor(27,47,74),True,c,1)
    add_text(slide,t,x+0.12,4.54,1.88,0.45,10,WHITE,True,align=PP_ALIGN.CENTER)
add_callout(slide,"Interview signal: be direct about assumptions and risks, ask why, invite alternatives, and connect architecture to accountants' daily work.",1.0,5.9,11.3,0.72,RGBColor(35,58,84),ORANGE,11)

slide = add_slide("Where data engineering creates customer superpowers", "Translate platform capabilities into faster, safer finance outcomes.", "Campfire Preparation")
use_cases=[
    ("FASTER CLOSE", "Live ingestion, reconciliation, exception queues, period snapshots, and restatement lineage.", TEAL),
    ("LESS MANUAL WORK", "Document extraction, matching, coding suggestions, approvals, and idempotent workflow actions.", BLUE),
    ("REAL-TIME INTELLIGENCE", "Cash, revenue, spend, variance, and anomaly insights with freshness and finality labels.", PURPLE),
    ("TRUSTED AI", "Permission-aware retrieval, governed finance semantics, citations, evaluation, and human controls.", ORANGE),
]
for i,(t,b,c) in enumerate(use_cases):
    card(slide,0.68+(i%2)*6.12,1.68+(i//2)*2.12,5.72,1.62,t,b,c,i+1,14,10.5)
add_callout(slide,"Senior answer: name the user, manual pain, measurable outcome, financial invariant, and smallest safe release—not only the pipeline.",1.0,6.15,11.3,0.68)

slide = add_slide("Campfire-style AI-native finance architecture", "Keep transactional authority, financial intelligence, and AI automation connected by lineage and policy.", "Campfire Preparation")
node(slide,0.35,1.85,1.45,0.95,"Finance sources","GL • AP/AR • cash",WHITE,TEAL,10)
node(slide,0.35,3.45,1.45,0.95,"Documents","invoices • contracts",WHITE,ORANGE,10)
node(slide,2.15,1.85,1.45,0.95,"CDC + events","tenant • txn • LSN",WHITE,BLUE,10)
node(slide,2.15,3.45,1.45,0.95,"AI extraction","parse • classify",WHITE,BLUE,10)
arrow(slide,1.82,2.33,2.1,2.33,TEAL,1.4); arrow(slide,1.82,3.93,2.1,3.93,ORANGE,1.4)
node(slide,4.0,1.38,1.7,0.82,"Bronze","immutable evidence",WHITE,BRONZE,10)
node(slide,4.0,2.55,1.7,0.82,"Silver","canonical finance",WHITE,SILVER,10)
node(slide,4.0,3.72,1.7,0.82,"Gold","governed metrics",WHITE,GOLD,10)
node(slide,4.0,4.89,1.7,0.82,"Audit ledger","versions + approvals",WHITE,RED,10)
arrow(slide,3.62,2.33,3.95,1.8,BLUE,1.3); arrow(slide,3.62,3.93,3.95,4.12,BLUE,1.3)
node(slide,6.15,1.55,1.75,0.85,"Semantic layer","finance definitions",WHITE,PURPLE,10)
node(slide,6.15,2.8,1.75,0.85,"Feature / model","forecast • anomaly",WHITE,PURPLE,10)
node(slide,6.15,4.05,1.75,0.85,"Secure retrieval","SQL + docs + ACL",WHITE,PURPLE,10)
arrow(slide,5.72,1.8,6.1,1.97,GOLD,1.3); arrow(slide,5.72,3.0,6.1,3.22,SILVER,1.3); arrow(slide,5.72,4.12,6.1,4.47,ORANGE,1.3)
node(slide,8.35,1.55,1.7,0.85,"Close workspace","reconcile • explain",WHITE,GREEN,10)
node(slide,8.35,2.8,1.7,0.85,"Intelligence","cash • variance",WHITE,GREEN,10)
node(slide,8.35,4.05,1.7,0.85,"AI copilot","cite • propose",WHITE,GREEN,10)
arrow(slide,7.92,1.97,8.3,1.97,PURPLE,1.3); arrow(slide,7.92,3.22,8.3,3.22,PURPLE,1.3); arrow(slide,7.92,4.47,8.3,4.47,PURPLE,1.3)
node(slide,10.5,2.05,2.2,1.05,"Controlled action","validate • approve • post",WHITE,TEAL,11)
node(slide,10.5,3.85,2.2,1.05,"Customer experience","fresh • clear • auditable",WHITE,ORANGE,11)
arrow(slide,10.07,4.47,10.45,2.58,GREEN,1.3); arrow(slide,11.6,3.12,11.6,3.8,TEAL,1.3)
add_text(slide,"Cross-cutting: tenant policy • finance contracts • reconciliation • lineage • evaluation • observability • cost",0.8,6.35,11.7,0.3,10,NAVY,True,align=PP_ALIGN.CENTER)

slide = add_slide("Non-negotiable finance and AI controls", "Move quickly around the controls—not through them.", "Campfire Preparation")
controls=[
    ("FINANCIAL TRUTH",["Debit = credit by journal/currency","Source control totals reconcile","Closed-period changes are versioned","Every metric has cutoff + lineage"],TEAL),
    ("TENANT + ACCESS",["Tenant identity at every boundary","Row/field/document authorization","Tenant-aware caches and indexes","Negative access tests"],BLUE),
    ("AI AUTOMATION",["Model is an untrusted planner","Typed validated commands","Risk-based human approval","Idempotency + before/after audit"],PURPLE),
]
for i,(t,vals,c) in enumerate(controls):
    x=0.68+i*4.2
    add_rect(slide,x,1.72,3.78,4.35,WHITE,True,c,1.2)
    add_rect(slide,x,1.72,3.78,0.64,c,True)
    add_text(slide,t,x,1.94,3.78,0.2,12,WHITE,True,align=PP_ALIGN.CENTER)
    add_rich_lines(slide,vals,x+0.3,2.75,3.15,2.3,10.5,DARK,True,c,9)
    add_chip(slide,["reconcile","authorize","approve + audit"][i],x+1.05,5.35,1.68,c,WHITE)
add_callout(slide,"Quality with velocity: automate these gates, use tenant canaries and feature flags, and make rollback faster than debate during an incident.",1.0,6.25,11.3,0.57)

slide = add_slide("Model prompt: design real-time close intelligence", "Show the complete answer before deep-diving into CDC ordering, reconciliation, or AI explanation.", "Campfire Preparation")
phases=[
    ("1. CLARIFY", "Controllers/accountants; live exceptions vs final close; entities/currencies; p95 freshness; restatement rules", TEAL),
    ("2. ESTIMATE", "Tenants + largest tenant; journal lines/day; month-end burst; document volume; retention", BLUE),
    ("3. DESIGN", "Ordered CDC → immutable Bronze → canonical finance Silver → reconciled Gold → workspace/AI gateway", PURPLE),
    ("4. PROVE", "Tenant isolation; debit/credit; source totals; idempotent replay; period snapshot; citations", ORANGE),
    ("5. OPERATE", "Per-tenant lag; exception queues; canaries; backfill manifests; RPO/RTO; cost attribution", GREEN),
]
for i,(t,b,c) in enumerate(phases):
    y=1.52+i*1.04
    add_rect(slide,0.72,y,11.9,0.79,WHITE,True,LIGHT,0.8)
    add_rect(slide,0.9,y+0.14,1.45,0.5,c,True)
    add_text(slide,t,0.9,y+0.3,1.45,0.18,9.5,WHITE,True,align=PP_ALIGN.CENTER)
    add_text(slide,b,2.62,y+0.18,9.65,0.4,9.8,DARK)
add_text(slide,"Close with the tension: fast provisional intelligence vs reproducible financial finality—and explain how the design supports both.",0.9,6.66,11.55,0.25,10,TEAL_DARK,True,align=PP_ALIGN.CENTER)

slide = add_slide("Translate Campfire values into interview evidence", "Do not only repeat a value—show a decision, behavior, and measurable outcome.", "Campfire Preparation")
rows=[
    ["Value from supplied guide","Technical behavior to show","Evidence in your story"],
    ["Transparent Accountability","State assumptions/risks; own incidents; communicate directly","Impact contained, stakeholders informed, data repaired, prevention shipped"],
    ["Customer-Centric Innovation","Begin with accountant pain and workflow outcome","Close time, manual hours, exceptions, or trust measurably improved"],
    ["Growth Mindset / Low Ego","Invite alternatives; change view when evidence wins","Feedback changed your design and improved the result"],
    ["Quality with Velocity","Small slices, automated gates, canaries, rollback","Shipped quickly with reconciliation/security proof"],
    ["Collaborative Excellence","Align finance, product, security, and engineering","Clear ownership, resolved conflict, shared team outcome"],
]
add_table(slide,rows,0.58,1.65,12.18,4.8,[2.7,4.0,5.48],font_size=9.35)
add_callout(slide,"Best story structure: customer stakes → your decision → alternatives → action → measured result → mistake/learning → what changed afterward.",1.0,6.45,11.3,0.55)

slide = add_slide("Campfire interview-day preparation", "Arrive ready for a collaborative conversation, not a memorized performance.", "Campfire Preparation")
card(slide,0.68,1.62,3.78,2.05,"PREPARE 3 STORIES","1. Customer empathy + innovation\n2. Quality with velocity\n3. Accountability + collaboration\n\nInclude metrics and what you learned.",TEAL,1,14,10.5)
card(slide,4.78,1.62,3.78,2.05,"TECHNICAL HABITS","Pause and clarify. State invariants. Show estimates. Compare alternatives. Admit uncertainty. Invite correction. Summarize risk and recovery.",BLUE,2,14,10.5)
card(slide,8.88,1.62,3.78,2.05,"LOGISTICS","Test camera, microphone, and internet. Use smart casual. Bring concise notes. For onsite, prepare for a focused multi-hour conversation.",PURPLE,3,14,10.5)
add_text(slide,"Questions worth asking",0.78,4.15,2.8,0.32,15,NAVY,True)
questions=[
    "Which accounting workflows create the most manual effort today?",
    "How are provisional insights separated from finalized financial truth?",
    "Where is the boundary between AI recommendation and automatic action?",
    "What would excellent senior data engineering impact look like after 12 months?",
]
for i,q in enumerate(questions):
    add_rect(slide,0.78+(i%2)*6.08,4.65+(i//2)*0.78,5.72,0.58,WHITE,True,LIGHT,0.8)
    add_text(slide,"?",0.94+(i%2)*6.08,4.82+(i//2)*0.78,0.3,0.2,11,ORANGE,True,align=PP_ALIGN.CENTER)
    add_text(slide,q,1.32+(i%2)*6.08,4.76+(i//2)*0.78,4.95,0.28,9.5,DARK)
add_text(slide,"Company details and values on these slides are based on the candidate-guide summary supplied by the user.",1.0,6.62,11.3,0.22,8.5,MID,align=PP_ALIGN.CENTER)

# References
slide = add_slide("Sources, scope, and implementation notes", "This deck is an educational synthesis of the supplied system-design and candidate-prep material.", "References")
add_text(slide,"Primary source",0.75,1.65,2.2,0.3,15,NAVY,True)
add_text(slide,"Afaque Ahmad, “How I Mastered System Design Interviews”\nhttps://www.youtube.com/watch?v=r58Cf_kc_bY",0.78,2.05,11.7,0.7,13,DARK)
add_text(slide,"Scope",0.75,3.05,2.2,0.3,15,NAVY,True)
add_rich_lines(slide,[
    "The six-step framework, examples, timestamps, and initial Delta/Spark snippets came from the user-provided video summary.",
    "The senior data engineering and AI ERP architecture sections are an educational expansion of that supplied material.",
    "Campfire company details, mission, values, and interview expectations are based on the candidate-guide summary supplied by the user and were not independently verified here.",
    "Companion: Campfire_Senior_Data_Engineer_System_Design_QA.docx contains 28 detailed model answers, values guidance, stories, and follow-up questions.",
],0.78,3.48,11.65,2.25,9.8,DARK,True,TEAL,7)
add_callout(slide,"Use the deck for visual practice and the Campfire companion guide for detailed technical, values, and behavioral preparation.",1.0,6.15,11.3,0.7)

# ---------- Plain-language speaker notes ----------
speaker_notes = [
"""Purpose:
Introduce the topic and set expectations for the presentation.

How to explain it:
This presentation is a practical guide for data engineering system design. The goal is not to memorize one architecture. The goal is to learn a repeatable way to take an unclear business problem and turn it into a design that is scalable, reliable, and understandable.

Tell the audience that the deck moves from requirements to architecture, data modeling, storage, quality, and operations. It also includes an end-to-end food-delivery example and working Spark/Delta Lake patterns.

Key takeaway:
Good system design begins with understanding the problem. Technology choices come later.""",

"""Purpose:
Explain what the learner should be able to do after using the deck.

How to explain it:
There are four main skills. First, frame the problem by asking who needs the data and how quickly they need it. Second, estimate the size of the system using simple calculations. Third, choose an architecture by comparing trade-offs instead of choosing favorite tools. Fourth, design for real production conditions such as failures, duplicates, late data, schema changes, and backfills.

Simple example:
A daily finance report and a live fraud alert need very different pipelines even if both use the same source data.

Key takeaway:
A complete answer covers both the normal data flow and how the system behaves when something goes wrong.""",

"""Purpose:
Show that a system design interview tests reasoning, not diagram-drawing skill.

How to explain it:
Every important architecture decision should form a clear chain. Start with a requirement, identify the constraint, make a decision, explain the trade-off, and add a control for the risk.

Use the restaurant dashboard example on the slide. The two-minute freshness requirement leads to streaming. Streaming adds state and operational complexity. Checkpoints, replayable events, monitoring, and a durable lakehouse path control those risks.

Avoid saying only, “I will use Kafka and Spark.” Explain why those components are needed and what disadvantages they introduce.

Key takeaway:
A strong design is a well-supported argument. The diagram is only a visual summary of that argument.""",

"""Purpose:
Introduce the six-step framework used throughout the deck.

How to explain it:
Work through the steps in order. Requirements tell us what success means. Pipeline design decides how data moves and is processed. Data modeling gives the information a useful structure. Storage decisions control durability, cost, and query performance. Quality and observability make the output trustworthy. Operations make the system safe to rerun, scale, and recover.

The process is not completely one-way. If a storage estimate becomes too expensive, we may revisit retention requirements. If a strict latency target is not valuable enough, we may replace streaming with cheaper batch processing.

Key takeaway:
Use the six steps as a checklist so that reliability and operations are not forgotten at the end.""",

"""Purpose:
Provide a simple way to manage time during a 45-minute interview.

How to explain it:
Spend the first few minutes clarifying the problem. Then perform rough sizing calculations. Draw the complete high-level data flow before spending time on details. Deep-dive into the most important components, followed by reliability and scaling. Finish by summarizing trade-offs and open assumptions.

The exact minute values are guidance, not strict rules. The important checkpoint is around minute 20: the interviewer should already understand the end-to-end flow and how it serves the users.

Simple example:
Do not spend 20 minutes choosing Kafka partitions before showing where processed data is stored and how users query it.

Key takeaway:
Breadth first, then depth. Complete the design before optimizing one small area.""",

"""Purpose:
Give a reusable set of questions for requirements gathering.

How to explain it:
Ask WHO consumes the data, WHAT they need, HOW they access it, WHEN it must be available, HOW MUCH data exists, and HOW LONG it must be retained. These questions turn a vague prompt into measurable design inputs.

Write assumptions down when the interviewer does not provide an answer. For example, say, “I will assume the peak load is four times the average and events must be replayable for 30 days.” This makes your reasoning visible and gives the interviewer a chance to correct the assumption.

Key takeaway:
Do not start with tools. First identify the users, outputs, service levels, scale, and constraints that the tools must satisfy.""",

"""Purpose:
Clarify the difference between functional and non-functional requirements.

How to explain it:
Functional requirements describe what the system produces: dashboards, tables, APIs, alerts, or ML features. Non-functional requirements describe how well the system must work: freshness, availability, correctness, security, retention, and cost.

Convert vague statements into measurable targets. “Real time” might mean under two minutes at the 95th percentile. “Reliable” might mean 99.9 percent serving availability with no silent data loss. “Accurate” might mean daily totals reconcile with the source within 0.1 percent.

Simple example:
“Show restaurant sales” is functional. “Refresh within two minutes and remain available during dinner rush” is non-functional.

Key takeaway:
Non-functional requirements usually create the strongest architecture constraints.""",

"""Purpose:
Demonstrate the sizing calculations expected in a data engineering design.

How to explain it:
Start with users and behavior. Five million daily users, two sessions each, and 30 events per session produce 300 million events per day. Divide by 86,400 seconds to get about 3,472 events per second on average. Apply a peak factor; at four times average, plan for about 13,900 events per second.

Next calculate storage. At 700 bytes per event, the raw input is about 210 GB per day and 76.7 TB per year. Compression may reduce this, but replication, table metadata, checkpoints, and derived layers add storage.

Key takeaway:
Show your assumptions and round sensibly. Approximate math is enough when it leads to a clear design decision.""",

"""Purpose:
Connect calculations to actual architecture decisions.

How to explain it:
A number is useful only when it changes the design. Peak events per second influence event-bus partitions and consumer parallelism. Daily bytes influence object storage, file compaction, and incremental processing. High-cardinality or uneven keys can create hot partitions. A two-minute SLA requires continuous processing and a fast serving store. Long retention creates lifecycle and restore requirements.

After every estimate, ask, “What does this number force me to do?” Also ask what must be measured in production, because interview assumptions can be wrong.

Key takeaway:
Translate each estimate into capacity, cost, performance, or reliability consequences. Do not stop after writing the arithmetic.""",

"""Purpose:
Explain how to choose between batch and streaming.

How to explain it:
Start with the freshness requirement. If users can wait hours or a day, batch is usually simpler and cheaper. If they need updates within seconds or minutes, streaming may be required. Then check whether processing is stateful, such as windowed counts, joins, or deduplication. Stateful streaming needs checkpoints, timeouts, watermarks, and careful recovery.

Batch systems still should be incremental. They should process only new or changed partitions rather than rereading all history every time.

Simple example:
A daily executive report fits batch. A dashboard showing active deliveries during dinner rush needs streaming.

Key takeaway:
Choose the simplest processing model that meets the SLA. Streaming is valuable, but it brings additional operational responsibilities.""",

"""Purpose:
Compare batch and streaming in an easy, practical way.

How to explain it:
Batch processes a bounded set of data on a schedule. It is easier to retry and reason about because the input window can be closed. Streaming processes data continuously. It reduces latency but must handle event time, out-of-order arrival, long-running state, checkpoints, and replay.

Many real systems use both. The live path provides recent operational values, while a batch or lakehouse path produces finalized and reconciled history.

When explaining cost, note that batch compute can often turn off after work completes. Streaming infrastructure is normally always running.

Key takeaway:
Different consumers can justify different paths. A hybrid design is reasonable when it avoids forcing one SLA and cost model onto every use case.""",

"""Purpose:
Explain three common architecture styles without treating any one as universally best.

How to explain it:
Lambda has a fast streaming path and a separate batch path. It supports low latency and accurate historical recomputation, but logic can be duplicated. Kappa uses one streaming model and replays retained events when data must be recomputed. It reduces duplicate logic but long replays and stateful processing can be difficult. A lakehouse-centered design stores durable data in object storage with an ACID table format and lets batch and streaming engines work over the same data plane.

Ask two questions: Where is the durable source of truth? How is the system replayed after a bug?

Key takeaway:
Choose an architecture based on the recovery model, operational skills, cost, and SLA—not because a pattern is fashionable.""",

"""Purpose:
Provide a high-level architecture that can be explained from left to right.

How to explain it:
Sources create events, database changes, or files. Ingestion safely receives and buffers the data. Processing validates, transforms, joins, and aggregates it. Storage preserves raw and curated history. Serving systems expose the result to SQL, dashboards, APIs, or machine-learning consumers.

Keep stages decoupled so one stage can slow down or fail without immediately breaking all others. Also mention the cross-cutting capabilities at the bottom: security, metadata, lineage, data quality, observability, cost controls, and deployment automation.

Key takeaway:
First show the complete flow. Then choose one or two critical stages for a deeper technical discussion.""",

"""Purpose:
Explain Bronze, Silver, and Gold as clear data contracts.

How to explain it:
Bronze preserves source data and ingestion metadata. Its main purpose is recoverability, so avoid destructive cleaning here. Silver converts raw data into trusted, reusable entities by parsing, casting, deduplicating, and enforcing important rules. Gold provides business-ready products such as stable metrics, aggregates, and consumer-specific tables.

A record that cannot be parsed should normally be retained or quarantined rather than silently dropped. Gold changes should be carefully versioned because dashboards and other consumers may depend on exact names and meanings.

Key takeaway:
Bronze lets us rebuild. Silver gives shared truth. Gold gives consumers an understandable and stable business interface.""",

"""Purpose:
Show how to begin dimensional modeling with the table grain.

How to explain it:
The grain states exactly what one row represents. In this example, one fact-table row represents one lifecycle event for one order. Measures such as amount or duration belong in the fact. Descriptive context, such as customer segment, restaurant cuisine, date, and location, belongs in dimensions.

After defining grain, identify keys, dimensions, and measures. Then discuss late-arriving facts and dimension history. A fact must join to the dimension version that was valid when the event happened, not necessarily the current version.

Key takeaway:
Always state the grain before listing columns. An unclear grain causes duplicates, incorrect totals, and confusing joins.""",

"""Purpose:
Compare common analytical modeling choices.

How to explain it:
A star schema is a strong default for governed business intelligence because facts and dimensions make grain and reuse clear. A snowflake normalizes dimensions further, reducing duplication but adding joins and user complexity. A one-big-table model can simplify a specific query path but duplicates data and becomes harder to update consistently. Data Vault is useful when auditability and source-history integration are major goals, but business-facing marts are still normally required.

State both your default and the condition that would make you switch.

Simple example:
Use a star for shared sales reporting. Build a carefully managed wide table only if a proven high-volume dashboard benefits from avoiding repeated joins.

Key takeaway:
The model should match consumer access patterns and governance needs.""",

"""Purpose:
Explain how dimension changes can be stored over time.

How to explain it:
SCD Type 1 overwrites the old value. Use it when history is not needed, such as correcting a spelling error. SCD Type 2 inserts a new version and keeps effective start and end dates. Use it when historical reporting must show the value that was true at that time. SCD Type 3 stores only limited previous information in extra columns.

In the sample table, customer C55 changed from SILVER to GOLD. The old row is closed and a new current row is added. Prevent overlapping date ranges and define how late events find the correct version.

Key takeaway:
Choose history behavior by business meaning. Not every attribute needs the same SCD strategy.""",

"""Purpose:
Distinguish file serialization formats from analytical table formats.

How to explain it:
CSV and JSON are easy to exchange and inspect but are large and weakly typed. Avro is row-oriented and well suited to serializing individual records on event systems. Parquet and ORC are columnar, so analytical engines can read only needed columns and apply compression efficiently. Delta Lake and Iceberg are table layers over data files; they add snapshots, metadata, schema management, and transactional behavior.

A common design uses Avro or Protobuf for events and Parquet files managed by a Delta or Iceberg table for analytics.

Key takeaway:
Choose the event format for safe record exchange, the file format for efficient storage, and the table format for reliable table operations.""",

"""Purpose:
Explain how physical data layout affects query performance and cost.

How to explain it:
Partitioning separates data into directories or logical groups that can be skipped during a query. Date is often useful because many queries filter by time. Avoid very high-cardinality partition columns because they create too many small partitions and files. Clustering or sorting can place similar values together without a huge directory structure. Compaction combines small files, improving listing and read efficiency. Metadata maintenance removes old snapshots only after replay and time-travel requirements are considered.

Walk through the read path: partition pruning, file skipping, column pruning, and decompression.

Key takeaway:
Design layout from real filter patterns and file sizes. More partitions do not automatically mean faster queries.""",

"""Purpose:
Show that data quality rules should become stricter as data moves toward consumers.

How to explain it:
Bronze checks whether data can be ingested and replayed. Record parse failures and source counts, and quarantine malformed data. Silver checks whether entities are trustworthy by enforcing types, uniqueness, valid values, references, and freshness. Gold checks business meaning by reconciling metrics, validating business rules, and protecting consumer SLAs.

Every check needs an owner, threshold, and action. Decide whether failure should alert, quarantine records, stop a pipeline, or hold publication. Silent failure is the most dangerous outcome.

Key takeaway:
Quality is not one test at the end. It is a set of controls applied at the right layer with a clear response.""",

"""Purpose:
Explain how data contracts prevent downstream surprises.

How to explain it:
A contract describes structure, meaning, service levels, ownership, and change policy. Schema includes field names, data types, and nullability. Semantics explain what the fields and events mean. SLOs define freshness and availability. Ownership identifies who approves changes and responds to incidents.

A schema registry helps enforce structural compatibility, but it is only part of a full contract. For a breaking change, publish a new version, allow old and new versions to run together, measure migration, and retire the old version only after consumers move.

Key takeaway:
Data contracts move quality checks closer to the producer, where problems are cheaper and easier to correct.""",

"""Purpose:
Explain what must be monitored in a production data platform.

How to explain it:
Data telemetry measures freshness, volume, duplicates, and distribution changes. Pipeline telemetry measures job duration, event lag, watermarks, retries, and dead-letter volume. Platform telemetry measures CPU, memory, disk, shuffle, checkpoints, and service quotas. Business telemetry checks whether important numbers, such as orders or revenue, still make sense.

Alerts should describe user impact and point to an owner and runbook. Include lineage, affected partitions, recent deployments, and recovery steps so an engineer can act quickly.

Key takeaway:
Observability should answer three questions: What is wrong? Who is affected? What should we do next?""",

"""Purpose:
Explain idempotency as more than a single write command.

How to explain it:
Idempotency means repeating the same logical work produces the same visible result. It requires a stable event or business key, deterministic transformations, an atomic write, durable progress tracking, safe retries, and reconciliation.

A message system may deliver an event more than once. That is acceptable if the target uses the event identity to deduplicate or upsert so the final table contains one correct record. Do not record source progress before the output commit succeeds, or the system may skip data after a failure.

Key takeaway:
Design the rerun path before the first run. A pipeline is not idempotent merely because one component claims exactly-once behavior.""",

"""Purpose:
Walk through an idempotent Delta Lake batch upsert.

How to explain it:
The code first defines a compound key using order ID and event timestamp. A window keeps only the newest source row for each key. This source deduplication matters because multiple source rows matching one target row can make a merge ambiguous or incorrect.

The MERGE updates an existing record only when the incoming updated_at value is at least as recent as the target. Otherwise, it inserts a new record. Delta commits the change atomically, so readers do not see a partially updated table.

Mention remaining decisions: deletion behavior, null-safe keys, concurrent writers, and count reconciliation.

Key takeaway:
A safe MERGE needs a correct key, one source winner per key, deterministic update rules, and an atomic target commit.""",

"""Purpose:
Explain a safe method for reprocessing historical data.

How to explain it:
A backfill should use immutable Bronze input and the same transformation logic as the normal pipeline. Select a bounded date range, rebuild the Silver output, and validate row counts, checksums, and business totals. Then use replaceWhere to atomically replace only that date range.

Keep the run ID, code version, date range, and validation results for audit. Ensure every output record satisfies the replacement predicate so records are not accidentally written outside the intended range. Coordinate downstream refreshes because replacing history can change dashboards and aggregates.

Key takeaway:
Backfills are planned production operations, not manual one-off scripts. Scope, validate, publish atomically, and record what changed.""",

"""Purpose:
Explain how to make a Spark Structured Streaming output idempotent.

How to explain it:
The stream uses a durable checkpoint to track source progress and calls foreachBatch for each micro-batch. Inside the function, records are deduplicated and merged using a stable event ID. If the batch is attempted again, the deterministic MERGE produces the same table outcome.

The note on the right corrects an important API issue. Transaction options such as txnAppId and txnVersion are not normally chained onto DeltaMergeBuilder. For MERGE, rely on checkpointed input progress and idempotent merge logic. A batch ID can also be recorded in an audit ledger.

Key takeaway:
A checkpoint controls progress. The merge key and update rules control the final table result. Both are required.""",

"""Purpose:
Present a safe strategy for handling changing source schemas.

How to explain it:
Bronze should be resilient. Keep the raw payload, schema identifier, ingest timestamp, and unexpected fields so data is not lost. Silver should be explicit: cast expected types, apply defaults, quarantine invalid records, and test compatibility. Gold should be stable because dashboards and applications depend on its names and meanings.

Additive nullable fields are often backward-compatible. Renames, removals, type changes, and semantic changes normally require versioning and migration. Even when a platform can merge schemas automatically, the organization still needs a change policy.

Key takeaway:
Be permissive at the edge so data survives, but strict at the trusted and business-facing layers so consumers are protected.""",

"""Purpose:
Show practical code for controlled schema evolution.

How to explain it:
The Bronze example uses a rescued-data column to capture fields that do not match the known schema. This prevents unexpected data from disappearing and allows the team to investigate drift. The Silver example first validates required columns and compatible types. Only then does it enable mergeSchema for an approved additive change.

Avoid enabling global automatic schema merge as a convenience. It may allow surprising or weakly related data into important tables. Use a production gate: compatibility test, owner approval, migration plan, consumer validation, rollout, and drift monitoring.

Key takeaway:
Automatic schema capability is a tool, not a governance policy. Validate and approve changes before trusted layers evolve.""",

"""Purpose:
Explain how the system handles failures, disaster recovery, and major growth.

How to explain it:
For each failure, name four things: the failure domain, detection signal, recovery action, and possible data-loss boundary. Consumer crashes need durable checkpoints. Poison records need quarantine and replay. Regional outages need replicated data and tested failover. Ten-times traffic needs partition and consumer scaling plus hot-key analysis. Bad deployments need versioning and rollback. Corrupt output needs snapshots and rebuild from Bronze.

RPO is the maximum acceptable data loss. RTO is the maximum acceptable recovery time. Product features do not prove these targets; recovery drills do.

Key takeaway:
A reliable design includes a tested recovery story for the most important failure modes.""",

"""Purpose:
Introduce the end-to-end food-delivery design problem and quantify it.

How to explain it:
There are two consumers. Restaurant partners need operational metrics in under two minutes. Executives need accurate daily history. Five million orders with six lifecycle events produce 30 million events per day. This is about 350 events per second on average, with a supplied peak of about 833 events per second. Raw data is roughly 30 GB per day at one KB per event.

Challenge assumptions politely. The stated peak is only about 2.4 times the average, so promotions, regional concentration, retries, and future growth may require more headroom.

Key takeaway:
Different SLAs justify different serving paths, while durable raw data provides one foundation for replay and reconciliation.""",

"""Purpose:
Walk through the proposed food-delivery architecture from source to consumer.

How to explain it:
Order services publish lifecycle events to Kafka using order ID as the key to preserve per-order ordering. The streaming path parses, validates, deduplicates, and calculates recent metrics. It writes live values to Redis or a low-latency OLAP store for restaurant dashboards.

At the same time, raw events land in Bronze. Silver creates clean, conformed entities, and Gold creates finalized business metrics for executive reporting. The lakehouse path provides history, backfills, and reconciliation when late events revise live values.

Mention the cross-cutting controls: contracts, catalog, lineage, quality, monitoring, checkpoints, replay, and access control.

Key takeaway:
The live path serves speed; the lakehouse path provides durability, correctness, and historical reproducibility.""",

"""Purpose:
Demonstrate that the design handles more than the happy path.

How to explain it:
Trace six scenarios. A normal event flows through validation, streaming, serving, and Bronze archival. A late event uses event time and may revise a recent window. Duplicate delivery is controlled by the event key and idempotent MERGE. A bad schema is blocked or quarantined. A backfill rebuilds bounded history from Bronze and publishes atomically. A ten-times traffic spike is handled with more partitions and consumers, while stale-but-labeled data can provide graceful degradation.

Use one event as a test: can it be traced, replayed, and explained without creating a duplicate?

Key takeaway:
A credible architecture explains normal flow, late data, duplicates, failure, replay, and scaling.""",

"""Purpose:
Give the presenter a simple sentence pattern for explaining decisions.

How to explain it:
For every major choice, say: Because of this requirement, I choose this component or pattern. This provides a benefit. It also creates a cost or risk. I control that risk with a specific mitigation.

Use the worked example. A two-minute SLA leads to streaming. Streaming gives continuous updates but adds state and always-on operations. Bounded windows, checkpoints, lag alerts, retained events, and lakehouse reconciliation reduce those risks.

This format prevents a tool-list answer and makes trade-offs visible. Also say what is intentionally out of scope until the interviewer asks.

Key takeaway:
Requirement, decision, benefit, cost, mitigation—repeat this structure throughout the interview.""",

"""Purpose:
Provide a final completeness check for a design answer.

How to explain it:
Review six categories. Requirements should name users, outputs, measurable SLOs, retention, and security. Scale should cover average and peak throughput, storage, growth, and skew. Architecture should show the complete flow and explain batch or streaming. Data design should state grain, keys, model, format, and layout. Reliability should cover quality, replay, idempotency, backfills, schema change, and disaster recovery. Trade-offs should include cost, complexity, bottlenecks, and alternatives.

If an item is unknown, do not hide it. State it as an assumption or open question and describe how you would validate it.

Key takeaway:
A transparent gap is better than an unsupported claim.""",

"""Purpose:
Offer a one-page template that can be copied onto a whiteboard.

How to explain it:
Create six areas before solving the prompt. Write users and outputs first. Add service levels and constraints. Perform scale calculations. Draw the complete data flow. Define data grain, keys, models, formats, and layout. Finally, add operational controls such as quality, monitoring, replay, backfills, schema evolution, and disaster recovery.

At the end, identify the likely bottleneck at ten-times scale, the largest correctness risk, the largest cost driver, an alternative architecture, and any unresolved assumptions.

Key takeaway:
The template keeps the discussion organized and prevents important production topics from being forgotten.""",

"""Purpose:
Summarize the most important lessons from the presentation.

How to explain it:
Begin with users and measurable service levels. Estimate peak load and storage before choosing technology. Prefer the simplest architecture that satisfies the requirement. Define data grain, history, schema contracts, and access patterns. Plan reruns, replay, backfills, and migrations as normal system behavior. Explain every trade-off using a requirement and a mitigation.

Remind the audience that complexity is not a sign of quality. A smaller batch architecture can be the best answer for a daily report. A streaming architecture is justified only when its lower latency creates real business value.

Key takeaway:
The best design is understandable, measurable, recoverable, and no more complicated than necessary.""",

"""Purpose:
Identify the source and explain how to use the material responsibly.

How to explain it:
The deck is based on the user-provided summary of Afaque Ahmad's video and expands it into a reusable teaching and interview framework. The technology names are examples, not fixed recommendations. Exact APIs, feature support, and operational behavior can vary by platform and version, so implementation details should be checked in the target environment.

The streaming idempotency section intentionally corrects the supplied example that attached transaction options to a Delta MERGE builder. The deck uses checkpointed progress plus deterministic MERGE logic as the main pattern.

Key takeaway:
Use the framework consistently, but replace assumptions and technologies according to the real users, cloud, team, compliance rules, and workload.""",
]

# Add an AI-ERP interpretation to every original slide's notes.
base_erp_relevance = [
    "For an AI ERP company, this framework connects systems of record such as finance, HR, procurement, and inventory to analytics, forecasting, copilots, and controlled automation.",
    "Apply the four skills to ERP by clarifying each module and persona, sizing both tenant-fleet and largest-tenant load, and treating financial correctness and tenant isolation as design invariants.",
    "An ERP answer should explicitly connect a business requirement such as month-end finality or payroll confidentiality to architecture, trade-offs, and controls.",
    "Use the six steps for both the data platform and the AI feature: requirements, movement, semantic model, storage/index, quality/evaluation, and operations/governance.",
    "In an ERP interview, reserve time to discuss ledger reconciliation, tenant isolation, authorization-aware AI retrieval, and human approval for write-back actions.",
    "Add ERP questions: which modules, legal entities, currencies, fiscal calendars, tenant tiers, user roles, and regulated fields are in scope?",
    "ERP non-functional requirements include balanced accounting, closed-period immutability, payroll privacy, tenant-level availability, data residency, and explainable AI outputs.",
    "Repeat the sizing at two levels: total SaaS fleet and largest tenant. Include month-end bursts, document volume, CDC record size, and vector-index growth.",
    "For ERP, estimates should influence tenant quotas, hot-ledger partitioning, close-period capacity, cache isolation, index sharding, and per-tenant cost attribution.",
    "ERP often needs streaming for inventory and operations, while financial close and regulatory outputs use controlled batch finalization and reconciliation.",
    "Use streaming for named operational needs, but retain a durable batch/lakehouse path to restate periods and reproduce reports as of a prior close.",
    "A lakehouse-centered pattern is useful for shared governed ERP history, while specialized streaming, warehouse, feature, and vector stores serve distinct workloads.",
    "In the ERP version, sources are transactional modules and documents; serving includes BI, forecasts, anomaly detection, copilots, and approval-based actions.",
    "ERP Bronze should preserve CDC order and tenant identity; Silver should create canonical parties, transactions, resources, and ledgers; Gold should expose governed measures.",
    "State ERP grain precisely: one journal line, invoice line, inventory movement, employee event, or order status change. Mixing grains creates incorrect balances.",
    "A star schema is strong for finance and operations BI; a canonical integration model can feed it; wide tables should be limited to proven tenant-safe serving paths.",
    "ERP dimensions such as employee, supplier, chart of accounts, cost center, and legal entity often require SCD2 history for correct as-of reporting.",
    "ERP CDC events may use Avro/Protobuf; analytical history may use Parquet with Delta/Iceberg; contracts and version compatibility matter across tenant customizations.",
    "Partition first by access and scale needs, often date plus a carefully chosen tenant/legal-entity strategy; prevent one large tenant from creating hot files or partitions.",
    "Add ERP invariants such as debit equals credit, invoice totals equal lines plus tax, valid accounting periods, inventory cannot silently disappear, and tenant IDs are complete.",
    "ERP contracts must define business meaning as well as types—for example currency units, sign conventions, fiscal period, source module, and whether an amount is posted or provisional.",
    "Monitor ERP outcomes per tenant: CDC lag, close freshness, reconciliation differences, policy denials, retrieval quality, model drift, and cost by workload.",
    "ERP idempotency must cover journal postings and AI-initiated actions. Use business transaction IDs and approval/action IDs so retries cannot double-post.",
    "For ERP MERGE keys, include tenant identity and the true business grain. Never let records from different tenants collide on a shared order or invoice ID.",
    "ERP backfills should respect closed periods, tenant maintenance windows, regulatory retention, downstream consolidations, and a formal restatement/audit process.",
    "A streaming ERP pipeline should preserve source transaction order, checkpoint offsets, deduplicate by tenant plus source identity, and reconcile against module control totals.",
    "Tenant custom fields make schema governance critical: keep a stable core, capture extensions safely, and promote only approved fields into shared semantic products.",
    "Use rescued data for observation, not as a permanent substitute for contracts. ERP schema changes should pass module-owner, data, security, and downstream compatibility checks.",
    "ERP disaster recovery should classify source ledgers and audit evidence as higher priority than rebuildable dashboards, features, embeddings, and predictions.",
    "Treat the food-delivery example as an operational ERP analogy: replace restaurants with tenants or business units and orders with invoices, shipments, or work orders.",
    "For AI ERP, extend the architecture with tenant policy enforcement, canonical business semantics, feature/model lineage, and permission-filtered document retrieval.",
    "Add ERP failure scenarios: late journal corrections, reopened periods, tenant key rotation, role changes during cached AI sessions, and partial multi-module transactions.",
    "A strong ERP narration begins with invariants such as tenant isolation and financial balance before naming Kafka, Spark, a lakehouse, a vector store, or an LLM.",
    "Use this scorecard per ERP workload and per AI use case; a platform can meet dashboard SLAs while failing authorization, auditability, or financial finality.",
    "Add three boxes to the template when needed: tenant-isolation model, business invariants, and AI authorization/evaluation/write-back controls.",
    "For AI ERP, the simplest acceptable design must still preserve transactional truth, tenant boundaries, semantic consistency, evidence, and safe human-controlled actions.",
    "The AI ERP extension is an applied design framework. Exact isolation, retention, model, and service choices must be validated against the company's products and regulations.",
]

if len(base_erp_relevance) != 37 or len(speaker_notes) != 37:
    raise ValueError("Expected 37 original notes and ERP relevance entries")

base_notes = [
    f"{note}\n\nAI ERP relevance:\n{relevance}"
    for note, relevance in zip(speaker_notes, base_erp_relevance)
]

ai_erp_notes = [
"""Purpose:
Explain why an AI-powered ERP platform is a harder design problem than a standard analytics pipeline.

How to explain it:
ERP is a system of record. Incorrect or missing transactions can change financial statements, payroll, tax, inventory, or customer commitments. It is also multi-tenant SaaS, so one customer's data must never appear in another customer's query, cache, model context, vector result, trace, or support workflow. Operational users need fresh data, while auditors need reproducible history. AI copilots add retrieval, model, evaluation, and action-control requirements.

Describe the four pillars together. Transactional truth supplies trusted facts. Tenant isolation controls every data path. Operational analytics provides timely decisions. AI copilots use governed context and should cite evidence or abstain.

Key takeaway:
An AI ERP design is not just a lakehouse plus an LLM. It is a governed connection from authoritative transactions to permission-aware decisions and actions.""",

"""Purpose:
Show that an AI ERP platform contains several workloads with different service levels.

How to explain it:
Financial close values correctness, restatement, and audit evidence more than second-level latency. Operations dashboards need low CDC lag and predictable serving performance. Forecasting requires reproducible point-in-time features rather than only current values. A copilot needs interactive response time, but it also needs authorized, fresh, cited evidence. Audit workloads may run infrequently but require long retention and immutable lineage.

Do not put every workload into one database. Use shared canonical data, governance, tenant identity, and metrics, then choose a warehouse, operational OLAP store, feature store, vector index, or archive according to the access pattern.

Key takeaway:
Shared truth does not require one serving technology. Match each workload to its latency, consistency, query, and isolation needs.""",

"""Purpose:
Present an end-to-end reference architecture for ERP data, analytics, machine learning, and copilots.

How to explain it:
Transactional ERP modules emit CDC records and domain events with source offsets, transaction IDs, schemas, and tenant identity. Documents use a separate OCR and parsing path. Bronze preserves original changes and files. Silver maps module-specific records into canonical ERP entities. Gold supplies governed measures and features.

The semantic layer serves finance and operations BI. The feature store supports reproducible model training and scoring. The vector index contains document chunks and metadata with mandatory tenant and ACL filters. An AI gateway performs authorization, retrieval, prompt controls, citation, caching, and audit before the copilot responds or proposes an action.

Cross-cutting controls must follow the data across every plane.

Key takeaway:
Keep transactional authority, analytical truth, and AI serving separate, but connect them with identity, semantics, lineage, and policy.""",

"""Purpose:
Explain the main multi-tenant storage and compute isolation choices.

How to explain it:
Shared tables are efficient for many small tenants, but every key and query must include tenant identity and policy enforcement must be extensively tested. A schema or database per tenant offers clearer restoration and logical boundaries, but migrations and metadata become expensive at large scale. A dedicated stack provides strongest separation for regulated or very large customers, at higher cost. Many ERP companies use a tiered hybrid and route tenants by size, risk, geography, or contract.

Isolation also applies outside tables. Include encryption keys, object paths, checkpoints, caches, temporary files, model features, prompt traces, vector namespaces, observability tags, and support access. Add per-tenant quotas and fair scheduling to control noisy neighbors.

Key takeaway:
Multi-tenancy is not a WHERE clause. Tenant identity and policy must be impossible to omit at every boundary.""",

"""Purpose:
Explain how CDC becomes financially correct analytical data.

How to explain it:
The database transaction log provides ordered technical changes, but financial meaning comes from business transactions and accounting rules. Capture source transaction ID, row identity, operation, LSN or offset, commit time, tenant, legal entity, and schema version. Preserve raw before/after images. Build canonical ledger lines by deduplicating and applying changes in source order.

Create an atomic relationship between consumed source range and target commit. A retry must merge to the same result. Then validate accounting invariants, such as debit equals credit, and reconcile source counts and control totals. Corrections to closed periods should be explicit reversals or adjustment versions, not destructive overwrites.

Key takeaway:
Exactly-once reporting is proved by identity, ordering, idempotent writes, atomic progress, invariants, and reconciliation—not by the CDC tool alone.""",

"""Purpose:
Connect a canonical ERP model to secure AI retrieval.

How to explain it:
ERP modules use different names for similar concepts. A canonical model gives stable identities and relationships for parties, legal entities, transactions, resources, and accounting. A governed semantic layer defines measures such as booked revenue, available inventory, or overdue receivables consistently.

For an AI question, first establish tenant, user, role, purpose, and current entitlements. Retrieve structured facts through governed SQL and unstructured evidence through a vector or search index. Apply row, field, document, and effective-time policy before context reaches the model. Include source, time, currency, and freshness metadata. The answer should cite evidence and abstain when the available context is incomplete.

Key takeaway:
The copilot should inherit ERP semantics and authorization. Retrieval must not create a second, weaker security model.""",

"""Purpose:
Show how data governance extends across the complete AI lifecycle.

How to explain it:
At ingest, classify data, validate contracts, and record consent or purpose restrictions. During curation, preserve lineage and construct point-in-time-correct data. During training or indexing, record dataset snapshots, feature definitions, model or embedding versions, parameters, and evaluation sets. At serving, record tenant policy, retrieved evidence, prompt template, model, cache behavior, and response. Evaluate groundedness, business accuracy, fairness, drift, and abstention.

For write-back, treat the LLM as an untrusted planner. Convert the proposal into a typed command, validate ERP rules, require human approval according to risk, attach an idempotency key, and log before/after state. Support rollback or compensating action.

Key takeaway:
An AI ERP company must trace an answer or action from source evidence through policy and model version to the final outcome.""",

"""Purpose:
Demonstrate tenant-aware sizing and resilience planning for an ERP SaaS fleet.

How to explain it:
The example assumes 8,000 tenants generating an average of 250,000 changes each day, or about two billion changes. This is roughly 23,000 changes per second on average. A six-times month-end peak requires about 139,000 changes per second before extra headroom. At 1.2 KB per change, raw volume is around 2.4 TB per day.

Fleet average is not enough. One large tenant or legal entity can dominate a partition during close. Plan buffering, pre-scaling, tenant quotas, weighted scheduling, and hot-key splitting. Define separate recovery tiers: source ledgers and audit evidence need stronger RPO/RTO than rebuildable aggregates, features, embeddings, and predictions.

Key takeaway:
Size for total fleet, peak calendar events, and largest tenant. Protect critical truth more strongly than derived AI assets.""",

"""Purpose:
Give a repeatable method for answering an AI ERP system-design question.

How to explain it:
First clarify modules and users. Then state non-negotiable invariants: tenant isolation, balanced accounting, as-of correctness, authorization, and audit. Define service levels for CDC, report finality, AI response time, and recovery. Size both fleet and largest tenant. Draw three connected planes: transactional, analytical, and AI serving. Explain the canonical model and metric semantics. Prove replay, reconciliation, backfill, and schema migration. Finally prove AI authorization, grounding, evaluation, approval, idempotent action, and audit.

Close by naming the hardest trade-off. For example, low latency may expose provisional values, so label them and run a finalized reconciled path.

Key takeaway:
Lead with business invariants and risks, then justify technology as a way to satisfy them.""",

"""Purpose:
Provide deeper model answers for complex questions 1 through 4.

1. Near-real-time analytics for 10,000 tenants:
Clarify tenant sizes, modules, regions, freshness, and query patterns. Capture CDC into a partitioned durable log carrying tenant and source identity. Land immutable Bronze, create canonical Silver, and publish tenant-aware Gold. Use a low-latency OLAP store for live operations and a warehouse/lakehouse for governed history. Enforce row/field policy, per-tenant quotas, lag SLOs, cost attribution, and dedicated tiers for regulated or very large customers. Test noisy-neighbor and cross-tenant access failures.

2. Exactly-once financial reporting:
Preserve source transaction ID, row ID, LSN, commit order, tenant, and legal entity. Deduplicate and MERGE using source identity; commit consumed ranges with target versions. Do not publish a period until debit/credit and source control totals reconcile. Keep correction and restatement lineage. Explain that transport may be at-least-once while the business result is idempotent and reconciled.

3. Tenant custom fields:
Keep a stable shared core. Capture extensions in a typed key/value, JSON/variant, or tenant extension structure with schema metadata. Validate per-tenant contracts and index only commonly queried fields. Promote a custom field to a governed column only after ownership, type, meaning, and usage justify it. Prevent per-tenant columns from exploding shared-table schemas.

4. Closed-period corrections:
Do not overwrite history. Post a reversal or adjustment, keep effective and recorded times, version as-of facts, and rebuild only affected tenant/entity/period aggregates. Require approval, record reason and actor, preserve old report versions, and notify downstream consumers of restatement.

Key takeaway:
Strong ERP answers combine tenant boundaries, source identity, business invariants, controlled extensibility, and auditable correction.""",

"""Purpose:
Provide deeper model answers for complex questions 5 through 8.

5. ERP copilot over tables and documents:
Use an AI gateway. Authenticate tenant/user/purpose, resolve entitlements, classify the question, and retrieve structured facts through the semantic layer plus document chunks through hybrid search. Filter before model context, include freshness and citations, and prefer deterministic tools for calculations. The model should abstain or ask for clarification when evidence conflicts. Log evidence IDs and model/prompt versions.

6. Prevent cross-tenant RAG leakage:
Use physically separate indexes for high-risk tenants or mandatory tenant namespaces and filters for shared indexes. Copy ACLs and effective dates to every chunk. Encrypt, use tenant-aware caches, and never trust an LLM to enforce policy. Add policy-as-code, negative authorization tests, adversarial prompts, canaries, redacted traces, and incident kill switches.

7. Forecast features without leakage:
Define event time and availability time. Build training rows using point-in-time joins so no feature uses information known after the prediction timestamp. Version feature code, source snapshots, labels, and fiscal calendars. Compare offline and online feature values, monitor skew, and support reproducible retraining by tenant cohort.

8. Trustworthy AI evaluation:
Measure retrieval recall, citation support, groundedness, calculation/business-rule accuracy, freshness, permission correctness, abstention, latency, and cost. Evaluate by module, tenant tier, language, role, and risk. Use curated test cases plus production feedback and shadow evaluation. A fluent answer with unsupported numbers must fail.

Key takeaway:
AI quality in ERP includes authorization and business correctness, not only natural-language quality.""",

"""Purpose:
Provide deeper model answers for complex questions 9 through 12.

9. Privacy deletion with audit retention:
Classify personal fields and identify legal basis per product and region. Separate business transaction evidence from direct identity where possible and tokenize or pseudonymize identifiers. Delete or tombstone permitted data in source, lakehouse, warehouse, feature store, vector index, caches, logs, and training queues. Preserve only legally required evidence under restricted purpose and legal hold. Maintain a deletion manifest and verify completion.

10. Two-year backfill without live impact:
Read immutable snapshots using a versioned transformation. Run isolated compute with quotas and lower-priority scheduling. Break work into resumable tenant/date manifests, handle skewed tenants separately, and publish partitions incrementally after quality and financial control-total validation. Record code/input/output versions and coordinate restatements. Throttle if CDC lag or serving SLOs degrade.

11. Ten-times month-end spike:
Pre-scale based on fiscal calendars, retain enough log capacity, increase consumers, and remove tenant/legal-entity hot keys. Apply weighted fair scheduling and prioritize ledger ingestion and close-critical outputs over secondary AI indexing. Use backpressure and display labeled stale analytics rather than dropping data. Load-test with the largest tenant and correlated closes.

12. Regional outage with residency:
Classify data by residency and criticality. Replicate only allowed data to an approved paired region; replicate code, schemas, catalog, policies, keys, and checkpoints appropriately. Define RPO/RTO separately for transactions, analytics, and rebuildable AI indexes. Use DNS/routing and controlled failover, reconcile after recovery, and exercise the runbook regularly.

Key takeaway:
Privacy, backfills, peak events, and disaster recovery require explicit scope, prioritization, audit evidence, and tested operational procedures.""",
]

# Two senior-level deep-dive slides are inserted after the general reference architecture.
new_general_notes = [
"""Purpose:
Explain the senior-level decisions behind an event-ingestion backbone.

How to explain it:
Begin with identity and ordering, not partition count. Every event needs a stable event ID and source identity so consumers can safely process duplicate delivery. Define the smallest business scope that requires order. An order may require lifecycle order; a financial ledger may require tenant plus legal entity plus ledger order. Global ordering is usually unnecessary and limits scale.

Choose a partition key that preserves the required local order while distributing peak traffic. Measure the largest key and tenant because fleet averages can hide a hot partition. If a key is too hot, sub-shard only when the business can tolerate independent order across shards. Size the event service using measured bytes and records per partition, consumer capacity, desired backlog-drain time, replay retention, and service quotas.

For AI ERP, the envelope must carry tenant, aggregate, source transaction or LSN, occurred and produced time, schema version, and trace identity. Downstream files and state should retain that lineage.

Key takeaway:
Partitioning encodes ordering, parallelism, tenant fairness, and recovery. It cannot be selected from throughput alone.""",

"""Purpose:
Explain how to select serving technologies for BI, applications, machine learning, and ERP copilots.

How to explain it:
Start with query shape and latency. BI and finance use scans, joins, governed measures, and concurrency, so a warehouse, lakehouse SQL engine, or OLAP system may fit. Operational dashboards need fast recent aggregates and controlled updates. Application APIs need predictable point or range access. Machine learning needs reproducible offline features and sometimes low-latency online values. An ERP copilot needs authorized structured queries plus permission-filtered document retrieval.

Every serving copy needs a refresh and correction method, freshness indicator, authorization policy, reconciliation with durable truth, and fallback when stale or unavailable. Cache keys must include tenant and entitlement context. Add a new store only when its access pattern justifies the synchronization and operating cost.

Key takeaway:
Share governed data and semantics, but choose serving systems by access pattern. One physical store rarely satisfies every workload well.""",
]

campfire_notes = [
"""Purpose:
Frame the interview around Campfire's stated mission and values from the candidate-guide summary.

How to explain it:
Campfire is described as an AI-native ERP that aims to give accounting and finance teams superpowers by reducing repetitive work and providing timely financial insight. Translate that mission into engineering priorities: trustworthy financial data, automation that users can understand and control, responsive customer experiences, and fast iteration without compromising accounting correctness.

In the conversation, demonstrate transparent accountability by stating assumptions and risks directly. Show customer-centric innovation by beginning with an accountant's workflow and measurable outcome. Show low ego and growth mindset by comparing alternatives and changing direction when evidence is better. Show quality with velocity through small releases, automated gates, canaries, and rollback. Show collaborative excellence by including accounting, product, security, and engineering ownership.

Key takeaway:
Do not merely repeat company values. Make them visible in how you clarify, design, communicate trade-offs, and discuss mistakes.""",

"""Purpose:
Connect data engineering capabilities to practical customer outcomes for finance teams.

How to explain it:
Faster close requires timely ingestion, clear exception queues, reconciliation, reproducible period snapshots, and restatement history. Reducing manual work requires safe document extraction, matching, coding recommendations, approval workflows, and idempotent actions. Real-time intelligence requires governed measures with freshness and finality indicators. Trusted AI requires permission-aware retrieval, citations, evaluation, and human control.

For each capability, name the user and pain before the technology. For example: a controller spends hours finding an unexplained variance; lineage and exception prioritization reduce investigation time. Explain the financial invariant that cannot be sacrificed and the smallest safe release that proves value.

Key takeaway:
The strongest Campfire answer turns architecture into an outcome: fewer manual steps, faster close, better explanations, or higher financial confidence.""",

"""Purpose:
Show a reference architecture for AI-native financial intelligence and automation.

How to explain it:
Financial systems emit ordered CDC and domain events; documents use OCR and extraction. Bronze retains immutable evidence. Silver creates canonical finance entities. Gold exposes governed metrics. An audit ledger records versions, approvals, and actions.

The semantic layer ensures reports and AI use the same definitions. Features and models support forecasting and anomaly detection. Secure retrieval combines authorized structured data and documents. User experiences include close workflows, intelligence, and a copilot. Any proposed write-back becomes a typed command that passes accounting rules, authorization, approval, idempotency, and audit before posting.

Follow tenant identity, source transaction, time, schema, and policy through every arrow. Explain provisional versus finalized outputs and how corrections are replayed.

Key takeaway:
Transactional authority, analytical truth, and AI automation remain separate responsibilities connected by semantics, lineage, policy, and reconciliation.""",

"""Purpose:
Make the non-negotiable controls explicit before discussing speed or convenience.

How to explain it:
Financial controls prove that journals balance, source totals reconcile, closed periods are not silently rewritten, and every published measure has a cutoff and lineage. Tenant controls ensure customer identity and authorization are present in tables, object paths, caches, indexes, prompts, traces, and support tools. AI controls treat the model as an untrusted planner: output is typed, validated, approved according to risk, idempotent, and audited.

Quality with velocity means automating these controls. A canary tenant, contract tests, reconciliation gates, feature flags, and quick rollback let the team ship faster because risk is visible and bounded.

Key takeaway:
Move quickly by making critical controls automatic and repeatable, not by bypassing them.""",

"""Purpose:
Provide a Campfire-relevant system-design prompt and a clear answer structure.

How to explain it:
Clarify controllers and accountants, live exceptions versus finalized close, legal entities, currencies, fiscal calendars, and restatement behavior. Estimate tenants, largest tenant, journal lines, month-end concentration, document volume, and retention. Draw ordered CDC and document ingestion into immutable evidence, canonical finance models, reconciled metrics, and authorized experiences.

Prove tenant isolation, balanced accounting, source reconciliation, idempotent replay, versioned close snapshots, and cited AI explanation. Add per-tenant lag, exception telemetry, canary rollout, audited backfills, RPO/RTO, and cost attribution.

End with the main tension: users benefit from fast provisional intelligence, while finance requires reproducible finality. The design supports both and labels the difference.

Key takeaway:
Lead with financial invariants and customer workflow, then justify pipeline and AI components as mechanisms to meet them.""",

"""Purpose:
Turn Campfire's values into concrete evidence a candidate can show.

How to explain it:
Transparent accountability appears when you own an incident, communicate scope, and add prevention. Customer-centric innovation appears when user research changes priorities and produces a measurable finance outcome. Growth mindset and low ego appear when you invite criticism and adopt a better idea. Quality with velocity appears through small slices, automated tests, reconciliation, canaries, and rollback. Collaborative excellence appears through aligned domain, product, security, and engineering decisions.

A good story includes customer stakes, your specific role, alternatives, action, measurable result, an honest difficulty or mistake, learning, and the durable change afterward. Share team credit while being clear about your contribution.

Key takeaway:
Values answers are strongest when they contain a decision and evidence, not adjectives about yourself.""",

"""Purpose:
Prepare the candidate for both the practical interview setup and a collaborative discussion.

How to explain it:
Prepare three stories: customer empathy and innovation; quality with velocity; transparent accountability and collaboration. Include metrics and lessons. During technical questions, pause, clarify, state invariants, estimate, compare alternatives, admit uncertainty, invite correction, and summarize recovery.

Follow the supplied logistical guidance: test camera, microphone, and internet; use smart casual clothing that feels natural; and be ready for virtual and multi-hour onsite conversations. Ask questions that reveal real customer pain, finality rules, AI action boundaries, scaling pressure, engineering impact, and collaboration with accounting experts.

The goal is not to perform a memorized answer. Treat the interview as a design session with shared problem solving.

Key takeaway:
Preparation creates confidence, but curiosity, directness, and collaboration should remain visible in the conversation.""",
]

# Campfire slides follow the reusable AI ERP interview section; references remain last.
base_notes[36] += "\n\nCompanion guide:\nCampfire_Senior_Data_Engineer_System_Design_QA.docx contains 28 detailed questions, Campfire-focused model answers, values guidance, story preparation, and follow-up prompts."
speaker_notes = base_notes[:13] + new_general_notes + base_notes[13:36] + ai_erp_notes + campfire_notes + [base_notes[36]]

if len(speaker_notes) != len(prs.slides):
    raise ValueError(f"Expected {len(prs.slides)} notes, found {len(speaker_notes)}")

for slide, note in zip(prs.slides, speaker_notes):
    slide.notes_slide.notes_text_frame.text = note.strip()

# ---------- Metadata and save ----------
prs.core_properties.title = "Campfire-Tailored Senior Data Engineering and AI ERP Interview Playbook"
prs.core_properties.subject = "System design, AI-native finance architecture, Campfire values, and complex interview Q&A"
prs.core_properties.author = "Kiro"
prs.core_properties.keywords = "Campfire, senior data engineer, system design, AI ERP, finance, accounting, Delta Lake, Spark, interview"
prs.core_properties.comments = "Includes speaker notes, AI ERP architecture, Campfire-focused preparation based on the user-supplied candidate guide summary, and companion Q&A reference."
prs.save(OUT)
print(f"Created {OUT}")
print(f"Slides: {len(prs.slides)}")
print(f"Speaker notes: {len(speaker_notes)}")
print(f"Bytes: {OUT.stat().st_size}")
