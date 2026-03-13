"""
Generate Project Abstract PDF for Abuse Word Detector
College: Narula Institute of Technology | CSE (AIML)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF
import os

# ──────────────────────────────────────────────────
# OUTPUT PATH
# ──────────────────────────────────────────────────
OUTPUT = "/home/saurav-kumar/Downloads/AbuseWordDetector_Abstract.pdf"

# ──────────────────────────────────────────────────
# COLOURS
# ──────────────────────────────────────────────────
NIT_BLUE   = colors.HexColor("#003366")
NIT_GOLD   = colors.HexColor("#FFD700")
ACCENT     = colors.HexColor("#1565C0")
LIGHT_BLUE = colors.HexColor("#D6E4F7")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
DARK_GRAY  = colors.HexColor("#333333")
MID_GRAY   = colors.HexColor("#666666")
GREEN      = colors.HexColor("#1B5E20")
RED        = colors.HexColor("#B71C1C")
ORANGE     = colors.HexColor("#E65100")

W, H = A4


# ──────────────────────────────────────────────────
# CUSTOM FLOWABLE: FLOWCHART
# ──────────────────────────────────────────────────
class FlowchartFlowable(Flowable):
    """Draws the system architecture flowchart."""
    WIDTH  = 460
    HEIGHT = 640

    def wrap(self, availWidth, availHeight):
        return self.WIDTH, self.HEIGHT

    def draw(self):
        c = self.canv
        w = self.WIDTH
        # helper sizes
        bw, bh = 200, 36   # box width, height
        cx = w / 2          # centre x
        lx = cx - bw / 2    # left x of box

        def box(y, text, fill=LIGHT_BLUE, text_color=NIT_BLUE, radius=8, bold=False):
            c.setFillColor(fill)
            c.setStrokeColor(NIT_BLUE)
            c.setLineWidth(1.2)
            c.roundRect(lx, y, bw, bh, radius, stroke=1, fill=1)
            c.setFillColor(text_color)
            fs = 9
            c.setFont("Helvetica-Bold" if bold else "Helvetica", fs)
            # word-wrap manually
            lines = text.split("\n")
            lh = fs + 2
            start_y = y + bh / 2 + (len(lines) - 1) * lh / 2 - fs * 0.35
            for i, line in enumerate(lines):
                c.drawCentredString(cx, start_y - i * lh, line)

        def diamond(y, text, fill=NIT_GOLD):
            hw, hh = 130, 28
            c.setFillColor(fill)
            c.setStrokeColor(NIT_BLUE)
            c.setLineWidth(1.2)
            p = c.beginPath()
            p.moveTo(cx,       y + hh + 6)
            p.lineTo(cx - hw,  y + hh / 2)
            p.lineTo(cx,       y - 6)
            p.lineTo(cx + hw,  y + hh / 2)
            p.close()
            c.drawPath(p, stroke=1, fill=1)
            c.setFillColor(NIT_BLUE)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawCentredString(cx, y + hh / 2 - 3, text)

        def arrow(y_from, y_to, label=""):
            mid_x = cx
            c.setStrokeColor(DARK_GRAY)
            c.setLineWidth(1.0)
            c.line(mid_x, y_from, mid_x, y_to + 6)
            # arrow head triangle
            c.setFillColor(DARK_GRAY)
            p = c.beginPath()
            p.moveTo(mid_x,     y_to)
            p.lineTo(mid_x - 5, y_to + 9)
            p.lineTo(mid_x + 5, y_to + 9)
            p.close()
            c.drawPath(p, stroke=0, fill=1)
            if label:
                c.setFillColor(MID_GRAY)
                c.setFont("Helvetica-Oblique", 7.5)
                c.drawCentredString(mid_x + 55, y_to + (y_from - y_to) / 2, label)

        def side_box(y, text, side='left', fill=LIGHT_GRAY):
            sbw, sbh = 115, 30
            if side == 'left':
                sx = lx - sbw - 10
            else:
                sx = lx + bw + 10
            c.setFillColor(fill)
            c.setStrokeColor(MID_GRAY)
            c.setLineWidth(0.8)
            c.roundRect(sx, y, sbw, sbh, 5, stroke=1, fill=1)
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 7.5)
            lines = text.split("\n")
            lh = 9
            sy = y + sbh / 2 + (len(lines) - 1) * lh / 2 - 4
            for i, ln in enumerate(lines):
                if side == 'left':
                    c.drawCentredString(sx + sbw / 2, sy - i * lh, ln)
                else:
                    c.drawCentredString(sx + sbw / 2, sy - i * lh, ln)

        # ── Layout (y positions from top, descending) ──
        y_start = 610

        # 1. User Input
        box(y_start, "User Submits Text", fill=NIT_BLUE, text_color=colors.white, bold=True)
        arrow(y_start, y_start - 28)

        # 2. Mode Selection
        y2 = y_start - 28 - 38
        diamond(y2 + 6, "Mode: Kid or Adult?")
        # Side labels
        side_box(y2 + 8, "Kid Mode\n(strict thresholds)", side='left', fill=colors.HexColor("#E3F2FD"))
        side_box(y2 + 8, "Adult Mode\n(relaxed thresholds)", side='right', fill=colors.HexColor("#FFF8E1"))
        arrow(y2 + 6, y2 - 14)

        # 3. Emoji Detection
        y3 = y2 - 14 - 40
        box(y3, "Emoji Detection\n(Always runs — regex scan)", fill=colors.HexColor("#E8F5E9"))
        arrow(y3, y3 - 28)

        # 4. ML scoring
        y4 = y3 - 28 - 40
        box(y4, "Detoxify BERT Model\n(Primary Scorer — ML)", fill=colors.HexColor("#EDE7F6"))
        side_box(y4 + 3, "If model\nunavailable →\nregex fallback", side='right', fill=colors.HexColor("#FFF3E0"))
        arrow(y4, y4 - 28)

        # 5. Regional patterns
        y5 = y4 - 28 - 40
        box(y5, "Regional Pattern Matching\n(Hindi + Bengali — always runs)", fill=colors.HexColor("#FFF9C4"))
        arrow(y5, y5 - 28)

        # 6. Score aggregation
        y6 = y5 - 28 - 40
        box(y6, "Score Aggregation &\nThreshold Check", fill=LIGHT_BLUE)
        arrow(y6, y6 - 28)

        # 7. Severity label
        y7 = y6 - 28 - 40
        box(y7, "Assign Severity Label\n(Safe / Mild / Moderate / Severe)", fill=colors.HexColor("#FCE4EC"))

        # 8. Result
        arrow(y7, y7 - 28)
        y8 = y7 - 28 - 40
        box(y8, "Save to DB & Return Result", fill=NIT_BLUE, text_color=colors.white, bold=True)


class DBSchemaFlowable(Flowable):
    """Draws the AnalysisResult database table."""
    WIDTH  = 420
    HEIGHT = 230

    def wrap(self, aw, ah):
        return self.WIDTH, self.HEIGHT

    def draw(self):
        c = self.canv
        # Table header
        c.setFillColor(NIT_BLUE)
        c.setStrokeColor(NIT_BLUE)
        c.setLineWidth(1)
        c.roundRect(10, self.HEIGHT - 38, self.WIDTH - 20, 32, 4, stroke=1, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(self.WIDTH / 2, self.HEIGHT - 22, "AnalysisResult  (SQLite Table)")

        fields = [
            ("id",               "INTEGER",   "Primary Key, auto-increment"),
            ("text",             "TEXT",       "Input text submitted by user"),
            ("is_offensive",     "BOOLEAN",    "True if content flagged"),
            ("severity",         "VARCHAR(20)","safe / mild / moderate / severe"),
            ("confidence_score", "FLOAT",      "0.0–1.0 ML confidence"),
            ("categories",       "JSON",       "List of detected categories"),
            ("flagged_terms",    "JSON",       "Specific flagged words / phrases"),
            ("emoji_detections", "JSON",       "Bad emojis found + category"),
            ("mode",             "VARCHAR(10)","kid or adult"),
            ("analyzed_at",      "DATETIME",   "Auto-set on record creation"),
        ]

        row_h = 17
        col_w = [100, 105, 205]
        col_x = [10, 110, 215]
        y = self.HEIGHT - 44

        for i, (name, dtype, desc) in enumerate(fields):
            bg = colors.HexColor("#EEF4FF") if i % 2 == 0 else colors.white
            c.setFillColor(bg)
            c.setStrokeColor(colors.HexColor("#CCCCCC"))
            c.setLineWidth(0.5)
            for j, (cx_, cw) in enumerate(zip(col_x, col_w)):
                c.rect(cx_, y - row_h, cw, row_h, stroke=1, fill=1)

            c.setFillColor(NIT_BLUE)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(col_x[0] + 3, y - row_h + 5, name)
            c.setFillColor(ORANGE)
            c.setFont("Helvetica-Oblique", 7.5)
            c.drawString(col_x[1] + 3, y - row_h + 5, dtype)
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica", 7.5)
            c.drawString(col_x[2] + 3, y - row_h + 5, desc)

            y -= row_h

        # column headers
        c.setFillColor(colors.HexColor("#1565C0"))
        for k, (cx_, cw, label) in enumerate(zip(col_x, col_w, ["Field Name", "Data Type", "Description"])):
            c.rect(cx_, y, cw, row_h, stroke=1, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        for cx_, cw, label in zip(col_x, col_w, ["Field Name", "Data Type", "Description"]):
            c.drawCentredString(cx_ + cw / 2, y + 4, label)


# ──────────────────────────────────────────────────
# PAGE TEMPLATE (header / footer on each page)
# ──────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # TOP BANNER
    canvas.setFillColor(NIT_BLUE)
    canvas.rect(0, H - 60, W, 60, stroke=0, fill=1)
    canvas.setFillColor(NIT_GOLD)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(W / 2, H - 22, "NARULA INSTITUTE OF TECHNOLOGY")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(W / 2, H - 38, "Department of Computer Science & Engineering (AI & ML)")
    canvas.setFillColor(NIT_GOLD)
    canvas.rect(0, H - 63, W, 3, stroke=0, fill=1)

    # FOOTER
    canvas.setFillColor(NIT_BLUE)
    canvas.rect(0, 0, W, 28, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(W / 2, 10, f"Page {doc.page}  |  Abuse Word Detector  |  Project Submission 2025–26")
    canvas.restoreState()


# ──────────────────────────────────────────────────
# STYLES
# ──────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

title_style = S("DocTitle",
    fontSize=18, fontName="Helvetica-Bold",
    textColor=NIT_BLUE, alignment=TA_CENTER, spaceAfter=4)

subtitle_style = S("SubTitle",
    fontSize=11, fontName="Helvetica",
    textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=2)

section_head = S("SecHead",
    fontSize=13, fontName="Helvetica-Bold",
    textColor=colors.white, alignment=TA_LEFT,
    backColor=NIT_BLUE, leftIndent=-6, rightIndent=-6,
    borderPadding=(5, 8, 5, 8), spaceAfter=10, spaceBefore=16)

sub_head = S("SubHead",
    fontSize=11, fontName="Helvetica-Bold",
    textColor=NIT_BLUE, spaceAfter=4, spaceBefore=10)

body = S("Body",
    fontSize=10, fontName="Helvetica",
    textColor=DARK_GRAY, leading=16,
    alignment=TA_JUSTIFY, spaceAfter=6)

bullet = S("Bullet",
    fontSize=10, fontName="Helvetica",
    textColor=DARK_GRAY, leading=15,
    leftIndent=20, bulletIndent=8, spaceAfter=3)

caption = S("Caption",
    fontSize=8.5, fontName="Helvetica-Oblique",
    textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=6)

table_cell_head = S("TCH",
    fontSize=9, fontName="Helvetica-Bold",
    textColor=colors.white, alignment=TA_CENTER)

table_cell = S("TC",
    fontSize=9, fontName="Helvetica",
    textColor=DARK_GRAY, alignment=TA_LEFT)

info_label = S("InfoLabel",
    fontSize=10, fontName="Helvetica-Bold",
    textColor=NIT_BLUE, spaceAfter=2)

info_value = S("InfoValue",
    fontSize=10, fontName="Helvetica",
    textColor=DARK_GRAY, spaceAfter=2)


# ──────────────────────────────────────────────────
# BUILD DOCUMENT
# ──────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2.2 * cm,
    leftMargin=2.2 * cm,
    topMargin=3.6 * cm,
    bottomMargin=1.8 * cm,
)

story = []

# ── COVER INFO TABLE ──
info_data = [
    [Paragraph("<b>Project Title</b>", info_label),
     Paragraph("Abuse Word Detector — Hybrid Content Moderation System", info_value)],
    [Paragraph("<b>College</b>", info_label),
     Paragraph("Narula Institute of Technology, Kolkata", info_value)],
    [Paragraph("<b>Stream</b>", info_label),
     Paragraph("B.Tech — CSE (Artificial Intelligence &amp; Machine Learning)", info_value)],
    [Paragraph("<b>Mentor</b>", info_label),
     Paragraph("Mr. Parthasarathi De, Assistant Professor (CSE AIML)", info_value)],
    [Paragraph("<b>Students</b>", info_label),
     Paragraph("Saurav Kumar, Pralav Jha, Nasim Aktar — CSE (AIML)", info_value)],
    [Paragraph("<b>Academic Year</b>", info_label),
     Paragraph("2025 – 2026", info_value)],
]

info_table = Table(info_data, colWidths=[4.5 * cm, 11.5 * cm])
info_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
    ('BACKGROUND', (0, 0), (0, -1), LIGHT_BLUE),
    ('BOX',        (0, 0), (-1, -1), 1, NIT_BLUE),
    ('INNERGRID',  (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 7),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ('LEFTPADDING',   (0, 0), (-1, -1), 8),
]))
story.append(Spacer(1, 0.4 * cm))
story.append(info_table)
story.append(Spacer(1, 0.6 * cm))

# ── ABSTRACT ──
story.append(Paragraph("1. ABSTRACT", section_head))
story.append(Paragraph(
    "The <b>Abuse Word Detector</b> is a Django-based web application designed to identify and "
    "classify offensive, abusive, and harmful content in user-submitted text. The system employs "
    "a <b>hybrid detection pipeline</b> combining state-of-the-art BERT-based deep learning "
    "(Detoxify), rule-based regex pattern matching, and Unicode emoji analysis to deliver "
    "robust, multi-lingual content moderation. It supports content moderation for both child-safe "
    "(Kid Mode) and general-audience (Adult Mode) contexts through configurable sensitivity thresholds.",
    body))
story.append(Paragraph(
    "The application classifies text into six toxicity dimensions — Toxicity, Severe Toxicity, "
    "Obscene, Threat, Insult, and Identity Attack — assigning a confidence score and a severity "
    "label (Safe, Mild, Moderate, Severe). Multilingual offensive content in <b>Hindi</b> and "
    "<b>Bengali</b> transliterations is handled through a dedicated rule-based layer, making the "
    "system suitable for Indian social-media moderation scenarios. All analysis results are "
    "persisted in an SQLite database for audit, history browsing, and API-based access.",
    body))

# ── INTRODUCTION ──
story.append(Paragraph("2. INTRODUCTION", section_head))
story.append(Paragraph(
    "The rapid growth of social media, online forums, and digital communication platforms has "
    "led to a significant increase in the spread of hate speech, cyberbullying, and abusive "
    "language. Traditional keyword-filter approaches are brittle; they fail to handle synonyms, "
    "misspellings, context, or regional language variations. Modern NLP-based approaches using "
    "deep learning models have shown superior performance, but often lack interpretability and "
    "multilingual support tailored to the Indian context.",
    body))
story.append(Paragraph(
    "This project addresses these challenges by designing and implementing a <b>hybrid content "
    "moderation architecture</b> that layers multiple detection strategies — ensuring both "
    "high recall (catching offensive content) and interpretability (explaining why content was "
    "flagged). The system is accessible as a web application and via a REST API, making it "
    "suitable for integration into chat platforms, social networks, and educational tools.",
    body))

story.append(Paragraph("2.1  Objectives", sub_head))
objectives = [
    "Detect offensive and abusive language in English, Hindi (transliterated), and Bengali.",
    "Provide interpretable results: flagged categories, confidence score, and severity level.",
    "Support audience-specific moderation policies (Kid Mode vs. Adult Mode).",
    "Persist analysis results for historical review and audit purposes.",
    "Expose a REST API endpoint suitable for third-party integration.",
]
for obj in objectives:
    story.append(Paragraph(f"• {obj}", bullet))

story.append(Paragraph("2.2  Scope", sub_head))
story.append(Paragraph(
    "The system targets text-based online communications in English with supplementary support "
    "for Hindi and Bengali transliterations. The current release handles single-document "
    "analysis (up to 512 tokens for the BERT model). Video, audio, and image content are "
    "outside the current scope but are planned for future enhancement.",
    body))

# ── SYSTEM ARCHITECTURE / FLOWCHART ──
story.append(PageBreak())
story.append(Paragraph("3. SYSTEM ARCHITECTURE & FLOWCHART", section_head))
story.append(Paragraph(
    "The diagram below illustrates the end-to-end text analysis pipeline. Each step is executed "
    "sequentially; multiple detection layers run in concert and their scores are aggregated "
    "before the final severity decision.",
    body))
story.append(Spacer(1, 0.4 * cm))
story.append(FlowchartFlowable())
story.append(Paragraph(
    "Figure 1 — System Architecture Flowchart: End-to-end text analysis pipeline.",
    caption))

# ── DATABASE SCHEMA ──
story.append(PageBreak())
story.append(Paragraph("4. DATABASE SCHEMA ABSTRACT", section_head))
story.append(Paragraph(
    "All analysis results are stored in a single relational table <b>AnalysisResult</b> within "
    "an SQLite database. JSON fields are used to store structured lists (categories, flagged "
    "terms, emoji detections) without requiring additional join tables, keeping the schema "
    "lean and the queries simple. The schema is managed through Django ORM migrations.",
    body))
story.append(Spacer(1, 0.4 * cm))
story.append(DBSchemaFlowable())
story.append(Paragraph("Figure 2 — AnalysisResult database schema (SQLite, managed by Django ORM).", caption))

story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("4.1  Data Flow Narrative", sub_head))
story.append(Paragraph(
    "When a user submits text via the web form or REST API, the "
    "<code>analyze_text()</code> function in <b>services.py</b> orchestrates the pipeline. "
    "The result dictionary is serialised and saved to the database using "
    "<code>AnalysisResult.objects.create()</code>. The history view retrieves the last 50 "
    "records ordered by <code>analyzed_at</code> (descending), while the API returns a "
    "JSON response immediately without a page reload.",
    body))

# ── LIBRARIES / TECH STACK ──
story.append(Paragraph("5. LIBRARIES & TECHNOLOGY STACK", section_head))
story.append(Paragraph(
    "The following is a detailed description of all primary libraries and frameworks used in "
    "this project, their sources, and their roles within the system.",
    body))

libs = [
    ("Django 5.x", "https://pypi.org/project/Django/", "BSD-3-Clause",
     "The primary web framework providing the MVC architecture, ORM, admin interface, URL routing, "
     "template engine, and development server. All views, models, and URL patterns are defined using "
     "Django conventions."),
    ("Detoxify", "https://pypi.org/project/detoxify/", "Apache-2.0",
     "A Python library wrapping pre-trained BERT-based transformer models trained on the "
     "Jigsaw Toxic Comments dataset. It predicts multi-label toxicity scores across six "
     "categories: toxicity, severe_toxicity, obscene, threat, insult, and identity_attack. "
     "The 'original' model variant is loaded lazily as a singleton at first call."),
    ("Transformers (HuggingFace)", "https://pypi.org/project/transformers/", "Apache-2.0",
     "The underlying library used by Detoxify for BERT model loading, tokenisation, and "
     "neural network inference via PyTorch. Provides the tokenizer and model weights."),
    ("PyTorch", "https://pypi.org/project/torch/", "BSD-3-Clause",
     "Deep learning framework used at runtime by HuggingFace Transformers for tensor "
     "computations and BERT inference on CPU or GPU."),
    ("Python re (regex)", "https://docs.python.org/3/library/re.html", "PSF",
     "Python's built-in regular expression engine. Used as the fallback scorer when Detoxify "
     "is unavailable, and as the always-on engine for Hindi/Bengali transliteration pattern "
     "matching and emoji detection."),
    ("Python 3.12", "https://www.python.org/", "PSF",
     "The runtime environment. Key standard library modules used: re, logging, json."),
    ("SQLite3", "https://www.sqlite.org/", "Public Domain",
     "Embedded relational database bundled with Python. Stores all AnalysisResult records. "
     "No external database server is required for deployment."),
    ("Bootstrap 5", "https://getbootstrap.com/", "MIT",
     "Frontend CSS/JS framework used in the Django HTML templates for responsive layout, "
     "progress bars (confidence score visualisation), badges (severity labels), and cards."),
    ("ReportLab", "https://pypi.org/project/reportlab/", "BSD",
     "Used to programmatically generate this PDF document — including custom flowcharts, "
     "database schema diagrams, styled tables, and page headers/footers."),
]

for i, (name, url, lic, desc) in enumerate(libs, 1):
    story.append(Paragraph(f"5.{i}  {name}", sub_head))
    data = [
        [Paragraph("<b>Source URL</b>", table_cell_head), Paragraph(url, table_cell)],
        [Paragraph("<b>License</b>",    table_cell_head), Paragraph(lic, table_cell)],
        [Paragraph("<b>Role</b>",       table_cell_head), Paragraph(desc, table_cell)],
    ]
    t = Table(data, colWidths=[3 * cm, 12 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_BLUE),
        ('BACKGROUND', (1, 0), (1, -1), LIGHT_GRAY),
        ('BOX',        (0, 0), (-1, -1), 0.8, NIT_BLUE),
        ('INNERGRID',  (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(KeepTogether([t, Spacer(1, 0.2 * cm)]))

# ── MODE THRESHOLDS TABLE ──
story.append(PageBreak())
story.append(Paragraph("6. MODE THRESHOLDS (Kid vs. Adult)", section_head))
story.append(Paragraph(
    "The system supports two sensitivity modes. Kid Mode applies strict thresholds suitable "
    "for children's platforms, flagging even mild offensive content. Adult Mode applies "
    "relaxed thresholds appropriate for general-audience forums where mild language is acceptable.",
    body))
story.append(Spacer(1, 0.4 * cm))

headers = ["ML Category", "Kid Mode Threshold", "Adult Mode Threshold", "Severity Impact"]
rows = [
    ["Toxicity",        "0.15", "0.75", "Primary indicator"],
    ["Severe Toxicity", "0.05", "0.50", "Highest weight (×1.0)"],
    ["Obscene",         "0.10", "0.70", "Weight ×0.85"],
    ["Threat",          "0.10", "0.60", "Weight ×1.0 (high risk)"],
    ["Insult",          "0.15", "0.80", "Weight ×0.80"],
    ["Identity Attack", "0.10", "0.65", "Weight ×0.95 (hate speech)"],
]

table_data = [[Paragraph(h, table_cell_head) for h in headers]] + \
             [[Paragraph(c, table_cell) for c in row] for row in rows]

thresh_table = Table(table_data, colWidths=[4.5*cm, 3.5*cm, 3.5*cm, 4.5*cm])
thresh_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NIT_BLUE),
    ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
    ('BOX',        (0, 0), (-1, -1), 1, NIT_BLUE),
    ('INNERGRID',  (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ('TOPPADDING',    (0, 0), (-1, -1), 7),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ('LEFTPADDING',   (0, 0), (-1, -1), 8),
    ('ALIGN',      (1, 0), (2, -1), 'CENTER'),
]))
story.append(thresh_table)

# ── SEVERITY SEVERITY ──
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph("6.1  Severity Level Mapping", sub_head))
sev_data = [
    [Paragraph("<b>Severity</b>", table_cell_head),
     Paragraph("<b>Confidence Range</b>", table_cell_head),
     Paragraph("<b>Meaning</b>", table_cell_head)],
    [Paragraph("Safe",     table_cell), Paragraph("0.00",           table_cell), Paragraph("No offensive content detected",          table_cell)],
    [Paragraph("Mild",     table_cell), Paragraph("0.01 – 0.34",    table_cell), Paragraph("Minor or borderline content",            table_cell)],
    [Paragraph("Moderate", table_cell), Paragraph("0.35 – 0.64",    table_cell), Paragraph("Clearly offensive but not extreme",      table_cell)],
    [Paragraph("Severe",   table_cell), Paragraph("0.65 – 1.00",    table_cell), Paragraph("Highly toxic, threatening, or hateful",  table_cell)],
]
sev_table = Table(sev_data, colWidths=[3.5*cm, 4*cm, 8.5*cm])
sev_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NIT_BLUE),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
    ('BOX',        (0, 0), (-1, -1), 1, NIT_BLUE),
    ('INNERGRID',  (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ('TOPPADDING',    (0, 0), (-1, -1), 7),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ('LEFTPADDING',   (0, 0), (-1, -1), 8),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
]))
story.append(sev_table)

# ── CONCLUSION ──
story.append(Spacer(1, 0.6 * cm))
story.append(Paragraph("7. CONCLUSION", section_head))
story.append(Paragraph(
    "The Abuse Word Detector demonstrates how a layered, hybrid approach to content moderation "
    "can outperform single-strategy solutions. By combining the contextual understanding of a "
    "BERT-based ML model with deterministic regex rules for regional languages and Unicode emoji "
    "analysis, the system achieves high coverage across diverse input types. The dual-mode "
    "(Kid / Adult) design acknowledges that acceptable content is audience-dependent, providing "
    "platform operators with flexible policy controls.",
    body))
story.append(Paragraph(
    "Future work will explore fine-tuning the underlying model on Hindi and Bengali corpora, "
    "adding support for code-switched text (Hinglish / Banglish), image meme analysis, and "
    "real-time stream processing for high-throughput platforms.",
    body))

# ── REFERENCES ──
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("8. REFERENCES", section_head))
refs = [
    "[1] Hanu, L., & Unitary team. (2020). <i>Detoxify</i>. GitHub. https://github.com/unitaryai/detoxify",
    "[2] Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2018). BERT: Pre-training of Deep Bidirectional Transformers. <i>arXiv:1810.04805</i>.",
    "[3] Jigsaw / Google. (2018). <i>Toxic Comment Classification Challenge</i>. Kaggle. https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge",
    "[4] Django Software Foundation. (2024). <i>Django Documentation v5.x</i>. https://docs.djangoproject.com/",
    "[5] HuggingFace. (2024). <i>Transformers Library</i>. https://huggingface.co/docs/transformers/",
    "[6] Python Software Foundation. (2024). <i>Python 3.12 Documentation — re module</i>. https://docs.python.org/3/library/re.html",
    "[7] Waseem, Z., & Hovy, D. (2016). Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection. <i>Proceedings of NAACL-HLT 2016</i>.",
]
for ref in refs:
    story.append(Paragraph(ref, bullet))

# ──────────────────────────────────────────────────
# BUILD PDF
# ──────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"✅  PDF generated → {OUTPUT}")
