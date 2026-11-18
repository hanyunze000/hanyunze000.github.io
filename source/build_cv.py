"""Create the English public CV from the same academic record as the website."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import profile_data as p


ROOT = Path(__file__).resolve().parent.parent
INK = "#1C302C"
GREEN = "#254C40"
MUTED = "#4A6054"
CLAY = "#864B3C"


def en(value):
    return value if isinstance(value, str) else value[0]


def style(name, font, size, leading, color=INK, **options):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
                          textColor=colors.HexColor(color), **options)


STYLES = {
    "title": style("name", "Times-Roman", 33, 36),
    "section": style("section", "Times-Bold", 18, 22, GREEN, spaceBefore=13, spaceAfter=7),
    "paper": style("paper title", "Times-Bold", 12.2, 15.5, spaceAfter=3),
    "body": style("body", "Helvetica", 10.3, 14.4),
    "note": style("note", "Helvetica", 9.6, 13.4, MUTED),
    "journal": style("journal", "Helvetica", 10.5, 14.5, GREEN),
    "meeting": style("conference", "Helvetica", 9.4, 13.5, MUTED, leftIndent=11),
    "date": style("date", "Helvetica", 9.2, 14.4, MUTED, alignment=TA_RIGHT),
}


def para(text, kind="body"):
    return Paragraph(text, STYLES[kind])


def paper_section(title, papers):
    return para(f'{title} <font name="Helvetica" size="10.5" color="{MUTED}">({len(papers)})</font>', "section")


def link(label, url):
    return f'<link href="{escape(url)}" color="{GREEN}"><u>{escape(label)}</u></link>'


def paper_flowables(item):
    title = escape(item["title"])
    if "doi" in item:
        title = f'<link href="https://doi.org/{item["doi"]}">{title}</link>'
    names = []
    for author in item["authors"]:
        name = f"<b>{escape(author)}</b>" if author == p.NAME else escape(author)
        if author == item.get("corresponding"):
            name += "<super>*</super>"
        names.append(name)
    lines = [para(title, "paper"), para(", ".join(names))]
    if "journal" in item:
        doi = link(item["doi"], "https://doi.org/" + item["doi"])
        lines.append(para(f'<i>{escape(item["journal"])}</i> ({item["year"]}) · {doi}', "journal"))
    if "meetings" in item:
        label = "Conference for this paper" if item.get("program_only") else "Presentations of this paper"
        lines.append(para(label, "meeting"))
        for event in item["meetings"]:
            event_name = escape(en(event["name"]))
            note = f' · {en(event["note"])}' if "note" in event else ""
            lines.append(para(f'{en(event["date"])} · {event_name}{note}', "meeting"))
    if "summary" in item:
        lines.extend([Spacer(1, 6), para(escape(en(item["summary"])))])
    lines.append(Spacer(1, 14))
    return KeepTogether(lines)


def cv_table(rows):
    data = []
    for date, title, institution in rows:
        record = f"<b>{escape(en(title))}</b><br/>{escape(en(institution))}"
        data.append([para(record), para(escape(en(date)), "date")])
    table = Table(data, colWidths=[348, 144], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def footer(canvas, doc):
    width, _ = A4
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD2C7"))
    canvas.line(51, 37, width - 51, 37)
    canvas.setFillColor(colors.HexColor(MUTED))
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(51, 24, "Yunze Han  /  Curriculum vitae")
    canvas.drawRightString(width - 51, 24, str(doc.page))
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(str(ROOT / "assets" / "yunze-han-cv.pdf"), pagesize=A4,
                            leftMargin=45, rightMargin=45, topMargin=36, bottomMargin=47,
                            title="Yunze Han — Curriculum Vitae", author=p.NAME, invariant=1,
                            subject="Agricultural and development economics")
    story = [
        para(p.NAME, "title"),
        Spacer(1, 5),
        para(p.MASKED_EMAIL + " (replace * with @)  ·  " + link("researchmap", p.RESEARCHMAP), "note"),
        Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor(CLAY)),
        para("Education", "section"), cv_table(p.EDUCATION),
        paper_section("Publications", p.PUBLICATIONS),
        para("* Corresponding author", "note"), Spacer(1, 4),
    ]
    story.extend(paper_flowables(item) for item in p.PUBLICATIONS)
    story.extend([PageBreak(), paper_section("Working papers", p.WORKING_PAPERS)])
    story.extend(paper_flowables(item) for item in p.WORKING_PAPERS)
    story.extend([PageBreak(), para("Research, teaching &amp; service", "section"), cv_table(p.APPOINTMENTS),
                  para("Research projects", "section")])
    for project in p.FIELDWORK:
        story.append(KeepTogether([
            para(escape(en(project["title"])) + " · " + en(project["country"]), "paper"),
            para(escape(en(project["detail"]))), Spacer(1, 5),
        ]))
    story.extend([para("Fellowships &amp; awards", "section"), cv_table(p.AWARDS),
                  para("Academic memberships", "section")])
    member_rows = [[para(escape(en(name))), para(f"Since {year}", "date")]
                   for year, name in p.MEMBERSHIPS]
    membership_table = Table(member_rows, colWidths=[383, 109], hAlign="LEFT")
    membership_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(membership_table)
    story.extend([para("Other professional experience", "section"), cv_table(p.OTHER_EXPERIENCE)])
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
