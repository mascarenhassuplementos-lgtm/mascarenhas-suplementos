#!/usr/bin/env python3
"""
Gera uma tabela de preços compacta (catalogo/tabela-de-precos.pdf) a partir de site/produtos.json.
Uso (na pasta da loja):  python3 tools/gerar_tabela_precos.py
"""
import json, os
from datetime import date
from collections import OrderedDict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
d = json.load(open("site/produtos.json", encoding="utf-8"))
def tam(p):
    t = p["tam"]
    if p.get("prazo_cliente_horas", 0) > 48:
        t += f" · sob encomenda ({-(-p['prazo_cliente_horas'] // 24)} dias)"
    return t
brl = lambda v: "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
cats = OrderedDict()
for p in d["produtos"]:
    if p.get("disponivel", True):
        cats.setdefault(p["cat"], []).append(p)

VERDE = colors.HexColor("#14894a"); ESC = colors.HexColor("#14201b")
CINZA = colors.HexColor("#5b6b64"); CLARO = colors.HexColor("#eef2f0")
st = lambda **k: ParagraphStyle("x", fontName=k.pop("f", "Helvetica"), **k)
T = st(f="Helvetica-Bold", fontSize=18, textColor=ESC, leading=21)
S = st(fontSize=8.5, textColor=CINZA, leading=11)
P = st(fontSize=8, textColor=ESC, leading=9.6)
PR = st(f="Helvetica-Bold", fontSize=8.5, textColor=VERDE, leading=9.6, alignment=2)
CH = st(f="Helvetica-Bold", fontSize=9.5, textColor=colors.white, leading=11)

W = A4[0] - 20*mm
doc = SimpleDocTemplate("catalogo/tabela-de-precos.pdf", pagesize=A4, leftMargin=10*mm, rightMargin=10*mm,
                        topMargin=10*mm, bottomMargin=10*mm, title="Tabela de preços – Mascarenhas Suplementos",
                        author="Mascarenhas Suplementos")
hoje = date.today().strftime("%d/%m/%Y")
topo = Table([[Image("logo/segunda-casa/logo-horizontal.png", width=66*mm, height=66*mm*470/1560), Paragraph("TABELA DE PREÇOS", st(f="Helvetica-Bold", fontSize=18, textColor=VERDE, leading=21, alignment=2))]],
             colWidths=[70*mm, W - 70*mm])
topo.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
story = [topo,
         Paragraph(f"Atualizada em {hoje} · Pedidos: WhatsApp (71) 99704-4675 · E-mail: mascarenhassuplementos@gmail.com · Instagram: @mascarenhassuplementos · Delivery em Salvador R$ 15,00 (até 48h) · "
                   "Retirada GRÁTIS: Loteamento Aquarius, Rua Magno Valente, 484 – Edf. Georges Pompidou · "
                   "Pix ou cartão (chave Pix enviada pelo WhatsApp)", S), Spacer(1, 5)]

# monta as linhas (cabeçalho de categoria + produtos) e divide em 2 colunas
linhas = []
for c, ps in cats.items():
    linhas.append(("cat", c))
    for p in sorted(ps, key=lambda x: x["preco"]):
        linhas.append(("p", p))
# divide em colunas pela altura estimada; cada página tem 2 colunas.
# Quando uma categoria continua na coluna seguinte, repete o cabeçalho com "(cont.)".
def altura(l):
    if l[0] == "cat":
        return 15
    txt = len(l[1]["nome"]) + len(tam(l[1])) + 3
    return 3.2 + 9.6 * (1 + txt // 58)

import sys
AJUSTE = int(sys.argv[1]) if len(sys.argv) > 1 else 0   # reduz os limites se a coluna transbordar
LIMITE_1, LIMITE = 720 - AJUSTE, 772 - AJUSTE   # pontos disponíveis por coluna (1ª página tem o cabeçalho)
colunas, atual, usado, cat_atual = [], [], 0, None
for l in linhas:
    limite = LIMITE_1 if len(colunas) < 2 else LIMITE
    h = altura(l)
    if l[0] == "cat":
        cat_atual = l[1]
        h += altura(("p", {"nome": "x" * 30, "tam": ""}))   # não deixa cabeçalho sozinho no fim
    if usado + h > limite and atual:
        colunas.append(atual)
        atual, usado = [], 0
        if l[0] == "p":
            atual.append(("cat", cat_atual + " (cont.)"))
            usado += 15
    atual.append(l)
    usado += altura(l)
if atual:
    colunas.append(atual)
if len(colunas) % 2:
    colunas.append([])

def tabela(col):
    rows, estilos = [], []
    for i, (tipo, v) in enumerate(col):
        if tipo == "cat":
            extra = " (contém cafeína)" if v.split(" (")[0] in ("Pré-treino", "Termogênico") else ""
            rows.append([Paragraph(v.upper() + extra, CH), ""])
            estilos += [("SPAN", (0, i), (1, i)), ("BACKGROUND", (0, i), (1, i), VERDE)]
        else:
            rows.append([Paragraph(f"<b>{v['nome']}</b> <font color='#5b6b64'>– {tam(v)}</font>", P),
                         Paragraph(brl(v["preco"]), PR)])
            if i % 2:
                estilos.append(("BACKGROUND", (0, i), (1, i), CLARO))
    cw = (W - 4*mm) / 2
    t = Table(rows, colWidths=[cw - 19*mm, 19*mm])
    t.setStyle(TableStyle(estilos + [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                     ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                     ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
                                     ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#dbe3df"))]))
    return t

for k in range(0, len(colunas), 2):
    if k:
        story.append(PageBreak())
    esq, dir_ = colunas[k], colunas[k + 1]
    grade = Table([[tabela(esq) if esq else "", tabela(dir_) if dir_ else ""]], colWidths=[(W - 4*mm) / 2 + 2*mm] * 2)
    grade.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 2*mm)]))
    story.append(grade)
story += [Spacer(1, 4),
          Paragraph("Preços sujeitos a alteração e à disponibilidade de estoque. Pré-treinos e termogênicos contêm cafeína: "
                    "não indicados para gestantes, menores de 18 anos, cardíacos e hipertensos.", S)]
from reportlab.platypus.doctemplate import LayoutError
try:
    doc.build(story)
except LayoutError:  # alguma coluna ficou alta demais: tenta de novo com colunas mais curtas
    if AJUSTE >= 100:
        raise
    os.execv(sys.executable, [sys.executable, os.path.abspath(__file__), str(AJUSTE + 10)])
print(sum(len(v) for v in cats.values()), "produtos")
