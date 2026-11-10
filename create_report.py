from pathlib import Path
import re, html
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

root=Path(__file__).parent
pdfmetrics.registerFont(TTFont('Arial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
ink=colors.HexColor('#17213b'); slate=colors.HexColor('#59657a'); blue=colors.HexColor('#1959d1')
styles={
 'title':ParagraphStyle('title',fontName='Arial-Bold',fontSize=22,leading=26,textColor=ink,spaceAfter=12),
 'h2':ParagraphStyle('h2',fontName='Arial-Bold',fontSize=13,leading=16,textColor=blue,spaceBefore=10,spaceAfter=5,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=9.7,leading=14,textColor=ink,spaceAfter=6),
 'bullet':ParagraphStyle('bullet',fontName='Arial',fontSize=9.7,leading=14,textColor=ink,leftIndent=14,firstLineIndent=-10,spaceAfter=4),
}
def markup(text):
    text=html.escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'`(.+?)`',r'<font color="#1959d1">\1</font>',text)
    text=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',text)
    return text
story=[]
for line in (root/'database/normalization.md').read_text().splitlines():
    line=line.strip()
    if not line: continue
    if line.startswith('# '):
        story.append(Paragraph(markup(line[2:]),styles['title']))
        story.append(Image(str(root/'docs/database/er_diagram.png'),width=420,height=223.125))
        story.append(Spacer(1,14))
    elif line.startswith('## '): story.append(Paragraph(markup(line[3:]),styles['h2']))
    elif line.startswith('- '): story.append(Paragraph('– '+markup(line[2:]),styles['bullet']))
    else: story.append(Paragraph(markup(line),styles['body']))
def page(c,doc):
    c.setFillColor(blue);c.rect(0,A4[1]-8,A4[0],8,fill=1,stroke=0)
    c.setFont('Arial',8);c.setFillColor(slate);c.drawString(48,26,'ТРЕКЕР ПОЛЕЗНЫХ ПРИВЫЧЕК · ЛАБОРАТОРНАЯ № 4');c.drawRightString(A4[0]-48,26,str(doc.page))
doc=SimpleDocTemplate(str(root/'Отчёт лабораторная 4.pdf'),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=38,bottomMargin=48,title='Лабораторная работа № 4')
doc.build(story,onFirstPage=page,onLaterPages=page)
