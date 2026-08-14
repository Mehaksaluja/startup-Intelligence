from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re
import os


def markdown_to_pdf(markdown_text: str, output_path: str, company_name: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    # custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6,
        alignment=TA_CENTER,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#666666"),
        spaceAfter=20,
        alignment=TA_CENTER,
    )

    h1_style = ParagraphStyle(
        "CustomH1",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=20,
        spaceAfter=8,
        borderPad=4,
    )

    h2_style = ParagraphStyle(
        "CustomH2",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#16213e"),
        spaceBefore=14,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
        leading=16,
    )

    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=4,
        leading=15,
        leftIndent=20,
        bulletIndent=10,
    )

    bold_style = ParagraphStyle(
        "Bold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    story = []
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"{company_name}", title_style))
    story.append(Paragraph("Intelligence Brief", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2,
                 color=colors.HexColor("#1a1a2e")))
    story.append(Spacer(1, 0.2 * inch))
    lines = markdown_text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            story.append(Spacer(1, 0.05 * inch))
            continue

        if line.startswith("# "):
            text = line[2:].strip()
            if company_name.lower() not in text.lower():
                story.append(Paragraph(text, h1_style))
                story.append(HRFlowable(
                    width="100%", thickness=0.5,
                    color=colors.HexColor("#cccccc")
                ))
            continue

        if line.startswith("## "):
            text = line[3:].strip()
            story.append(Paragraph(text, h2_style))
            continue

        if line.startswith("### "):
            text = line[4:].strip()
            story.append(Paragraph(f"<b>{text}</b>", body_style))
            continue

        if line.startswith("- ") or line.startswith("* "):
            text = line[2:].strip()
            text = apply_inline_formatting(text)
            story.append(Paragraph(f"• {text}", bullet_style))
            continue

        if re.match(r"^\d+\.\s", line):
            text = re.sub(r"^\d+\.\s", "", line).strip()
            text = apply_inline_formatting(text)
            story.append(Paragraph(f"• {text}", bullet_style))
            continue

        if line.startswith("---") or line.startswith("***"):
            story.append(HRFlowable(
                width="100%", thickness=0.5,
                color=colors.HexColor("#cccccc")
            ))
            continue

        text = apply_inline_formatting(line)
        story.append(Paragraph(text, body_style))

    doc.build(story)
    print(f"PDF saved to: {output_path}")


def apply_inline_formatting(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.*?)__", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"_(.*?)_", r"<i>\1</i>", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = text.replace("&", "&amp;")
    text = text.replace("<b>", "BOLD_OPEN").replace("</b>", "BOLD_CLOSE")
    text = text.replace("<i>", "ITALIC_OPEN").replace("</i>", "ITALIC_CLOSE")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("BOLD_OPEN", "<b>").replace("BOLD_CLOSE", "</b>")
    text = text.replace("ITALIC_OPEN", "<i>").replace("ITALIC_CLOSE", "</i>")

    return text