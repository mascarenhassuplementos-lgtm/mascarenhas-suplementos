#!/usr/bin/env python3
"""
Gera a logo da Mascarenhas Suplementos em PNG (alta resolução) e SVG, na pasta logo/.

Símbolo: hexágono verde (força, molécula) com um "M" branco; no centro do M,
uma seta dourada sobe e ultrapassa as pernas da letra (evolução, resultado).

Uso (na pasta da loja):  python3 tools/gerar_logo.py   (precisa de Pillow)
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "logo")
os.makedirs(OUT, exist_ok=True)

VERDE, ESCURO, OURO, BRANCO, VERDE_CLARO = "#14894a", "#14201b", "#f2b705", "#ffffff", "#3ddc84"
F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SS = 4  # supersampling para bordas suaves


# ---------- geometria do símbolo (unidade: raio do hexágono = 100) ----------
def hexagono():
    return [(100 * math.cos(math.radians(a)), 100 * math.sin(math.radians(a))) for a in range(-90, 270, 60)]

PERNA_E = [(-48, -36), (-27, -36), (-27, 46), (-48, 46)]
PERNA_D = [(27, -36), (48, -36), (48, 46), (27, 46)]
V = [(-48, -36), (-27, -36), (0, 0), (27, -36), (48, -36), (0, 26)]
HASTE = [(-5, -4), (5, -4), (5, -46), (-5, -46)]
PONTA = [(-17, -44), (0, -68), (17, -44)]


def pts(poly, cx, cy, s):
    return [(cx + x * s, cy + y * s) for x, y in poly]


def desenha_simbolo(d, cx, cy, s, fundo=VERDE, letra=BRANCO, acento=OURO):
    d.polygon(pts(hexagono(), cx, cy, s), fill=fundo)
    for p in (PERNA_E, PERNA_D, V):
        d.polygon(pts(p, cx, cy, s), fill=letra)
    d.polygon(pts(HASTE, cx, cy, s), fill=acento)
    d.polygon(pts(PONTA, cx, cy, s), fill=acento)


def svg_simbolo(cx, cy, s, fundo=VERDE, letra=BRANCO, acento=OURO):
    def path(p, cor):
        return '<path fill="%s" d="M %s Z"/>' % (cor, " L ".join("%.1f,%.1f" % q for q in pts(p, cx, cy, s)))
    return "\n".join([path(hexagono(), fundo), path(PERNA_E, letra), path(PERNA_D, letra), path(V, letra),
                      path(HASTE, acento), path(PONTA, acento)])


# ---------- texto com espaçamento entre letras ----------
def largura(txt, fonte, track):
    return sum(fonte.getlength(c) for c in txt) + track * (len(txt) - 1)


def escreve(d, x, y, txt, fonte, track, cor):
    for c in txt:
        d.text((x, y), c, font=fonte, fill=cor)
        x += fonte.getlength(c) + track


def bloco_texto(d, x, y, tam, cor1, cor2, centro=False):
    """MASCARENHAS (negrito) e, embaixo, SUPLEMENTOS espaçado na mesma largura."""
    fb = ImageFont.truetype(F_BOLD, tam)
    fr = ImageFont.truetype(F_REG, int(tam * 0.42))
    tb = tam * 0.06
    w1 = largura("MASCARENHAS", fb, tb)
    base2 = largura("SUPLEMENTOS", fr, 0)
    tr = (w1 - base2) / 10
    if centro:
        x = x - w1 / 2
    escreve(d, x, y, "MASCARENHAS", fb, tb, cor1)
    escreve(d, x, y + tam * 1.02, "SUPLEMENTOS", fr, tr, cor2)
    return w1, tb, tr


def salva(nome, w, h, desenho, fundo=None):
    img = Image.new("RGBA", (w * SS, h * SS), fundo or (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    info = desenho(d, SS)
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUT, nome + ".png"))
    return info


def svg(nome, w, h, corpo, fundo=None):
    bg = '<rect width="100%%" height="100%%" fill="%s"/>' % fundo if fundo else ""
    open(os.path.join(OUT, nome + ".svg"), "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n'
        '<title>Mascarenhas Suplementos</title>\n%s\n%s\n</svg>\n' % (w, h, w, h, bg, corpo))


def svg_texto(x, y, tam, w1, tb, tr, cor1, cor2, anchor="start"):
    fam = "Liberation Sans, Arial, Helvetica, sans-serif"
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-weight="700" font-size="%d" letter-spacing="%.1f" fill="%s" text-anchor="%s">MASCARENHAS</text>\n'
            '<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" letter-spacing="%.1f" fill="%s" text-anchor="%s">SUPLEMENTOS</text>'
            % (x, y + tam * 0.82, fam, tam, tb, cor1, anchor, x, y + tam * 1.02 + tam * 0.42 * 0.82, fam, int(tam * 0.42), tr, cor2, anchor))


# 1) Horizontal (fundo claro e fundo escuro)
for nome, c1, c2, fundo, fsvg in [("logo-horizontal", ESCURO, VERDE, None, None),
                                  ("logo-horizontal-fundo-escuro", BRANCO, VERDE_CLARO, ESCURO, ESCURO)]:
    W, H = 1420, 440
    def des(d, k, c1=c1, c2=c2):
        desenha_simbolo(d, 220 * k, 220 * k, 1.85 * k)
        return bloco_texto(d, 450 * k, 128 * k, 104 * k, c1, c2)
    w1, tb, tr = salva(nome, W, H, des, fundo)
    svg(nome, W, H, svg_simbolo(220, 220, 1.85) + "\n" + svg_texto(450, 128, 104, w1 / SS, tb / SS, tr / SS, c1, c2), fsvg)

# 2) Vertical
W, H = 1200, 960
def des_v(d, k):
    desenha_simbolo(d, 600 * k, 340 * k, 2.6 * k)
    return bloco_texto(d, 600 * k, 700 * k, 112 * k, ESCURO, VERDE, centro=True)
w1, tb, tr = salva("logo-vertical", W, H, des_v)
svg("logo-vertical", W, H, svg_simbolo(600, 340, 2.6) + "\n" + svg_texto(600, 700, 112, w1 / SS, tb / SS, tr / SS, ESCURO, VERDE, "middle"))

# 3) Ícone de perfil (Instagram / WhatsApp) — cabe dentro do recorte redondo
for nome, fundo, hexa in [("icone-perfil", BRANCO, VERDE), ("icone-perfil-verde", VERDE, ESCURO)]:
    W = H = 1080
    salva(nome, W, H, lambda d, k, hexa=hexa: desenha_simbolo(d, 540 * k, 556 * k, 4.0 * k, fundo=hexa), fundo)
    svg(nome, W, H, svg_simbolo(540, 556, 4.0, fundo=hexa), fundo)

# 4) Só o símbolo, sem fundo (site, favicon, cabeçalhos)
W = H = 240
salva("simbolo", W, H, lambda d, k: desenha_simbolo(d, 120 * k, 124 * k, 1.12 * k))
svg("simbolo", W, H, svg_simbolo(120, 124, 1.12))
# versão clara do símbolo, para usar sobre fundo verde
salva("simbolo-claro", W, H, lambda d, k: desenha_simbolo(d, 120 * k, 124 * k, 1.12 * k, fundo=BRANCO, letra=VERDE))
svg("simbolo-claro", W, H, svg_simbolo(120, 124, 1.12, fundo=BRANCO, letra=VERDE))

print("logos gerados em", OUT)
