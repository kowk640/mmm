# -*- coding: utf-8 -*-
"""PDF builder for the biology olympiad handbook."""
import os, re, glob
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, PageBreak,
                                KeepTogether, CondPageBreak, HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents

FONTDIR = None
for cand in glob.glob('/usr/local/lib*/python3*/site-packages/matplotlib/mpl-data/fonts/ttf'):
    FONTDIR = cand
    break
if FONTDIR is None:
    raise RuntimeError('font dir not found')


def _reg(name, fn):
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTDIR, fn)))


_reg('Body', 'DejaVuSerif.ttf'); _reg('Body-Bold', 'DejaVuSerif-Bold.ttf')
_reg('Body-Italic', 'DejaVuSerif-Italic.ttf'); _reg('Body-BoldItalic', 'DejaVuSerif-BoldItalic.ttf')
_reg('Head', 'DejaVuSans.ttf'); _reg('Head-Bold', 'DejaVuSans-Bold.ttf')
_reg('Head-Italic', 'DejaVuSans-Oblique.ttf'); _reg('Head-BoldItalic', 'DejaVuSans-BoldOblique.ttf')
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-Bold', italic='Body-Italic', boldItalic='Body-BoldItalic')
pdfmetrics.registerFontFamily('Head', normal='Head', bold='Head-Bold', italic='Head-Italic', boldItalic='Head-BoldItalic')

INK = colors.HexColor('#111111')
C_DEF = colors.HexColor('#1f4e79')
C_OLYMP = colors.HexColor('#7b3f00')
C_WARN = colors.HexColor('#9b1c1c')
C_EX = colors.HexColor('#1f6b45')
C_NEU = colors.HexColor('#444444')
BG_LIGHT = colors.HexColor('#f2f2f2')
BG_ZEBRA = colors.HexColor('#f7f7f7')
BG_HEAD = colors.HexColor('#e3e3e3')
FOOTER = 'Біологія — олімпіадний посібник для 9 класу'

LM, RM, TM, BM = 20*mm, 16*mm, 18*mm, 18*mm
CW = A4[0] - LM - RM

S = {}
S['body'] = ParagraphStyle('body', fontName='Body', fontSize=9.6, leading=13.4, textColor=INK,
                           alignment=TA_JUSTIFY, spaceAfter=4)
S['h1'] = ParagraphStyle('h1', fontName='Head-Bold', fontSize=19, leading=23, textColor=INK, spaceAfter=3)
S['sub'] = ParagraphStyle('sub', fontName='Head', fontSize=10.5, leading=14, textColor=C_NEU, spaceAfter=10)
S['h2'] = ParagraphStyle('h2', fontName='Head-Bold', fontSize=13, leading=16, textColor=INK, spaceBefore=9, spaceAfter=4)
S['h3'] = ParagraphStyle('h3', fontName='Head-Bold', fontSize=11, leading=14, textColor=C_NEU, spaceBefore=7, spaceAfter=3)
S['h4'] = ParagraphStyle('h4', fontName='Head-Bold', fontSize=9.8, leading=13, textColor=C_NEU, spaceBefore=5, spaceAfter=2)
S['li'] = ParagraphStyle('li', parent=S['body'], leftIndent=9, bulletIndent=1, spaceAfter=2)
S['boxtitle'] = ParagraphStyle('boxtitle', fontName='Head-Bold', fontSize=9.6, leading=12.6, spaceAfter=2)
S['boxbody'] = ParagraphStyle('boxbody', fontName='Body', fontSize=9.3, leading=12.8, textColor=INK, alignment=TA_LEFT, spaceAfter=3)
S['boxli'] = ParagraphStyle('boxli', parent=S['boxbody'], leftIndent=9, bulletIndent=1, spaceAfter=1)
S['cell'] = ParagraphStyle('cell', fontName='Body', fontSize=8.6, leading=11.2, textColor=INK)
S['cellsm'] = ParagraphStyle('cellsm', fontName='Body', fontSize=7.6, leading=9.8, textColor=INK)
S['cellh'] = ParagraphStyle('cellh', fontName='Head-Bold', fontSize=8.6, leading=11.2, textColor=INK)
S['cellhsm'] = ParagraphStyle('cellhsm', fontName='Head-Bold', fontSize=7.6, leading=9.8, textColor=INK)
S['caption'] = ParagraphStyle('caption', fontName='Head', fontSize=8.4, leading=11, textColor=C_NEU, alignment=TA_CENTER, spaceBefore=3, spaceAfter=7)
S['tabtitle'] = ParagraphStyle('tabtitle', fontName='Head-Bold', fontSize=8.8, leading=11.5, textColor=C_NEU, spaceBefore=6, spaceAfter=3)
S['math'] = ParagraphStyle('math', fontName='Body-Italic', fontSize=10.2, leading=14, textColor=INK, alignment=TA_CENTER, spaceBefore=4, spaceAfter=6)
S['toc1'] = ParagraphStyle('toc1', fontName='Head-Bold', fontSize=10, leading=15, spaceBefore=5)
S['toc2'] = ParagraphStyle('toc2', fontName='Body', fontSize=9, leading=12.5, leftIndent=12)
S['toc3'] = ParagraphStyle('toc3', fontName='Body', fontSize=8.4, leading=11.5, leftIndent=24, textColor=C_NEU)

BOX = {
    'def': ('Означення', C_DEF),
    'olymp': ('Олімпіадне поглиблення', C_OLYMP),
    'warn': ('Увага', C_WARN),
    'ex': ('Розібраний приклад', C_EX),
    'rem': ('Запам’ятайте', C_DEF),
    'algo': ('Алгоритм міркування', C_OLYMP),
    'check': ('Самоперевірка', C_NEU),
    'sum': ('Стисле повторення', C_NEU),
    'link': ('Зв’язки між темами', C_NEU),
    'exam': ('Як це перевіряють на олімпіаді', C_OLYMP),
    'note': ('Примітка', C_NEU),
}


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(t):
    t = esc(t)
    t = re.sub(r'\[\[([A-Za-z0-9_]+)\|(.+?)\]\]', r'<link href="#\1" color="#1f4e79">\2</link>', t)
    t = re.sub(r'\{\{(.+?)\}\}', r'<font face="Head">\1</font>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', t)
    t = re.sub(r'\^\{(.+?)\}', r'<super>\1</super>', t)
    t = re.sub(r'_\{(.+?)\}', r'<sub>\1</sub>', t)
    return t


class Head(Paragraph):
    def __init__(self, text, style, level, key=None, label=None):
        Paragraph.__init__(self, text, style)
        self.tocLevel = level
        self.tocKey = key
        self.tocLabel = label if label is not None else re.sub(r'<[^>]+>', '', text)


class Anchor(Spacer):
    def __init__(self, name):
        Spacer.__init__(self, 1, 0.1)
        self.name = name

    def draw(self):
        self.canv.bookmarkPage(self.name)


class Book(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=A4, leftMargin=LM,
                                 rightMargin=RM, topMargin=TM, bottomMargin=BM,
                                 title='Біологія. Олімпіадний посібник для 9 класу',
                                 author='Notion AI', **kw)
        frame = Frame(LM, BM, CW, A4[1]-TM-BM, id='n')
        self.addPageTemplates([
            PageTemplate(id='main', frames=[frame], onPage=self._deco),
            PageTemplate(id='plain', frames=[frame]),
        ])
        self.chapter = ''
        self.seq = 0

    def _deco(self, canv, doc):
        canv.saveState()
        canv.setFont('Head', 7.4)
        canv.setFillColor(C_NEU)
        y = A4[1] - TM + 6
        canv.drawString(LM, y, self.chapter[:80])
        canv.drawRightString(A4[0]-RM, y, FOOTER)
        canv.setStrokeColor(colors.HexColor('#cccccc'))
        canv.setLineWidth(0.4)
        canv.line(LM, y-2.5, A4[0]-RM, y-2.5)
        canv.drawCentredString(A4[0]/2.0, BM-10, str(doc.page))
        canv.restoreState()

    def afterFlowable(self, fl):
        if isinstance(fl, Head):
            lvl = fl.tocLevel
            if lvl == 0:
                self.chapter = fl.tocLabel
            self.notify('TOCEntry', (lvl, fl.tocLabel, self.page, fl.tocKey))
            self.seq += 1
            key = fl.tocKey or ('h%d' % self.seq)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(fl.tocLabel[:90], key, level=min(lvl, 2), closed=(lvl == 0))


def box(kind, title, flows):
    label, col = BOX.get(kind, ('', C_NEU))
    head = title or label
    inner = [Paragraph('<font color="%s">%s</font>' % ('#' + col.hexval()[4:], esc(head)), S['boxtitle'])] + flows
    t = Table([[inner]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT if kind in ('sum', 'check', 'note') else colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#bbbbbb')),
        ('LINEBEFORE', (0, 0), (0, -1), 2.2, col),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return [Spacer(1, 3), t, Spacer(1, 6)]


def make_table(widths, rows, small, title, num):
    st_c = S['cellsm'] if small else S['cell']
    st_h = S['cellhsm'] if small else S['cellh']
    data = []
    for i, r in enumerate(rows):
        style = st_h if i == 0 else st_c
        data.append([Paragraph(inline(c), style) for c in r])
    ncol = max(len(r) for r in data)
    for r in data:
        while len(r) < ncol:
            r.append(Paragraph('', st_c))
    if widths and len(widths) == ncol:
        tot = float(sum(widths))
        cw = [CW*w/tot for w in widths]
    else:
        cw = [CW/float(ncol)]*ncol
    t = Table(data, colWidths=cw, repeatRows=1)
    cmds = [('BACKGROUND', (0, 0), (-1, 0), BG_HEAD),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    for i in range(2, len(data), 2):
        cmds.append(('BACKGROUND', (0, i), (-1, i), BG_ZEBRA))
    t.setStyle(TableStyle(cmds))
    out = []
    if title:
        out.append(Paragraph('<b>Табл. %d.</b> %s' % (num, esc(title)), S['tabtitle']))
    out.append(t)
    out.append(Spacer(1, 7))
    return out


def parse(path, ctx, figdir):
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if s.startswith('# '):
            ctx['ch'] += 1
            title = s[2:].strip()
            if ctx['ch'] > 1 or out:
                out.append(PageBreak())
            lab = 'Розділ %d. %s' % (ctx['ch'], title)
            out.append(Head('<font color="#1f4e79">Розділ %d</font>' % ctx['ch'],
                            ParagraphStyle('chn', fontName='Head-Bold', fontSize=10, leading=13, spaceAfter=1), 0,
                            key='ch%d' % ctx['ch'], label=lab))
            out.append(Paragraph(inline(title), S['h1']))
            out.append(HRFlowable(width='100%', thickness=1.0, color=C_DEF, spaceBefore=3, spaceAfter=7))
            i += 1; continue
        if s.startswith('@ '):
            out.append(Paragraph(inline(s[2:]), S['sub'])); i += 1; continue
        if s.startswith('#### '):
            out.append(Paragraph(inline(s[5:]), S['h4'])); i += 1; continue
        if s.startswith('### '):
            ctx['n3'] += 1
            out.append(Head(inline(s[4:]), S['h3'], 2, key='s3_%d' % ctx['n3'])); i += 1; continue
        if s.startswith('## '):
            ctx['n2'] += 1
            out.append(Head(inline(s[3:]), S['h2'], 1, key='s2_%d' % ctx['n2'])); i += 1; continue
        if s.startswith('::anchor '):
            out.append(Anchor(s.split(None, 1)[1].strip())); i += 1; continue
        if s == '::pagebreak':
            out.append(PageBreak()); i += 1; continue
        if s == '::rule':
            out.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#cccccc'),
                                  spaceBefore=5, spaceAfter=5)); i += 1; continue
        if s.startswith('::keep '):
            out.append(CondPageBreak(float(s.split()[1])*mm)); i += 1; continue
        if s.startswith('::fig '):
            m = re.match(r'::fig\s+(\S+?)\[(\d+)\]\s*(?:\|\s*(.*))?$', s)
            if m:
                name, w, cap = m.group(1), float(m.group(2)), (m.group(3) or '')
                p = os.path.join(figdir, name + '.png')
                if os.path.exists(p):
                    from PIL import Image as PImage
                    iw, ih = PImage.open(p).size
                    wpt = w*mm
                    img = Image(p, width=wpt, height=wpt*ih/float(iw))
                    ctx['figs'] += 1
                    capp = Paragraph('<b>Рис. %d.</b> %s' % (ctx['figs'], inline(cap)), S['caption'])
                    out.append(KeepTogether([Spacer(1, 4), img, capp]))
                else:
                    print('MISSING FIG', p)
            i += 1; continue
        if s.startswith('::table'):
            m = re.match(r'::table(!?)\[([0-9,\s]*)\]\s*(.*)$', s)
            small = bool(m and m.group(1))
            widths = [float(x) for x in m.group(2).split(',') if x.strip()] if m else []
            title = (m.group(3).strip() if m else '')
            i += 1
            rows = []
            while i < n and lines[i].strip() != '::':
                r = lines[i].strip()
                if r and not r.startswith('---'):
                    rows.append([c.strip() for c in r.split('|')])
                i += 1
            i += 1
            if rows:
                ctx['tabs'] += 1
                out.extend(make_table(widths, rows, small, title, ctx['tabs']))
            continue
        if s.startswith(':::'):
            headline = s[3:].strip().split(None, 1)
            kind = headline[0] if headline else 'note'
            title = headline[1] if len(headline) > 1 else ''
            i += 1
            buf = []
            while i < n and lines[i].strip() != ':::':
                buf.append(lines[i]); i += 1
            i += 1
            flows = []
            for b in buf:
                bs = b.strip()
                if not bs or bs.startswith('$$') or bs.startswith('::'):
                    continue
                if bs.startswith('- '):
                    flows.append(Paragraph(inline(bs[2:]), S['boxli'], bulletText='\u2022'))
                elif re.match(r'^\d+[.)]\s', bs):
                    num, rest = re.split(r'[.)]\s', bs, 1)
                    flows.append(Paragraph(inline(rest), S['boxli'], bulletText=num + '.'))
                else:
                    flows.append(Paragraph(inline(bs), S['boxbody']))
            out.extend(box(kind, title, flows))
            continue
        if s.startswith('$$'):
            body = s.strip('$ ').strip()
            if not body:
                i += 1
                buf = []
                while i < n and not lines[i].strip().startswith('$$'):
                    buf.append(lines[i].strip()); i += 1
                i += 1
                body = ' '.join(buf)
            else:
                i += 1
            out.append(Paragraph(inline(body), S['math']))
            continue
        if s.startswith('- '):
            out.append(Paragraph(inline(s[2:]), S['li'], bulletText='\u2022')); i += 1; continue
        m = re.match(r'^(\d+)[.)]\s+(.*)$', s)
        if m:
            out.append(Paragraph(inline(m.group(2)), S['li'], bulletText=m.group(1) + '.')); i += 1; continue
        out.append(Paragraph(inline(s), S['body']))
        i += 1
    return out


def title_pages(meta):
    fl = [Spacer(1, 45*mm)]
    fl.append(Paragraph(meta['title'], ParagraphStyle('t', fontName='Head-Bold', fontSize=26, leading=31,
                                                      alignment=TA_CENTER, textColor=INK)))
    fl.append(Spacer(1, 6*mm))
    fl.append(Paragraph(meta['subtitle'], ParagraphStyle('t2', fontName='Head', fontSize=13, leading=18,
                                                         alignment=TA_CENTER, textColor=C_NEU)))
    fl.append(Spacer(1, 40*mm))
    fl.append(Paragraph(meta['footer'], ParagraphStyle('t3', fontName='Body', fontSize=9.5, leading=14,
                                                       alignment=TA_CENTER, textColor=C_NEU)))
    fl.append(PageBreak())
    fl.append(Paragraph('Про це видання та відповідальне використання', S['h2']))
    for p in meta['notice']:
        fl.append(Paragraph(inline(p), S['body']))
    return fl


def build(src_files, out_pdf, figdir, front_flowables=None, toc_title='Зміст'):
    doc = Book(out_pdf)
    story = []
    if front_flowables:
        story.extend(front_flowables)
        story.append(PageBreak())
    toc = TableOfContents()
    toc.levelStyles = [S['toc1'], S['toc2'], S['toc3']]
    story.append(Paragraph(toc_title, S['h1']))
    story.append(HRFlowable(width='100%', thickness=1.0, color=C_DEF, spaceBefore=3, spaceAfter=8))
    story.append(toc)
    ctx = {'ch': 0, 'figs': 0, 'tabs': 0, 'n2': 0, 'n3': 0}
    for f in src_files:
        story.extend(parse(f, ctx, figdir))
    doc.multiBuild(story)
    return ctx['figs'], ctx['tabs'], ctx['ch']
