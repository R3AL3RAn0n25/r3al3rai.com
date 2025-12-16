#!/usr/bin/env python3
"""
R3ÆLƎR AI Pitch PDF Generator
Converts markdown pitch to professional PDF with architecture diagram
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import black, blue, darkblue, lightgrey
import re
import os

def markdown_to_pdf(markdown_file, output_pdf):
    """Convert markdown content to PDF with professional formatting"""

    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=darkblue,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        textColor=blue,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=12,
        leftIndent=20,
        spaceAfter=8,
        fontName='Helvetica'
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Courier',
        backgroundColor=lightgrey,
        borderPadding=5,
        spaceAfter=12
    )

    signature_style = ParagraphStyle(
        'CustomSignature',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )

    email_style = ParagraphStyle(
        'CustomEmail',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        textColor=blue,
        fontName='Helvetica'
    )

    # Split content into sections
    sections = md_content.split('---')

    story = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Handle title
        if section.startswith('# '):
            title = section.split('\n', 1)[0].replace('# ', '')
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            section = section.split('\n', 1)[1] if '\n' in section else ''

        # Handle subtitles
        if section.startswith('## '):
            subtitle = section.split('\n', 1)[0].replace('## ', '')
            story.append(Paragraph(subtitle, subtitle_style))
            story.append(Spacer(1, 15))
            section = section.split('\n', 1)[1] if '\n' in section else ''

        # Process lines
        lines = section.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle bullet points
            if line.startswith('- '):
                bullet_text = line[2:]
                # Handle bold text in bullets
                bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', bullet_text)
                story.append(Paragraph(f"• {bullet_text}", bullet_style))
                continue

            # Handle code blocks
            if line.startswith('```'):
                continue
            if line.startswith('┌') or line.startswith('│') or line.startswith('├') or line.startswith('└'):
                # ASCII art - treat as code
                story.append(Paragraph(line, code_style))
                continue

            # Handle bold text
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)

            # Handle signature
            if 'Bradley Wayne Hughs' in line:
                story.append(Paragraph(line, signature_style))
                continue
            if '@proton.me' in line:
                story.append(Paragraph(line, email_style))
                continue

            # Regular paragraph
            story.append(Paragraph(line, normal_style))

        story.append(Spacer(1, 20))

    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully: {output_pdf}")

if __name__ == "__main__":
    markdown_file = "R3ALER_AI_PITCH_COMPLETE.md"
    output_pdf = "R3ALER_AI_Pitch_Professional.pdf"

    if os.path.exists(markdown_file):
        markdown_to_pdf(markdown_file, output_pdf)
    else:
        print(f"Error: {markdown_file} not found")