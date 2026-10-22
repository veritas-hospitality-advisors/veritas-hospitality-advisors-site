#!/usr/bin/env python3
"""
Veritas Hospitality Advisors — Owner's Profit Control Playbook
PDF generation using ReportLab — CORRECT 25-PAGE SOURCE CONTENT
Source: veritas_owner_profit_control_playbook_25_pages.pdf (Vaishakh Surendran IP)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import os

# ── Register brand fonts ───────────────────────────────────────────────────────
_FONTS_DIR = os.path.join(os.path.dirname(__file__), 'fonts')

def _reg(name, filename):
    path = os.path.join(_FONTS_DIR, filename)
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))
        return True
    return False

_have_brand_fonts = all([
    _reg('SourceSerif4',        'SourceSerif4-Regular.ttf'),
    _reg('SourceSerif4-Bold',   'SourceSerif4-Bold.ttf'),
    _reg('SourceSerif4-Italic', 'SourceSerif4-Italic.ttf'),
    _reg('PublicSans',          'PublicSans-Regular.ttf'),
    _reg('PublicSans-Bold',     'PublicSans-Bold.ttf'),
    _reg('PublicSans-Italic',   'PublicSans-Italic.ttf'),
])

if _have_brand_fonts:
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily('PublicSans',
        normal='PublicSans', bold='PublicSans-Bold', italic='PublicSans-Italic', boldItalic='PublicSans-Bold')
    registerFontFamily('SourceSerif4',
        normal='SourceSerif4', bold='SourceSerif4-Bold', italic='SourceSerif4-Italic', boldItalic='SourceSerif4-Bold')

# ── Brand palette ──────────────────────────────────────────────────────────────
INK   = colors.HexColor('#0D1B2A')   # Midnight navy
CREAM = colors.HexColor('#F5F4EF')   # Off-white
GOLD  = colors.HexColor('#A57426')   # Warm gold
SLATE = colors.HexColor('#4A6080')   # Slate (navy-adjacent)
WHITE = colors.white
LIGHT = colors.HexColor('#E8E7E0')   # Subtle rule colour
# Muted cream, for secondary text sitting on the INK (navy) cover only —
# replaces leftover Forest-Green-era greens/khakis never migrated to Navy.
CREAM_MUTED_HI = colors.Color(245/255, 244/255, 239/255, alpha=0.80)
CREAM_MUTED_LO = colors.Color(245/255, 244/255, 239/255, alpha=0.50)

W, H = A4   # 595.27 x 841.89 pt
MARGIN_OUTER = 22 * mm
MARGIN_INNER = 22 * mm
MARGIN_TOP   = 22 * mm
MARGIN_BOT   = 22 * mm

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'owner-playbook.pdf')

# ── Custom rule flowable ────────────────────────────────────────────────────────
class ThinRule(Flowable):
    def __init__(self, width, color=LIGHT, thickness=0.5):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = thickness + 2

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness / 2, self.width, self.thickness / 2)


class GoldBar(Flowable):
    """Full-width gold rule, heavier."""
    def __init__(self, width, height=3):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(GOLD)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


# ── Styles ──────────────────────────────────────────────────────────────────────
def make_styles():
    # Body text: Source Serif 4 (headings); UI / labels: Public Sans
    if _have_brand_fonts:
        serif       = 'SourceSerif4'
        serif_bold  = 'SourceSerif4-Bold'
        serif_ital  = 'SourceSerif4-Italic'
        sans        = 'PublicSans'
        sans_bold   = 'PublicSans-Bold'
        sans_ital   = 'PublicSans-Italic'
    else:
        serif = sans = 'Helvetica'
        serif_bold = sans_bold = 'Helvetica-Bold'
        serif_ital = sans_ital = 'Helvetica-Oblique'

    base_font      = serif
    base_bold      = serif_bold
    base_italic    = serif_ital
    base_bolditalic= serif_bold

    return {
        'cover_title': ParagraphStyle(
            'cover_title',
            fontName=serif_bold,
            fontSize=40,
            leading=46,
            textColor=WHITE,
            alignment=TA_LEFT,
            spaceAfter=10,
        ),
        'cover_subtitle': ParagraphStyle(
            'cover_subtitle',
            fontName=serif_ital,
            fontSize=14,
            leading=20,
            textColor=CREAM_MUTED_HI,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        'cover_byline': ParagraphStyle(
            'cover_byline',
            fontName=sans,
            fontSize=9,
            leading=14,
            textColor=CREAM_MUTED_LO,
            alignment=TA_LEFT,
        ),
        'toc_heading': ParagraphStyle(
            'toc_heading',
            fontName=sans_bold,
            fontSize=11,
            leading=14,
            textColor=INK,
            spaceAfter=4,
        ),
        'toc_item': ParagraphStyle(
            'toc_item',
            fontName=sans,
            fontSize=9.5,
            leading=14,
            textColor=INK,
            leftIndent=0,
        ),
        'toc_num': ParagraphStyle(
            'toc_num',
            fontName=sans_bold,
            fontSize=9.5,
            leading=14,
            textColor=GOLD,
        ),
        'section_label': ParagraphStyle(
            'section_label',
            fontName=sans_bold,
            fontSize=7.5,
            leading=10,
            textColor=GOLD,
            spaceBefore=0,
            spaceAfter=4,
        ),
        'article_num': ParagraphStyle(
            'article_num',
            fontName=sans_bold,
            fontSize=9,
            leading=12,
            textColor=GOLD,
            spaceAfter=4,
        ),
        'article_title': ParagraphStyle(
            'article_title',
            fontName=serif_bold,
            fontSize=18,
            leading=23,
            textColor=INK,
            spaceAfter=6,
        ),
        'article_tag': ParagraphStyle(
            'article_tag',
            fontName=sans_bold,
            fontSize=7.5,
            leading=10,
            textColor=GOLD,
            spaceAfter=8,
        ),
        'body': ParagraphStyle(
            'body',
            fontName=serif,
            fontSize=10,
            leading=16,
            textColor=INK,
            alignment=TA_LEFT,  # was TA_JUSTIFY — no hyphenation support produced uneven word-spacing "rivers" (fixed 10 Oct 2026)
            spaceAfter=8,
        ),
        'body_first': ParagraphStyle(
            'body_first',
            fontName=serif_ital,
            fontSize=11,
            leading=17,
            textColor=INK,
            alignment=TA_LEFT,  # was TA_JUSTIFY — same rivers issue, worse in italic (fixed 10 Oct 2026)
            spaceAfter=10,
        ),
        'pull_quote': ParagraphStyle(
            'pull_quote',
            fontName=serif_ital,
            fontSize=12,
            leading=18,
            textColor=SLATE,
            alignment=TA_LEFT,
            leftIndent=16,
            rightIndent=0,
            spaceBefore=12,
            spaceAfter=12,
        ),
        'sources': ParagraphStyle(
            'sources',
            fontName=sans_ital,
            fontSize=7.5,
            leading=11,
            textColor=SLATE,
            spaceAfter=4,
        ),
        'sources_label': ParagraphStyle(
            'sources_label',
            fontName=sans_bold,
            fontSize=7.5,
            leading=11,
            textColor=GOLD,
            spaceAfter=2,
        ),
        'section_intro': ParagraphStyle(
            'section_intro',
            fontName=base_italic,
            fontSize=11,
            leading=17,
            textColor=WHITE,
            alignment=TA_LEFT,
            spaceAfter=0,
        ),
        'section_intro_body': ParagraphStyle(
            'section_intro_body',
            fontName=serif_ital,
            fontSize=10.5,
            leading=16,
            textColor=SLATE,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        'divider_title': ParagraphStyle(
            'divider_title',
            fontName=base_bold,
            fontSize=22,
            leading=28,
            textColor=WHITE,
            alignment=TA_LEFT,
            spaceAfter=10,
        ),
        'footer': ParagraphStyle(
            'footer',
            fontName=base_font,
            fontSize=7,
            leading=10,
            textColor=SLATE,
        ),
        'page_num': ParagraphStyle(
            'page_num',
            fontName=base_bold,
            fontSize=7,
            leading=10,
            textColor=GOLD,
            alignment=TA_RIGHT,
        ),
    }


# ── Page templates (header / footer via onPage) ─────────────────────────────────
def make_header_footer(canvas, doc, styles):
    canvas.saveState()
    page = doc.page
    if _have_brand_fonts:
        _sans_bold, _sans_reg = 'PublicSans-Bold', 'PublicSans'
    else:
        _sans_bold, _sans_reg = 'Helvetica-Bold', 'Helvetica'


    if page == 1:
        # ── Full-bleed INK background ──────────────────────────────────
        canvas.setFillColor(INK)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)

        # ── GOLD top bar (8 pt) ────────────────────────────────────────
        canvas.setFillColor(GOLD)
        canvas.rect(0, H - 8, W, 8, fill=1, stroke=0)

        # ── Bottom info block (painted on canvas, anchored) ────────────
        bot_y  = 40 * mm          # baseline for bottom block
        lx     = MARGIN_OUTER     # left margin
        rx     = W - MARGIN_OUTER # right edge
        mid    = W / 2

        # Thin gold rule above bottom block
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.6)
        canvas.line(lx, bot_y + 36, rx, bot_y + 36)

        # Info labels (muted green)
        canvas.setFont(_sans_bold, 7)
        canvas.setFillColor(GOLD)
        canvas.drawString(lx,   bot_y + 24, 'PREPARED BY')
        canvas.drawString(mid,  bot_y + 24, 'DATE')

        # Info values (white)
        canvas.setFont(_sans_bold, 10)
        canvas.setFillColor(WHITE)
        canvas.drawString(lx,   bot_y + 10, 'Vaishakh Surendran')
        canvas.drawString(mid,  bot_y + 10, 'October 2026')

        # Second row labels
        canvas.setFont(_sans_bold, 7)
        canvas.setFillColor(GOLD)
        canvas.drawString(lx,   bot_y - 4, 'ORGANISATION')
        canvas.drawString(mid,  bot_y - 4, 'STATUS')

        # Second row values
        canvas.setFont(_sans_bold, 9)
        canvas.setFillColor(WHITE)
        canvas.drawString(lx,   bot_y - 16, 'Veritas Hospitality Advisors')
        canvas.drawString(mid,  bot_y - 16, 'Editorial draft')

        # Thin rule below bottom block
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.4)
        canvas.line(lx, bot_y - 28, rx, bot_y - 28)

        # Disclaimer
        canvas.setFont(_sans_reg, 6.5)
        canvas.setFillColor(CREAM_MUTED_LO)
        disclaimer = (
            'Illustrative figures are fictional and not benchmarks. '
            'This guide does not constitute financial, legal or accounting advice.'
        )
        canvas.drawString(lx, bot_y - 40, disclaimer)

        canvas.restoreState()
        return

    # Footer rule
    y_rule = MARGIN_BOT - 6 * mm
    canvas.setStrokeColor(LIGHT)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN_OUTER, y_rule, W - MARGIN_OUTER, y_rule)

    # Footer text
    canvas.setFont(_sans_reg, 7)
    canvas.setFillColor(SLATE)
    canvas.drawString(MARGIN_OUTER, y_rule - 4 * mm, 'Veritas Hospitality Advisors — Confidential')

    canvas.setFont(_sans_bold, 7)
    canvas.setFillColor(GOLD)
    canvas.drawRightString(W - MARGIN_OUTER, y_rule - 4 * mm, str(page))

    canvas.restoreState()


# ── Cover page ──────────────────────────────────────────────────────────────────
def build_cover(story, styles, cw):
    """
    Full ink-green cover.
    Background + bottom info block are painted by make_header_footer canvas callback.
    This function only places the text content in the upper two-thirds.
    """
    # Push content down from the gold top bar — sit in upper third
    story.append(Spacer(1, 68))

    # Eyebrow label
    story.append(Paragraph('VERITAS HOSPITALITY ADVISORS', styles['cover_byline']))
    story.append(Spacer(1, 18))

    # Gold accent rule above title
    story.append(ThinRule(cw, color=GOLD, thickness=1.2))
    story.append(Spacer(1, 18))

    # Main title — large, left-aligned, white
    story.append(Paragraph(
        'The Owner&#x2019;s<br/>Profit Control<br/>Playbook',
        styles['cover_title']
    ))
    story.append(Spacer(1, 20))

    # Subtitle
    story.append(Paragraph(
        'A 90-day diagnostic and governance system<br/>for independent hotels in India',
        styles['cover_subtitle']
    ))
    story.append(Spacer(1, 32))

    # Slim SLATE rule as a visual separator
    story.append(ThinRule(cw, color=colors.HexColor('#4A6080'), thickness=0.5))
    story.append(Spacer(1, 20))

    # Short descriptor paragraph
    desc_style = ParagraphStyle(
        'cover_desc',
        fontName='PublicSans' if _have_brand_fonts else 'Helvetica',
        fontSize=9.5,
        leading=15,
        textColor=CREAM_MUTED_HI,
        alignment=TA_LEFT,
    )
    story.append(Paragraph(
        'A practical owner&#x2019;s guide to understanding where the money goes '
        'in an independent Indian hotel &#x2014; from channel economics and GST '
        'to governance, cash control and the 90-day decision process.',
        desc_style
    ))
    # Bottom info block is rendered entirely on canvas — no story elements needed


# ── Table of contents ─────────────────────────────────────────────────────────
def build_toc(story, styles, cw):
    story.append(PageBreak())
    story.append(GoldBar(cw, height=3))
    story.append(Spacer(1, 24))
    story.append(Paragraph('CONTENTS', styles['section_label']))
    story.append(Spacer(1, 6))
    story.append(ThinRule(cw))
    story.append(Spacer(1, 14))

    toc_sections = [
        ('02', 'Executive decision brief — What to do if your hotel is busy but you cannot explain the cash'),
        ('03', 'Method and evidence boundaries — Where this guide is evidence and where it is a proposal'),
        ('04', 'The one-page owner control map — The six questions to answer every month'),
        ('05', 'Before measuring anything — Agree the definitions'),
        ('06', 'The revenue-to-cash bridge — Follow one month from guest to bank'),
        ('07', 'Worked example: a full-looking hotel — Fictional 50-room property, not a benchmark'),
        ('08', 'Channel economics — A booking source is a cost-and-demand relationship'),
        ('09', 'Rate and inventory — Price tomorrow, not last year\'s headline'),
        ('10', 'F&amp;B and banquet contribution — Turnover is not the same as contribution'),
        ('11', 'Payroll and service — Do not fix a wage problem by breaking the guest experience'),
        ('12', 'Energy and maintenance — Separate consumption from capacity and repair needs'),
        ('13', 'Cash, receivables and deposits — Why a good P&amp;L can coexist with a bad bank balance'),
        ('14', 'Capex and return — Ask what the investment changes and when'),
        ('15', 'Guest mix and local demand — A national tourist visit is not your booking'),
        ('16', 'Forecasting without false precision — Three cases are better than one immaculate spreadsheet'),
        ('17', 'Deciding who decides — The owner, GM and adviser need a shared map'),
        ('18', 'The monthly owner meeting — Forty-five minutes for decisions, not a theatre of charts'),
        ('19', 'The action register — An insight without an owner expires quickly'),
        ('20', 'Protecting the data — Confidentiality is operational, not decorative'),
        ('21', 'Where an adviser can add value — When to seek help, and when not to'),
        ('22', 'The 90-day implementation plan — Four practical phases'),
        ('23', 'Owner worksheets — Copy these fields into a spreadsheet or board pack'),
        ('24', 'Owner readiness self-assessment — Score the system, not the people'),
        ('25', 'Definitions, sources and next step — A guide to start a better conversation'),
    ]

    for num, title in toc_sections:
        row_data = [[
            Paragraph(num, styles['toc_num']),
            Paragraph(title, styles['toc_item']),
        ]]
        t = Table(row_data, colWidths=[22, cw - 22])
        t.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t)

    story.append(Spacer(1, 20))
    story.append(ThinRule(cw))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        'Evidence sources: [H] Horwath HTL, India Hotel Market Review 2025, 4 Feb 2026; '
        '[V] HVS ANAROCK, India Hospitality Industry Overview 2025, 8 May 2026; '
        '[M] Ministry of Tourism beta dashboard, data.tourism.gov.in/dashboard (accessed 1 Oct 2026); '
        '[P] Professionalising Indian Family Firms, SAGE, 28 Feb 2020; '
        '[W] PwC, 11th India Family Business Survey, 2023.',
        styles['sources']
    ))


# ── Section renderer (one section = one page of the playbook) ─────────────────
def build_section(story, styles, cw, sec_num, title, subtitle, paragraphs, worksheet=None, pull=None):
    """Render one playbook section with section number, title, subtitle, body, optional worksheet."""
    story.append(PageBreak())
    story.append(Spacer(1, 4))

    # Section eyebrow
    story.append(Paragraph(f'OWNER PROFIT CONTROL / {sec_num:02d}', styles['article_num']))
    story.append(Paragraph(title, styles['article_title']))
    story.append(Paragraph(subtitle, styles['section_intro_body']))
    story.append(GoldBar(cw, height=2))
    story.append(Spacer(1, 14))

    for i, para in enumerate(paragraphs):
        style = styles['body_first'] if i == 0 else styles['body']
        story.append(Paragraph(para, style))

    if pull:
        story.append(Spacer(1, 4))
        story.append(ThinRule(cw, color=GOLD, thickness=0.8))
        story.append(Spacer(1, 2))
        story.append(Paragraph(f'&#x201C;{pull}&#x201D;', styles['pull_quote']))
        story.append(ThinRule(cw, color=GOLD, thickness=0.8))
        story.append(Spacer(1, 8))

    if worksheet:
        story.append(Spacer(1, 8))
        story.append(ThinRule(cw, color=LIGHT))
        story.append(Spacer(1, 6))
        story.append(Paragraph('WORKSHEET FIELDS', styles['sources_label']))
        story.append(Paragraph(worksheet, styles['sources']))


# ── All 24 playbook sections (source: veritas_owner_profit_control_playbook_25_pages.pdf) ──

# ── All 24 playbook sections — v2 with India-specific research ─────────────────
SECTIONS = [
    {
        'num': 2,
        'title': 'Executive decision brief',
        'subtitle': 'What to do if your hotel is busy but you cannot explain the cash',
        'paragraphs': [
            'India\'s 2025 hotel market reported strong headline figures. Horwath HTL tracked 64% '
            'national occupancy, INR 8,624 ADR and INR 5,522 RevPAR. Hotelivate\'s FY2024-25 data '
            'shows 68% occupancy, INR 8,432 ADR and INR 5,730 RevPAR across its hotel sample. '
            'These are tracked-market averages across star categories and cities. They are not '
            'targets for any individual property, and they say nothing about what the owner kept '
            'after commissions, payroll, utilities, debt service and drawings.',
            'The four linked questions an owner must answer every month: What demand did we capture — '
            'in paid room nights and realised rate after all discounts? What did it cost to acquire '
            'and serve that demand — including OTA commissions that in India can run 18-28% or higher '
            'with mandatory promotional participation, plus GST on that commission? Which other '
            'obligations were incurred — payroll, energy, debt service, capex? Which owner decisions '
            'can actually change the outcome from here?',
            'Demand is not revenue. Revenue is not profit. Profit is not cash. A hotel running at '
            '70% occupancy with a significant corporate receivables book, high OTA dependency and '
            'a diesel generator bill it cannot control can report a profitable month and simultaneously '
            'face a deteriorating cash position. Each link in the chain from room night to bank '
            'statement requires a reconciliation, not an assumption.',
            'Action plan: Today — commission finance, reservations and operations to agree one '
            'authoritative calendar-month source file with agreed definitions that everyone in the '
            'property uses. Within two weeks — identify the three largest unexplained differences '
            'between what was expected and what was received. Within 90 days — run three monthly '
            'owner decision meetings and document action owners, deadlines and outcomes for every '
            'commitment made in those meetings.',
        ],
        'pull': 'Demand is not revenue. Revenue is not profit. Profit is not cash.',
        'worksheet': None,
    },
    {
        'num': 3,
        'title': 'Method and evidence boundaries',
        'subtitle': 'Where this guide is evidence and where it is a proposal',
        'paragraphs': [
            'Market benchmarks in this playbook come from three principal sources. Horwath HTL\'s '
            'India Hotel Market Review 2025 (published 4 February 2026) covers a tracked sample '
            'of classified hotels across major Indian markets. Hotelivate\'s India Hotel Performance '
            'report covers FY2024-25 and uses a different sample and methodology. The Ministry of '
            'Tourism beta dashboard at data.tourism.gov.in/dashboard displays 2025 domestic tourism '
            'figures that carry a beta label and may be revised; all citations use the access date '
            'of 1 October 2026.',
            'These datasets report on national aggregates and tracked-hotel samples. They reflect '
            'classified hotels in covered cities and are not representative of the approximately '
            '74% of India\'s hotel room inventory that is unbranded and independent. An independent '
            'hotel in a tier-2 or tier-3 city, a pilgrimage destination or a leisure resort market '
            'should expect to see different ADR, occupancy and cost structures than the national '
            'averages in these reports.',
            'The checklists, metric definitions, worked arithmetic and 90-day plan in this guide '
            'are proposed operating tools. They have not been tested on Veritas clients as a package. '
            'No claim of a specific percentage improvement, a universal OTA commission level or '
            'an applicable cost threshold is made for any individual property. Local accountants '
            'and legal counsel should verify GST treatment, revenue recognition, contract terms, '
            'personal data obligations under the DPDP Act and any other regulatory requirement.',
            'If your property has no reliable channel data, finance records or staffing information, '
            'mark the result as unknown rather than estimating from an industry average. A clean '
            'data gap is more useful than a precise-looking figure built on an assumption. Ask '
            'finance to record the coverage gap, its cause and any restatement made later.',
        ],
        'pull': None,
        'worksheet': None,
    },
    {
        'num': 4,
        'title': 'The one-page owner control map',
        'subtitle': 'The six questions to answer every month',
        'paragraphs': [
            'Six questions form the structure of the monthly owner review. Each should be answerable '
            'from a named report, have a named data owner and generate at most one decision per month. '
            '1. What changed in paid room nights and average realised rate — after discounts, and on '
            'a tax-consistent basis across channels? 2. What changed in net acquisition cost per '
            'booking — including OTA commissions, GST on commissions, and direct marketing spend? '
            '3. What was the contribution from rooms, F&amp;B and events after direct and variable '
            'costs? 4. Which overhead or one-off item moved materially and why? 5. What happened '
            'to cash, outstanding receivables, advance deposits and any scheduled debt service? '
            '6. Which decisions require owner approval this month?',
            'Place last month, budget, same month last year and trailing twelve months side by side. '
            'Annotate distortions clearly: a festival date that fell in a different month, a '
            'renovation that took rooms out of service, a large group that inflated revenue and '
            'costs simultaneously. Comparisons are prompts for questions, not verdicts. A month '
            'that looks weaker than the prior year may reflect a Diwali shift or a school holiday '
            'timing change rather than an operating decline.',
            'Attach a data owner and a decision owner to each line of the control map. A GM may '
            'own the data on channel costs but the owner approves the decision to renegotiate '
            'an OTA contract. Separating data ownership from decision authority reduces the risk '
            'that information is filtered before it reaches the person who needs it — a pattern '
            'documented in Indian family-hotel governance research.',
            'Meeting rule: no more than three major actions approved per month, each with a '
            'measurement baseline, an implementing owner, a deadline and a review metric. '
            'Without those four elements the meeting produces discussion but not accountability.',
        ],
        'pull': 'A month that looks better may have deferred urgent maintenance or a seasonal date shift.',
        'worksheet': None,
    },
    {
        'num': 5,
        'title': 'Before measuring anything',
        'subtitle': 'Agree the definitions',
        'paragraphs': [
            'ADR = paid room revenue divided by paid room nights. The numerator excludes complimentary '
            'and staff rooms. The treatment of breakfast is the most common source of confusion: '
            'if breakfast is bundled into a package rate and not unbundled in the PMS, the resulting '
            'ADR figure is not comparable to an ADR calculated on room-only rates. Choose one '
            'consistent treatment and document it. Occupancy = paid occupied rooms divided by '
            'available saleable room nights. The denominator must reflect a consistent policy for '
            'out-of-order inventory and seasonal closure. RevPAR = paid room revenue divided by '
            'available saleable room nights on the same inventory basis.',
            'GST adds a layer of definition complexity specific to India. Hotel room tariffs above '
            'INR 7,500 carry 18% GST (with input tax credit available on business stays). Tariffs '
            'at or below INR 7,500 carry 5-12% GST with no ITC. A PMS report that includes '
            'GST in the revenue figure produces a different ADR than one that excludes it. '
            'OTA dashboards typically show gross amounts that include GST; net amounts remitted '
            'after the OTA deducts its commission and applicable taxes will differ. The same '
            'period from the same property will appear to have a different ADR depending on '
            'which report you read unless definitions are agreed in writing.',
            'A further complication arises with OTA TDS and TCS obligations. The Tax Deducted '
            'at Source and Tax Collected at Source provisions that apply to OTA transactions in '
            'India mean that the cash received from the OTA is not the same as the revenue '
            'recognised in the P&amp;L. Ask your accountant to document exactly which line '
            'in the ledger corresponds to which number in the PMS and OTA dashboard before '
            'comparing them.',
            'Write down which report is authoritative for each metric and reconcile it to the '
            'general ledger at least quarterly. The GM quoting PMS RevPAR and the accountant '
            'quoting net room revenue from the ledger can produce figures that diverge by '
            '10-20% from the same month — each correct under their own system. Reconciliation '
            'is the starting point for trustworthy measurement.',
        ],
        'pull': None,
        'worksheet': 'metric | formula | source report | tax treatment | frequency | data owner | '
                     'exclusions and caveats | sign-off date. Ensure GST treatment is documented '
                     'for every revenue metric. Have the GM and accountant both sign the metric '
                     'dictionary before any comparison across months or channels.',
    },
    {
        'num': 6,
        'title': 'The revenue-to-cash bridge',
        'subtitle': 'Follow one month from guest to bank',
        'paragraphs': [
            'Start with total room and non-room revenue earned and recognised in the period under '
            'the property\'s accounting policy. Then work through each adjustment in order. '
            'GST collected on behalf of the government passes through the P&amp;L but is not '
            'the hotel\'s income; depending on the accountant\'s method, it may inflate gross '
            'revenue in some reports. OTA commissions and promotional discounts reduce the net '
            'figure. In India the major OTAs — MakeMyTrip, Goibibo, Booking.com, Agoda — '
            'may apply a commission, then add GST on that commission as a further charge. '
            'TDS deducted at source by the platform is a cash flow item, not a P&amp;L item, '
            'but it reduces the cash received this month even though it is recoverable on filing.',
            'Continue down the bridge: direct fulfilment costs booked to the reservation, '
            'payment processing costs (UPI typically carries low or zero MDR; card payments '
            'carry 1-2%), refunds and cancellations matched to the period. The result at '
            'this stage is net room contribution before overhead. Corporate account receivables '
            'are a common cash timing gap in Indian hotels: a corporate at 30-45 day credit '
            'terms means November occupancy may generate cash only in December or January.',
            'Converting to cash requires also reconciling advance event deposits received but '
            'not yet earned, payroll and PF obligations due, GST remittances due to the '
            'government, contractor bills outstanding, and any scheduled EMI or loan repayment. '
            'A seasonal property in Goa or a Rajasthan heritage hotel may receive large advance '
            'deposits from international wholesalers 90-180 days before the season, creating '
            'a cash inflow that appears months before the corresponding revenue is earned.',
            'The owner who can run this bridge every month, with a named person responsible '
            'for each line, has the core of a functioning financial oversight system. The owner '
            'who cannot run it has a reporting problem regardless of what the occupancy figure shows.',
        ],
        'pull': 'The owner who cannot run this bridge has a reporting problem regardless of what the occupancy figure shows.',
        'worksheet': 'ledger revenue | OTA commissions | GST on commissions | TDS deducted by OTAs | '
                     'direct costs | net contribution | receivables movement | deposits movement | '
                     'GST remittance due | EMI/debt service | capex payments | bank balance check.',
    },
    {
        'num': 7,
        'title': 'Worked example: a full-looking hotel',
        'subtitle': 'Fictional 50-room property in a tier-2 Indian market — not a benchmark',
        'paragraphs': [
            'Suppose a fictional 50-room hotel reports 80% occupancy in November — 1,200 paid '
            'room nights from 1,500 available. The PMS shows a rack ADR of INR 4,500, giving '
            'gross room revenue of INR 54,00,000. This is the number that produces congratulations. '
            'None of it has been tested against the cost of acquiring and serving those bookings.',
            'Suppose 500 of the 1,200 room nights came via MakeMyTrip at an effective net rate '
            'after all discounts of INR 3,600, with a 20% commission plus GST on commission '
            'applying — reducing the net receipt to roughly INR 2,765 per room night for those '
            '500 nights. Suppose a further 300 nights came via a corporate account that books '
            'at INR 3,800 on 45-day credit terms: the cash from those stays will arrive in '
            'January. The remaining 400 nights came direct at or near rack rate. Blended realised '
            'rate across all 1,200 paid nights may be materially below the reported ADR.',
            'What remains outside this illustration: payroll across departments (national '
            'averages suggest 1.0-1.2 staff per available room for mid-market properties), '
            'electricity (8-12% of revenue for a 50-room metro property with HVAC), F&amp;B '
            'and event costs, maintenance, finance costs, statutory contributions including PF '
            'and ESI, and any GST mismatch between ITC available and liability due. A property '
            'at 80% occupancy can produce a healthy EBITDA or a cash crisis depending on how '
            'these costs align with its revenue timing.',
            'Use this logic with your own actual realised rates — not rack rates, not '
            'contracted rates — and with all channel costs and GST treatment documented '
            'consistently. Compare any incremental channel decision only if you have evidence '
            'that a different channel could have sold those same rooms. Do not apply the '
            'national average RevPAR as a cost benchmark for your property.',
        ],
        'pull': None,
        'worksheet': None,
    },
    {
        'num': 8,
        'title': 'Channel economics',
        'subtitle': 'A booking source is a cost-and-demand relationship',
        'paragraphs': [
            'India\'s OTA market is dominated by MakeMyTrip and Goibibo (now one group), '
            'Booking.com and Agoda, with Airbnb and OYO relevant in specific segments. '
            'Published commission rates understate the true cost. MakeMyTrip / Goibibo '
            'typically charge 18-28% base commission; mandatory participation in promotional '
            'events, matched discounting obligations and GST on the commission can push the '
            'total OTA cost to 25-40% of gross room revenue in active promotional periods. '
            'OYO contracts for independent hotels have been reported at 25-35% of revenue. '
            'Know your actual contract terms before estimating channel cost.',
            'WhatsApp and phone enquiries, historically the dominant direct channel for '
            'independent hotels in India, have costs that are often invisible in the channel '
            'ledger: receptionist and reservations time, the rate at which enquiries are '
            'converted without follow-up, and the payment friction when guests expect a bank '
            'transfer but the property\'s UPI QR code is for a personal account rather than '
            'the business. A missed WhatsApp enquiry has a cost that does not appear in any '
            'report but is real.',
            'Direct bookings through the property website require: a functioning online booking '
            'engine with real-time inventory, a competitive rate parity policy, a payment '
            'gateway that accepts the card types Indian corporate and leisure travellers use, '
            'and a fast-response protocol for enquiries that arrive through the "contact us" '
            'form. The marginal cost of a well-managed direct booking is low but the investment '
            'to establish this infrastructure is not zero.',
            'Decision process: list each channel by volume and measure contribution on a tax-'
            'consistent basis. Identify the single channel with the weakest measured contribution '
            'relative to the demand it provides. Investigate whether the weak result reflects '
            'the commission structure, unfavourable rate parity terms, different guest behaviour '
            '(shorter stays, higher cancellations) or a cost allocation error. Make one specific '
            'change, measure over two to three months, then decide.',
        ],
        'pull': None,
        'worksheet': 'channel | nights | gross ADR | effective net rate | total channel cost incl. '
                     'GST | cancellation rate | payment timing | net contribution per night | '
                     'trailing 3-month trend.',
    },
    {
        'num': 9,
        'title': 'Rate and inventory',
        'subtitle': 'Price tomorrow, not last year\'s headline',
        'paragraphs': [
            'India\'s city markets behave very differently. Horwath HTL CY2024 data shows Mumbai '
            'leading occupancy among major tracked cities at 73-77%, Delhi at 68-72%, Bengaluru '
            'at 68-70%, and Goa and Udaipur showing strong leisure-season ADR driven by high-end '
            'supply. Hotelivate FY2024-25 data places Mumbai RevPAR at INR 9,494 and Udaipur ADR '
            'at INR 15,946. A corporate transit hotel near Bengaluru\'s Kempegowda airport and a '
            'heritage haveli in Udaipur\'s Old City operate in separate demand universes. National '
            'figures cannot price either one.',
            'A rate decision should start with booking pace for the specific date: rooms on books '
            'versus the same date last year and the expected pace at this point in the lead time. '
            'Then consider local demand drivers specific to your market: MICE and corporate events '
            'in business cities, festival calendar (Diwali, Navratri, Durga Puja timings vary '
            'by city and year), wedding season concentration in October-February, school holiday '
            'patterns, and pilgrimage seasons for relevant destinations.',
            'Common Indian hotel pricing mistakes: applying a uniform rate increase across all '
            'channels after a good month, failing to close availability to high-discount OTA '
            'channels on locally identified peak dates, and discounting early to fill rooms when '
            'local demand evidence suggests the booking will come closer to the date. Build a '
            'local demand calendar with the key dates and the expected direction of each, and '
            'review rates against it weekly rather than monthly.',
            'Rate floor decisions for owner protection: if a floor is set for brand or contract '
            'reasons, document it explicitly. Unexamined rate floors set three years ago at '
            'pandemic-era levels may now leave significant revenue on the table in peak periods. '
            'Review every floor rate with current demand evidence at the start of each season.',
        ],
        'pull': 'A corporate hotel near Bengaluru airport and a heritage haveli in Udaipur operate in separate demand universes.',
        'worksheet': 'stay date | local demand drivers | rooms on books | pickup vs prior year | '
                     'offered rate by channel | floor rate (if any) | post-stay contribution '
                     'review | action owner.',
    },
    {
        'num': 10,
        'title': 'F&amp;B and banquet contribution',
        'subtitle': 'Turnover is not the same as contribution',
        'paragraphs': [
            'Indian weddings are a structurally significant demand driver. HVS ANAROCK identifies '
            'the Indian wedding market — estimated at over USD 50 billion annually — as a key '
            'hospitality revenue source, concentrated in the October-February season with a second '
            'peak around the monsoon break. For a property with banquet space, a busy wedding '
            'weekend can look like the best month of the year in the revenue line and '
            'simultaneously be one of the worst in contribution once variable labour, decoration '
            'obligations, agency chef costs, utility consumption, advance-deposit refund risk and '
            'displaced regular room inventory are accounted for.',
            'GST treatment for hotel F&amp;B is layered. A restaurant that qualifies as a '
            '"specified premises" hotel (room tariff above INR 7,500) charges 18% GST on F&amp;B '
            'with ITC available. Alcohol sits outside the GST framework and is taxed under state '
            'excise; the rates vary by state and add complexity to multi-state event quotations. '
            'A banquet with a bar that crosses state-excise thresholds requires a separate '
            'licence in many states. Verify the current position with qualified local counsel '
            'before including alcohol in a minimum spend commitment.',
            'Before quoting any event, sales and finance should agree on: venue and food revenue '
            'separately; raw material and direct kitchen cost; overtime and agency staff; '
            'equipment, decoration and third-party obligations; rooms blocked and their release '
            'deadline; and the GST and excise treatment of each revenue line. The minimum spend '
            'commitment should reflect a contribution floor after all direct costs, not a revenue '
            'floor before any costs.',
            'After each major event, compare actual contribution to the quoted estimate. The '
            'pattern of variances over a season will show whether the property is '
            'systematically under-pricing agency labour, underestimating food waste at large '
            'covers, or accepting room release terms that allow a wedding client to hold '
            'inventory that is then returned too late to resell.',
        ],
        'pull': None,
        'worksheet': 'event date | venue + food contracted | rooms blocked | release date | '
                     'agency labour estimated | actual labour | food cost variance | '
                     'alcohol revenue | excise/GST compliance verified | net contribution.',
    },
    {
        'num': 11,
        'title': 'Payroll and service',
        'subtitle': 'Do not fix a wage problem by breaking the guest experience',
        'paragraphs': [
            'Indian hospitality has a structural staffing challenge. National attrition in the '
            'industry runs approximately 25-35% annually, with front-of-house and food service '
            'roles turning over fastest. The cost of attrition — recruitment fees, induction, '
            'reduced productivity during the learning curve, and overtime carried by the '
            'remaining team — is often higher than the wage saving from running lean. Before '
            'targeting a headcount reduction, calculate the full cost of the current attrition '
            'rate and compare it to the proposed saving.',
            'Benchmarks from the available research suggest mid-market Indian hotels run at '
            'approximately 1.0-1.2 permanent staff per available room, excluding agency and '
            'seasonal workers. Payroll as a percentage of revenue in the sector ranges '
            'from roughly 20-30% across star categories, with lower-category properties '
            'tending toward the higher end of this range as a percentage because fixed '
            'staffing levels do not scale proportionally with lower ADR. Budget labour cost '
            'by activity driver — occupied rooms, F&amp;B covers, event headcount — not simply '
            'as a fixed percentage of total revenue.',
            'Agency and contractual labour is widely used in Indian hotel operations for F&amp;B '
            'service, housekeeping and security. The ESI, PF and minimum-wage compliance '
            'obligations for contractual workers employed through a labour contractor are a '
            'shared liability in many interpretations of Indian labour law; verify the current '
            'legal position with a qualified HR or legal adviser before assuming a contractor '
            'arrangement eliminates the employer\'s obligations.',
            'Decision rule: test any roster or process change for a defined pilot period — four '
            'to six weeks — with an owner-approved guest service floor. Measure guest complaints, '
            'unresolved incidents and overtime cost during the pilot. Restore or revise the '
            'change if the service floor is breached. A reduction in the wage line that produces '
            'a parallel increase in refunds and review-score deterioration has not improved '
            'the business.',
        ],
        'pull': None,
        'worksheet': None,
    },
    {
        'num': 12,
        'title': 'Energy and maintenance',
        'subtitle': 'Separate consumption from capacity and repair needs',
        'paragraphs': [
            'Energy is a significant and variable cost for Indian hotels. Electricity costs for '
            'a 30-room property in a major metro can range from INR 1.5 lakh to INR 3 lakh '
            'monthly depending on the city\'s tariff band, power factor penalties, the HVAC '
            'load and the DG set dependency during load-shedding. Energy as a percentage of '
            'total revenue has been estimated at 8-12% for mid-market urban properties. '
            'This figure is not controllable at the level of a single monthly budget line '
            'without understanding the consumption drivers — HVAC in vacant rooms, pool '
            'heating, kitchen equipment, and DG fuel cost during power outages.',
            'Indian commercial electricity tariffs are set by state regulators and vary '
            'substantially by state, demand level and time-of-day category. A power factor '
            'surcharge can add 5-15% to the base electricity bill in some states if reactive '
            'power demand is not corrected. Tariff revisions, often announced mid-year by '
            'state electricity boards, can move the energy cost without any change in '
            'consumption. Annotate the energy line in the owner review with the current '
            'applicable tariff and any scheduled revision before attributing a variance to '
            'operating behaviour.',
            'DG fuel cost deserves a separate line item. An urban property that runs its '
            'generator for 8-10 hours a day during state power cuts incurs a fuel cost that '
            'does not appear in the electricity bill but can equal 2-4% of revenue. Properties '
            'in tier-2 cities with less reliable grid supply should track DG hours, fuel '
            'consumption per hour and average load alongside the state electricity bill to '
            'get a complete energy picture.',
            'Build a maintenance register with columns for: issue, safety and compliance risk '
            'level, estimated cost, room nights affected, contractor status, approval required '
            'and approval date. A month with lower energy spend because the air-conditioning '
            'plant was left partially operational to defer a repair is not an efficiency gain; '
            'it is a transferred cost and guest experience risk. Track out-of-order rooms '
            'explicitly rather than leaving them as invisible inventory gaps.',
        ],
        'pull': 'A month with lower energy spend because urgent maintenance was deferred is not an operating improvement — it is a transferred cost.',
        'worksheet': None,
    },
    {
        'num': 13,
        'title': 'Cash, receivables and deposits',
        'subtitle': 'Why a good P&amp;L can coexist with a bad bank balance',
        'paragraphs': [
            'Map all the timing gaps between recognised profit and available cash. For most '
            'independent Indian hotels the critical gaps are: corporate and travel agent '
            'receivables on 30-60 day terms; advance deposits from event bookings — often '
            '25-50% of event value — held for months before the event date; GST remittances '
            'due to the government monthly or quarterly; contractor bills and supplier '
            'payables; and EMI or term loan repayments on the property financing.',
            'A hotel that is selling 70% occupancy to a strong corporate account mix on '
            '45-day credit, collecting large wedding deposits for Q1 events in September-'
            'October, and servicing a construction loan with a year-end balloon may report '
            'a healthy operating profit for November and simultaneously face a January cash '
            'gap. The P&amp;L will not warn the owner. Only a cash bridge maintained from '
            'month to month will.',
            'Common cash management mistakes in independent Indian hotels: treating advance '
            'event deposits as operating cash and spending them before the event earns them; '
            'allowing the corporate receivables book to age beyond 90 days without a formal '
            'collection process; and conflating the GST collected from guests with the '
            'hotel\'s own revenue, then being surprised by the quarterly GST remittance. '
            'Each of these is correctable with a documented process and a named accountable '
            'person.',
            'Have finance maintain a rolling 13-week cash forecast: opening cash, expected '
            'receipts by confidence level, committed outflows that cannot be deferred, and '
            'discretionary outflows that could be moved. Reconcile receivables aging at '
            'every owner meeting. Any corporate account overdue beyond 60 days should have '
            'a named collections owner and documented follow-up status. Deposits for events '
            'more than six months away should have explicit cancellation and refund terms '
            'approved by the owner at the time of booking.',
        ],
        'pull': 'A hotel can show healthy monthly profit while moving toward a cash crisis. The P&amp;L will not warn the owner.',
        'worksheet': 'week | opening cash | certain receipts | probable receipts | '
                     'GST remittance due | EMI/loan payments | committed supplier payments | '
                     'discretionary payments | forecast closing cash.',
    },
    {
        'num': 14,
        'title': 'Capex and return',
        'subtitle': 'Ask what the investment changes and when',
        'paragraphs': [
            'For any proposed capital expenditure, distinguish between essential maintenance '
            '(restoring what exists to its designed condition), essential compliance work '
            '(fire safety, structural obligations, regulatory standards), growth investment '
            '(adding capability or capacity that generates new revenue) and discretionary '
            'upgrade (improving to a higher standard to support a rate premium). Each '
            'category has a different approval logic, a different risk profile and a different '
            'measure of success.',
            'Horwath HTL estimates India\'s branded pipeline at approximately 144,000 rooms, '
            'while cautioning that not all signed pipeline will open on schedule and that '
            'approximately 300,000 is a more realistic near-term estimate than the theoretical '
            '360,000. HVS ANAROCK reports 64,118 keys signed in 2025 across 586 branded '
            'properties, with 42% of new signings in the midscale segment and 44% of pipeline '
            'heading to tier-3 and tier-4 cities. An independent hotel owner who commits to '
            'a major renovation in response to a brand announcement may be reacting to a '
            'project that will not open for three years and will target a different segment '
            'and guest type than their current business.',
            'For a proposed room renovation or outlet upgrade, the approval memo should contain: '
            'total cost and contingency, disruption to available inventory during construction, '
            'realistic rate premium achievable after completion based on comparable properties '
            '(not renovation contractor estimates), ongoing maintenance obligation for the '
            'new condition, financing method and cost, cash timing of outflows, and a downside '
            'case if demand uplift is 30% below projection.',
            'A competitor\'s public rate after renovation does not prove you can achieve the '
            'same rate. It tells you what they are asking. Your achievable rate depends on '
            'your location, product, service reputation, segment access and the distribution '
            'channels you have built. Seek independent financial and technical advice before '
            'committing to any material capex; this guide does not substitute for it.',
        ],
        'pull': None,
        'worksheet': 'decision requested | cost estimate and contingency | alternative of doing nothing | '
                     'revenue assumption and evidence basis | cash flow timing | downside case | '
                     'accountable owner | review date and metric.',
    },
    {
        'num': 15,
        'title': 'Guest mix and local demand',
        'subtitle': 'A national tourist visit is not your booking',
        'paragraphs': [
            'India\'s domestic tourism figures are substantial. The Ministry of Tourism\'s beta '
            'dashboard reports approximately 4,287 million domestic tourist visits in 2025, '
            'up 45.55% on the prior year. Corporate travel spend in India was estimated at '
            'USD 38.3 billion in 2024 and is growing at approximately 15.5% annually — roughly '
            'twice the global average. The Indian wedding and events market represents a '
            'multi-billion dollar demand source concentrated in October-February. These '
            'macro figures describe aggregate demand, not hotel room nights, and not the '
            'demand available to a specific property.',
            'A domestic tourist visit includes day trips, visits to family, pilgrimage travel '
            'completed without a hotel stay, and accommodation in informal and unregistered '
            'facilities. The Ministry and HVS ANAROCK use different methodologies and their '
            '2025 estimates differ (approximately 4,287 million versus 4,548 million). '
            'Neither figure should be applied as a multiplier to room night projections without '
            'a clear understanding of the conversion rate from domestic visits to hotel room '
            'nights in your specific destination category.',
            'Build the guest mix analysis from your own booking records. List actual booking '
            'sources and define segments that are meaningful for your property: domestic '
            'leisure, domestic corporate (direct and managed), pilgrimage, weddings and '
            'social events, group tours and MICE, inbound international by source market. '
            'For each segment record booking window, length of stay, realised rate, channel '
            'cost, cancellation rate and ancillary spend. Identify which segments are growing, '
            'which are declining, and which months each segment dominates.',
            'Different Indian destinations behave very differently. A business hotel in '
            'Bengaluru\'s Whitefield tech corridor has demand driven by IT company travel '
            'policies and project cycles. A fort-palace hotel in Rajasthan draws international '
            'leisure guests and Indian destination weddings with very different booking windows '
            'and rate dynamics. A pilgrimage destination near Varanasi or Tirupati has demand '
            'that is relatively inelastic on rate and very concentrated on festival dates. '
            'Verify the local demand calendar before projecting.',
        ],
        'pull': None,
        'worksheet': 'segment | room nights | realised ADR | channel cost | LOS | '
                     'cancellation rate | ancillary revenue | seasonality peak | next test.',
    },
    {
        'num': 16,
        'title': 'Forecasting without false precision',
        'subtitle': 'Three cases are better than one immaculate spreadsheet',
        'paragraphs': [
            'Build three explicit cases for each quarter: base, downside and upside. Base case '
            'reflects the most probable outcome given current bookings on the books, historical '
            'patterns for the period, and known demand drivers. Downside reflects a plausible '
            'adverse scenario — a direct flight suspension reducing leisure arrivals, a key '
            'corporate client cutting travel, a new branded property opening earlier than '
            'expected, or a festival date moving into a different month. Upside reflects a '
            'favourable scenario — a large government or MICE event not yet confirmed, a '
            'competitor closing for renovation, a new infrastructure opening that accelerates '
            'demand.',
            'State key assumptions explicitly: projected occupancy by segment, assumed ADR '
            'by channel including the OTA commission treatment, specific events included or '
            'excluded, new supply opening assumptions and timing, payroll and utility cost '
            'assumptions. Assign a named person and a review date to each material assumption. '
            'A forecast without named assumptions is not a forecast; it is a wish.',
            'Indian seasonal dynamics require careful handling. The October-February window '
            'combines peak wedding season, domestic leisure demand and (for many markets) '
            'peak international arrivals. The April-June period is typically the weakest '
            'in most markets outside leisure and religious destinations. The monsoon period '
            '(June-September) behaves very differently across destination types. Build '
            'seasonality explicitly into the forecast rather than applying a uniform month-on-'
            'month growth rate from a different season.',
            'Month-end discipline: compare actuals to the forecast, identify which assumptions '
            'were wrong and by how much, revise the forward months, and preserve the original '
            'forecast for tracking bias. A forecast that is consistently optimistic on '
            'corporate bookings or consistently underestimates energy costs has a structural '
            'problem that improving the spreadsheet will not fix.',
        ],
        'pull': 'A forecast without named assumptions is not a forecast; it is a wish.',
        'worksheet': None,
    },
    {
        'num': 17,
        'title': 'Deciding who decides',
        'subtitle': 'The owner, GM and adviser need a shared map',
        'paragraphs': [
            'A governance map states who recommends, who approves, who implements and who '
            'reviews each category of material decision. Without this map, good analysis '
            'stalls because no one is certain who has authority to act, and poor decisions '
            'proceed because no one is certain who has authority to stop them. The map does '
            'not need to be complex; it needs to be explicit and shared with the operating team.',
            'The owner typically retains: the annual budget and any revision that crosses a '
            'materiality threshold; rate floors and ceilings that govern channel strategy; '
            'capex above an agreed value; key personnel appointments; and any legal or '
            'financial commitment that creates an obligation for the company. The GM manages '
            'daily operations, pricing within approved parameters, routine supplier relationships '
            'and service standards. An external adviser analyses, recommends and tracks outcomes '
            'within a written mandate that specifies scope, data access and limits of authority.',
            'Indian family hotels often have informal approval routes running alongside the '
            'formal chart. A senior family member not in a day-to-day role may override '
            'operational decisions on an ad hoc basis. Research on Indian family business '
            'governance documents these parallel structures and their costs — delayed '
            'decisions, team confusion and rework — without prescribing a single resolution. '
            'The practical aim is to make the informal routes visible so they can be '
            'managed rather than remaining as unpredictable overrides that undermine '
            'the GM\'s effectiveness.',
            'RACI table for the five to seven most frequent decisions at your property: '
            'rate exceptions, hiring above a threshold, vendor contracts above a value, '
            'refunds above an amount, capex proposals, monthly reporting sign-off and '
            'data access for an external adviser. For each, document who is Responsible, '
            'Accountable, Consulted and Informed. Resolve disagreements about this table '
            'before any advisory engagement begins.',
        ],
        'pull': None,
        'worksheet': None,
    },
    {
        'num': 18,
        'title': 'The monthly owner meeting',
        'subtitle': 'Forty-five minutes for decisions, not a theatre of charts',
        'paragraphs': [
            'Send the owner pack two business days before the meeting. The pack must contain: '
            'the revenue-to-cash bridge for the month just closed; the three largest exceptions '
            'to plan; the action register from the previous meeting with confirmed status of '
            'each commitment; and the decisions required at this meeting with a named proposer '
            'for each. If the GM and the finance lead disagree on any figure in the pack, '
            'record the disagreement in the pack itself rather than resolving it out of '
            'the owner\'s sight.',
            'Suggested agenda timing for a 45-minute meeting: 5 minutes on actions from '
            'the previous meeting — completed, delayed or closed? 10 minutes on commercial '
            'performance — rooms, F&amp;B, events, and the bridge from revenue to cash. '
            '10 minutes on costs and cash — energy, payroll, receivables ageing, upcoming '
            'obligations. 10 minutes on exceptions — the three things that diverged most from '
            'plan and what was done or proposed. 10 minutes on decisions required, with '
            'each decision named and an implementing owner confirmed before the meeting closes.',
            'Common failure modes in Indian owner-hotel meetings: the monthly review becomes '
            'a performance presentation by the GM rather than a decision meeting; exceptions '
            'are explained away rather than investigated; a family member outside the formal '
            'governance structure reverses a decision made at the meeting; the owner pack '
            'is built for operations rather than ownership, with no shared external benchmark. '
            'Each of these can be addressed structurally — but only if '
            'it is first named explicitly.',
            'A good meeting can end with "we do not know yet." Record the missing information, '
            'the person responsible for obtaining it and the deadline. Verify at the next '
            'meeting whether the gap was closed. Avoid the common pattern of unexplained '
            'gaps that persist for months because no one was formally tasked with resolving them.',
        ],
        'pull': 'A good meeting can end with "we do not know yet."',
        'worksheet': None,
    },
    {
        'num': 19,
        'title': 'The action register',
        'subtitle': 'An insight without an owner expires quickly',
        'paragraphs': [
            'Create one shared register visible to the owner, GM and any adviser. Each row '
            'represents a single action with: the issue and evidence; the business impact if '
            'unaddressed; the proposed response and its alternatives; the approving party; '
            'the implementing owner; the due date; the metric and baseline for measuring '
            'success; the next checkpoint date; status; and the documented result when '
            'closed. Each field must be completed — a row without a due date and a metric '
            'baseline is a discussion note, not an action.',
            'Limit active priorities to what the team can execute alongside existing '
            'obligations. Three to five active actions per month with clear owners and '
            'deadlines will produce more measurable improvement than a longer list with '
            'diffuse accountability. In a small Indian hotel team where the front office '
            'manager may also handle reservations and the GM is part of guest service '
            'coverage, an overloaded action register is a reliable predictor of nothing '
            'getting done.',
            'Distinguish between completing an activity and achieving an outcome. "Reservations '
            'team briefed on direct enquiry follow-up protocol" is an activity. "Direct '
            'booking conversion from WhatsApp enquiries increased from X to Y over 60 days" '
            'is an outcome. Document both, because an activity completed without an outcome '
            'needs a different response than an activity that was never implemented.',
            'Red flags in a poorly functioning register: actions without deadlines; owners '
            'without the authority to implement; metrics without a baseline; actions that '
            'have been carried forward from more than two months without resolution; and '
            'a status column that reads "green" with no supporting data. Any of these is '
            'a signal that the register is being maintained for appearance rather than '
            'accountability.',
        ],
        'pull': None,
        'worksheet': 'issue | evidence | impact | proposed response | approving party | '
                     'implementer | due date | metric and baseline | checkpoint | status | result.',
    },
    {
        'num': 20,
        'title': 'Protecting the data',
        'subtitle': 'Confidentiality is operational, not decorative',
        'paragraphs': [
            'A profitability review involves sensitive commercial information: payroll details '
            'that cannot be circulated freely within the team, guest payment and preference '
            'data that carries privacy obligations (including under the Digital Personal Data '
            'Protection Act 2023 as implemented), vendor and supplier terms that may contain '
            'confidentiality clauses, and banking and financing information that has no '
            'business being held on unsecured platforms. Before sharing any material with '
            'an adviser or external party, agree explicitly on scope, secure transfer method, '
            'retention period, deletion process and permitted uses.',
            'Data shared via ordinary email attachments, messaging apps including WhatsApp, '
            'or public cloud folders without access controls is not protected. An initial '
            'enquiry form on a consultant\'s website is not an appropriate channel for '
            'financial statements. A WhatsApp message containing monthly P&amp;L figures '
            'is not a secure data transfer — it is a common practice in the Indian hotel '
            'sector that creates real legal and commercial exposure.',
            'The Digital Personal Data Protection Act 2023 imposes obligations on the '
            'collection, processing and storage of personal data. Its implementation '
            'is evolving; verify the current applicable rules with qualified Indian legal '
            'counsel before designing any data flow that involves guest personal information, '
            'employee personal data or financial data that can be traced to an individual. '
            'This guide does not certify compliance with any data protection framework.',
            'Store only necessary copies of sensitive information. Remove personal guest '
            'identifiers from any sample dashboard or worked example before sharing for '
            'review or illustration. Reconcile the privacy notice the hotel presents to '
            'guests with the actual data practices in use — including data shared with OTA '
            'platforms as part of the booking process.',
        ],
        'pull': None,
        'worksheet': 'signed scope of data access | named recipients | access rights | '
                     'secure transfer method | retention period | deletion process | '
                     'permitted analyses | revocation path | DPDP compliance confirmed.',
    },
    {
        'num': 21,
        'title': 'Where an adviser can add value',
        'subtitle': 'When to seek help, and when not to',
        'paragraphs': [
            'Independent oversight may help when: the owner cannot reconcile the reports '
            'being provided; the GM needs analytical support to develop and implement a '
            'commercial plan; or a significant brand affiliation, management contract or '
            'capital decision requires analysis from a party without a vested interest in '
            'the outcome. HVS ANAROCK reports 64,118 branded keys signed in 2025: the '
            'question of whether an independent property should affiliate with a brand is '
            'becoming more frequent in tier-2 and tier-3 markets as networks expand. '
            'This decision requires a full financial model — not just a projected ADR uplift '
            '— before any commitment is made.',
            'An advisory engagement adds less value when: the data needed for analysis '
            'is inaccessible or unreliable; management authority is contested and no one '
            'with implementation authority will act on a recommendation; or the intended '
            'outcome is to replace the current team without addressing the governance '
            'and oversight gaps that will persist after a personnel change.',
            'Before engaging an adviser, request a sample deliverable from a comparable '
            'engagement. Ask what data will be required and how it will be transferred '
            'securely. Ask who will do the analytical work. Ask whether the adviser has '
            'any referral relationship with brands, lenders or technology suppliers whose '
            'services might be recommended. Ask the fee basis and what the exit process '
            'looks like if the engagement is not working.',
            'Start with a bounded assignment: defined scope, defined time period, defined '
            'deliverable. Require a written finding and a named action owner for every '
            'recommendation. Continue only if the process demonstrably improves the '
            'reliability of owner decisions. Avoid fee structures tied to metrics the '
            'adviser cannot materially influence or independently verify.',
        ],
        'pull': 'Start with a bounded assignment. Require a written finding and a named action owner for every recommendation.',
        'worksheet': None,
    },
    {
        'num': 22,
        'title': 'The 90-day implementation plan',
        'subtitle': 'Four practical phases',
        'paragraphs': [
            'Days 1-14: Foundation. The owner names a sponsor, a GM point of contact and a '
            'finance lead. The three agree on metric definitions (or document their own '
            'alternatives to those in this guide), the scope of data to collect and the '
            'access permissions required. They retrieve the last 12 months of operating '
            'and finance records and document gaps, restatements and data quality issues. '
            'If data is unavailable for more than three months back, this becomes the '
            'first action item before analysis proceeds. Establish the data-sharing '
            'protocol and confirm GST treatment consistency before any comparison is made.',
            'Days 15-30: Diagnosis. Reconcile revenue, channel costs and cash for the '
            'most recent complete month using the bridge in this playbook. Identify the '
            'three largest exceptions — where actual results diverged most from expectation. '
            'Produce a one-page decision brief: what we found, what it means, what owner '
            'decision it requires. This becomes the agenda for the first monthly owner '
            'meeting.',
            'Days 31-60: Testing. Take two to three approved actions from the decision '
            'brief and run structured tests: a revision to the OTA release policy for '
            'peak dates, an improved corporate receivables follow-up process, a change '
            'to the WhatsApp enquiry conversion protocol, or a review of the energy '
            'management schedule for low-occupancy nights. Record the baseline before '
            'the test, the guardrails that make it reversible, and the metric that will '
            'show whether it worked.',
            'Days 61-90: Review. Compare performance against the prior year period, '
            'noting distortions. Assess the tested actions against their baselines. '
            'Establish the recurring owner meeting, the action register and the rolling '
            'cash forecast as permanent operating disciplines. Do not promise a '
            'financial uplift at the end of 90 days. The first success condition is '
            'reliable data and decisions based on it.',
        ],
        'pull': 'Do not promise a financial uplift at the end of 90 days. The first success condition is reliable data and clear decisions.',
        'worksheet': None,
    },
    {
        'num': 23,
        'title': 'Owner worksheets',
        'subtitle': 'Copy these fields into a spreadsheet or board pack',
        'paragraphs': [
            'Worksheet A — Metric dictionary: for each metric used in the owner pack record '
            'the name, numerator, denominator, source report, GST treatment, any exclusions, '
            'the data owner, and the date agreed and signed. Any change must be dated so '
            'that year-on-year comparisons can be restated if needed. Worksheet B — Channel '
            'ledger: channel name, room nights, gross ADR, effective net rate after '
            'discounts and commissions, GST on commissions, TDS deducted, cancellation '
            'rate, payment timing, and net contribution per night. Maintain month by month '
            'over a rolling 12 months so trends are visible.',
            'Worksheet C — Cash bridge: start with the accounting result for the period, '
            'adjust for receivables movement, payables movement, GST remittance paid, '
            'debt service and EMI payments, advance deposits received or earned, capex '
            'outflows, owner drawings, and any other balance-sheet item that explains '
            'the difference between P&amp;L profit and the movement in the bank balance. '
            'End with the bank balance reconciliation.',
            'Worksheet D — Decision log: date, evidence presented, options considered, '
            'the approving owner, the implementer, the deadline and the documented outcome. '
            'Worksheet E — Risk log: nature of the data gap or exposure, service risk if '
            'unaddressed, financial exposure estimate, proposed mitigation and escalation '
            'path. Worksheet F — Energy register: monthly electricity units consumed, '
            'DG hours and fuel cost, tariff band applicable, water consumption, and '
            'any tariff revision or power factor penalty noted.',
            'Give each worksheet a version number and retain prior versions so that a '
            'restatement can be traced. Use a worked fictional row to train the team '
            'on the format, then delete it before loading real property data. Have '
            'the finance lead validate the classifications against the general ledger '
            'before worksheets are used in any owner meeting.',
        ],
        'pull': None,
        'worksheet': None,
    },
    {
        'num': 24,
        'title': 'Owner readiness self-assessment',
        'subtitle': 'Score the system, not the people',
        'paragraphs': [
            'Rate each of nine areas on a scale of 0 to 2. Score 0 if there is no reliable '
            'record. Score 1 if there is some evidence but it is not consistently reconciled '
            'or lacks a named review owner. Score 2 if there is a defined source, a named '
            'data owner and a regular review cadence. Maximum score: 18. This is an '
            'illustrative triage checklist, not a validated hotel-performance instrument.',
            'The nine areas: 1. Room inventory and ADR — can you produce a reconciled ADR '
            'figure for any month in the last 12, with GST treatment documented? 2. Booking-'
            'channel costs — do you have a complete channel ledger for the last three months '
            'including OTA commission and GST on commission? 3. F&amp;B and event contribution '
            '— can you show the actual contribution for the last three major events? '
            '4. Payroll versus demand — do you compare paid hours and agency costs to '
            'occupied rooms and covers each month? 5. Cash and receivables — can you '
            'reconcile profit to cash movement for the last complete month?',
            '6. Energy register — do you track electricity, DG hours and water separately '
            'and compare them to the applicable tariff? 7. Capex register — is there a '
            'current register with approval status for all projects above your threshold? '
            '8. Decision rights — is there a written RACI for the five decisions most '
            'frequently made at your property, agreed by owner and GM? 9. Action follow-'
            'through — what percentage of actions from the last three owner meetings were '
            'completed on time with the committed outcome documented?',
            'A score below 10 suggests the first priority is repairing data and roles '
            'before making pricing or investment recommendations. A score above 14 does '
            'not mean the business is profitable; it means decisions are more likely to '
            'be based on reliable information. Present the self-assessment to the GM and '
            'finance lead separately and discuss differences; do not use it to allocate '
            'blame for historical gaps. Rescore after 90 days and track the trajectory.',
        ],
        'pull': 'A high score does not mean the business is profitable. It means decisions are more likely to be based on reliable information.',
        'worksheet': None,
    },
    {
        'num': 25,
        'title': 'Definitions, sources and next step',
        'subtitle': 'A guide to start a better conversation',
        'paragraphs': [
            'ADR: paid room revenue divided by paid room nights on the agreed metric definition. '
            'RevPAR: paid room revenue divided by available saleable room nights. Contribution: '
            'revenue less specified direct costs — always state which costs are included. '
            'GOP (Gross Operating Profit): revenue less all departmental and undistributed '
            'operating expenses. EBITDA: earnings before interest, tax, depreciation and '
            'amortisation. Cash: the actual movement in the bank balance after all payments. '
            'These are not the same number. In a capital-intensive, GST-regulated, OTA-heavy '
            'business, the gap between RevPAR and available cash can be large and non-obvious.',
            'GST rate reference (verify current rates with your accountant): Room tariff '
            'INR 7,501 and above — 18% GST with ITC available on business stays. Room '
            'tariff INR 2,501 to INR 7,500 — 12% GST. Room tariff up to INR 2,500 — 5% '
            'GST (verify current slabs as these are subject to periodic revision by the GST '
            'Council). Restaurant in a hotel with room tariff above INR 7,500 ("specified '
            'premises") — 18% GST with ITC. Alcohol — governed by state excise, outside '
            'the GST framework, varying by state.',
            'Source register: [H] Horwath HTL, India Hotel Market Review 2025, 4 February '
            '2026 — horwathhtl.com/publication/india-hotel-market-review-2025/. '
            '[V] HVS ANAROCK, India Hospitality Industry Overview 2025, 8 May 2026 — '
            'hvs.com/article/10451-hvs-anarock-india-hospitality-industry-overview-2025. '
            '[M] Ministry of Tourism beta dashboard, accessed 1 October 2026 — '
            'data.tourism.gov.in/dashboard (beta; figures may be revised). '
            '[P] Professionalising Indian Family Firms, SAGE, 28 February 2020.',
            'If working through this playbook has identified a gap that cannot be resolved '
            'internally — missing data, disputed definitions, or a decision requiring '
            'independent analysis — a confidential, clearly scoped owner-side review may '
            'be appropriate. Do not send financial records with an initial enquiry to any '
            'adviser. Establish the scope, access requirements and data protection arrangements '
            'before any sensitive information changes hands. This is an editorial draft '
            'requiring founder sign-off. All illustrative figures are fictional. This guide '
            'is not an audit opinion, accounting standard, legal advice or financial advice.',
        ],
        'pull': None,
        'worksheet': None,
    },
]



# ── Back cover ────────────────────────────────────────────────────────────────
def build_back(story, styles, cw):
    story.append(PageBreak())
    story.append(GoldBar(cw, height=4))
    story.append(Spacer(1, 40))
    story.append(Paragraph('ABOUT VERITAS', styles['article_tag']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        'Veritas Hospitality Advisors',
        styles['article_title']
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Veritas works with independent hotel owners and operators across India, providing advisory '
        'services focused on commercial strategy, governance and operational clarity. Our engagements '
        'begin with an AI Visibility Audit and extend into sustained advisory relationships.',
        styles['body']
    ))
    story.append(Spacer(1, 20))
    story.append(ThinRule(cw, color=SLATE, thickness=0.6))
    story.append(Spacer(1, 16))

    contact_data = [
        [Paragraph('FOUNDER', styles['sources_label']), Paragraph('EMAIL', styles['sources_label'])],
        [Paragraph('Vaishakh Surendran', styles['toc_heading']), Paragraph('vaishakh@veritashospitalityadvisors.in', styles['toc_heading'])],
        ['', ''],
        [Paragraph('WEBSITE', styles['sources_label']), Paragraph('PUBLISHED', styles['sources_label'])],
        [Paragraph('veritashospitalityadvisors.in', styles['toc_heading']), Paragraph('October 2026', styles['toc_heading'])],
    ]
    contact_table = Table(contact_data, colWidths=[cw / 2, cw / 2])
    contact_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 40))
    story.append(ThinRule(cw))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        'This document is provided for informational and strategic planning purposes only. '
        'It does not constitute financial, legal or investment advice. All cited research '
        'figures are sourced from third-party publications; verify currency before acting on them. '
        'Copyright 2026 Veritas Hospitality Advisors. All rights reserved.',
        styles['sources']
    ))


# ── Main build ────────────────────────────────────────────────────────────────
def build_pdf():
    styles = make_styles()

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN_OUTER,
        rightMargin=MARGIN_INNER,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOT,
        title='The Independent Hotel Owner\'s Oversight Playbook',
        author='Veritas Hospitality Advisors',
        subject='Hotel Owner Frameworks — India 2026',
        creator='Veritas Hospitality Advisors',
    )

    cw = W - MARGIN_OUTER - MARGIN_INNER  # content width
    story = []

    # Cover (page 1)
    build_cover(story, styles, cw)

    # Table of contents (page 2)
    build_toc(story, styles, cw)

    # All 24 playbook sections (02–25)
    for sec in SECTIONS:
        build_section(
            story, styles, cw,
            sec_num=sec['num'],
            title=sec['title'],
            subtitle=sec['subtitle'],
            paragraphs=sec['paragraphs'],
            worksheet=sec.get('worksheet'),
            pull=sec.get('pull'),
        )

    # Back matter
    build_back(story, styles, cw)

    # Build with page callback
    def on_page(canvas, doc):
        make_header_footer(canvas, doc, styles)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'PDF built: {OUTPUT}')
    import os
    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f'File size: {size_kb} KB')


if __name__ == '__main__':
    build_pdf()
