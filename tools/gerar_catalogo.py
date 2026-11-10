#!/usr/bin/env python3
"""
Gera os catálogos de venda a partir de site/produtos.json:
  catalogo/catalogo-mascarenhas-suplementos.pdf   (para enviar como arquivo)
  catalogo/catalogo-whatsapp.txt         (texto completo para colar)
  catalogo/whatsapp-<categoria>.txt      (uma mensagem curta por categoria)

Uso (na pasta da loja):  python3 tools/gerar_catalogo.py
Precisa da biblioteca reportlab (pip install reportlab).
"""
import json, os
from collections import OrderedDict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
os.makedirs("catalogo", exist_ok=True)

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
EMO = {"Creatina": "💪", "Whey Protein": "🥛", "Pré-treino": "⚡", "Glutamina": "🔄",
       "Termogênico": "🔥", "Vitaminas e Saúde": "💊", "Acessórios": "🏋️", "Barra de Proteína": "🍫", "BCAA": "🧬",
       "Hipercalórico": "🍚", "Albumina": "🥚", "Aminoácidos": "🧪", "Hidratação": "💧", "Colágeno": "✨", "Alimentos Fit": "🥜"}
CAF = "Contém cafeína. Não indicado para gestantes, menores de 18 anos, cardíacos e hipertensos."
AVISO = {"Pré-treino": CAF, "Termogênico": CAF}
ENTREGA = "🚚 Entrega via delivery em Salvador: *R$ 15,00* (até 48h após o pagamento)"
RETIRADA = "🏢 Retirada *GRÁTIS*: Loteamento Aquarius, Rua Magno Valente, 484 – Edf. Georges Pompidou"
PAG = "💸 Pagamento: Pix (chave enviada no WhatsApp) ou cartão por link"

# ---------- texto completo ----------
t = ["*MASCARENHAS SUPLEMENTOS* 💪", "_Suplementos originais em Salvador_", "", ENTREGA, RETIRADA, PAG, ""]
for c, ps in cats.items():
    t.append(f"{EMO.get(c, '•')} *{c.upper()}*")
    for p in sorted(ps, key=lambda x: x["preco"]):
        t.append(f"• {p['nome']} – {tam(p)}: *{brl(p['preco'])}*")
    if c in AVISO:
        t.append(f"_⚠️ {AVISO[c]}_")
    t.append("")
t += ["📲 *Como pedir:* responda esta mensagem com o produto e a quantidade, ou peça pelo nosso site.",
      "📧 mascarenhassuplementos@gmail.com", "📸 instagram.com/mascarenhassuplementos", "_Preços sujeitos a alteração e à disponibilidade de estoque._"]
open("catalogo/catalogo-whatsapp.txt", "w", encoding="utf-8").write("\n".join(t))

# ---------- uma mensagem por categoria ----------
for c, ps in cats.items():
    m = [f"{EMO.get(c, '•')} *{c.upper()} – MASCARENHAS SUPLEMENTOS*", ""]
    m += [f"• {p['nome']} – {tam(p)}: *{brl(p['preco'])}*" for p in sorted(ps, key=lambda x: x["preco"])]
    if c in AVISO:
        m += ["", f"_⚠️ {AVISO[c]}_"]
    m += ["", "🚚 Delivery Salvador R$ 15 | 🏢 Retirada grátis no Aquarius", "📲 Responda com o produto que você quer!", "📸 @mascarenhassuplementos"]
    import unicodedata
    nome = unicodedata.normalize("NFKD", c.lower()).encode("ascii", "ignore").decode().replace(" ", "-")
    open(f"catalogo/whatsapp-{nome}.txt", "w", encoding="utf-8").write("\n".join(m))

# ---------- PDF ----------
VERDE = colors.HexColor("#14894a"); ESC = colors.HexColor("#14201b")
CINZA = colors.HexColor("#5b6b64"); CLARO = colors.HexColor("#eef2f0")
st = lambda **k: ParagraphStyle("x", fontName=k.pop("f", "Helvetica"), **k)
H = st(f="Helvetica-Bold", fontSize=26, textColor=ESC, leading=30)
SUB = st(fontSize=11, textColor=CINZA, leading=14)
CAT = st(f="Helvetica-Bold", fontSize=15, textColor=colors.white, leading=18)
N = st(fontSize=10, textColor=ESC, leading=13)
NB = st(f="Helvetica-Bold", fontSize=11, textColor=VERDE, leading=13, alignment=2)
AV = st(fontSize=8.5, textColor=colors.HexColor("#8a5a00"), leading=11)
doc = SimpleDocTemplate("catalogo/catalogo-mascarenhas-suplementos.pdf", pagesize=A4,
                        leftMargin=16*mm, rightMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm,
                        title="Catálogo Mascarenhas Suplementos", author="Mascarenhas Suplementos")
W = A4[0] - 32*mm
logo = Image("logo/segunda-casa/logo-horizontal-versiculo.png", width=120*mm, height=120*mm*500/1560)
logo.hAlign = "LEFT"
s = [logo, Paragraph("Suplementos originais em Salvador – BA", SUB), Spacer(1, 8)]
info = Table([[Paragraph("<b>Delivery em Salvador:</b> R$ 15,00 – entrega em até 48h após o pagamento", N)],
              [Paragraph("<b>Retirada GRÁTIS:</b> Loteamento Aquarius, Rua Magno Valente, 484 – Edf. Georges Pompidou", N)],
              [Paragraph("<b>Pagamento:</b> Pix (chave enviada pelo WhatsApp) ou cartão por link", N)],
              [Paragraph("<b>Pedidos:</b> WhatsApp (71) 99704-4675 · E-mail: mascarenhassuplementos@gmail.com · Instagram: @mascarenhassuplementos", N)]], colWidths=[W])
info.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CLARO), ("BOX", (0, 0), (-1, -1), 0.8, VERDE),
                          ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 3),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
s += [info, Spacer(1, 10)]
for c, ps in cats.items():
    head = Table([[Paragraph(c.upper(), CAT)]], colWidths=[W])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), VERDE), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                              ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    rows = [[Paragraph(f"<b>{p['nome']}</b><br/><font color='#5b6b64' size='9'>{tam(p)}</font>", N),
             Paragraph(brl(p["preco"]), NB)] for p in sorted(ps, key=lambda x: x["preco"])]
    tb = Table(rows, colWidths=[W - 32*mm, 32*mm])
    tb.setStyle(TableStyle([("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, CLARO]),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#dbe3df")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    bloco = [head, tb]
    if c in AVISO:
        bloco += [Spacer(1, 3), Paragraph("Atenção: " + AVISO[c], AV)]
    # categorias grandes podem quebrar de página; as pequenas ficam juntas
    s += ([KeepTogether(bloco)] if len(ps) <= 12 else bloco) + [Spacer(1, 10)]
s.append(Paragraph("Preços sujeitos a alteração e à disponibilidade de estoque. Mascarenhas Suplementos · Salvador – BA",
                   st(fontSize=8, textColor=CINZA, alignment=1)))
doc.build(s)
print(sum(len(v) for v in cats.values()), "produtos;", len(cats), "categorias")
