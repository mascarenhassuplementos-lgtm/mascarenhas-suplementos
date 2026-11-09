#!/usr/bin/env python3
"""
Logo "duas casas" da Mascarenhas Suplementos  ->  pasta logo/duas-casas/

Símbolo: duas casas sobrepostas.
  • Casa de trás, escura (a "sombra"): a loja online, com o sinal de Wi-Fi dourado.
  • Casa da frente, verde: a loja física, com o M branco e a seta dourada da marca.
As duas ficam nítidas porque há um contorno branco separando uma da outra.

Uso (na pasta da loja):  python3 tools/gerar_logo_duas_casas.py   (precisa de Pillow)
"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "logo", "duas-casas")
os.makedirs(OUT, exist_ok=True)

VERDE, ESCURO, OURO, BRANCO, VERDE_CLARO = "#14894a", "#14201b", "#f2b705", "#ffffff", "#3ddc84"
F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SS = 4

# casa (unidade ~100): telhado com beiral e paredes
CASA = [(0, -84), (82, -12), (64, -12), (64, 78), (-64, 78), (-64, -12), (-82, -12)]
# letra M e seta (mesmo desenho da marca), relativas ao centro da casa da frente
PERNA_E = [(-40, -6), (-22, -6), (-22, 62), (-40, 62)]
PERNA_D = [(22, -6), (40, -6), (40, 62), (22, 62)]
V = [(-40, -6), (-22, -6), (0, 24), (22, -6), (40, -6), (0, 46)]
HASTE = [(-4.5, 20), (4.5, 20), (4.5, -22), (-4.5, -22)]
PONTA = [(-15, -20), (0, -42), (15, -20)]

TRAS = (46, -30, 0.86)    # deslocamento x, y e escala da casa de trás (loja online)
FRENTE = (-22, 14, 1.0)   # casa da frente (loja física)
CONTORNO = 9              # espessura do contorno branco entre as casas


def tr(poly, cx, cy, s, dx, dy, k):
    return [(cx + (dx + x * k) * s, cy + (dy + y * k) * s) for x, y in poly]


def engorda(poly, d):
    """Aumenta o polígono a partir do centro (para o contorno branco)."""
    mx = sum(x for x, _ in poly) / len(poly); my = sum(y for _, y in poly) / len(poly)
    out = []
    for x, y in poly:
        vx, vy = x - mx, y - my
        n = (vx * vx + vy * vy) ** 0.5 or 1
        out.append((x + vx / n * d, y + vy / n * d))
    return out


def simbolo(d, cx, cy, s, fundo_contorno=BRANCO, casa_tras=ESCURO, casa_frente=VERDE, letra=BRANCO, acento=OURO):
    dx, dy, k = TRAS
    d.polygon(tr(CASA, cx, cy, s, dx, dy, k), fill=casa_tras)
    # Wi-Fi dourado na parte visível da casa de trás (loja online)
    wx, wy = cx + (dx + 30) * s, cy + (dy + 22) * s
    for r in (9, 18, 27):
        rr = r * s
        d.arc([wx - rr, wy - rr, wx + rr, wy + rr], 225, 315, fill=acento, width=max(1, int(5 * s)))
    d.ellipse([wx - 4 * s, wy - 4 * s, wx + 4 * s, wy + 4 * s], fill=acento)
    # casa da frente com contorno (separa nitidamente as duas casas)
    fdx, fdy, fk = FRENTE
    frente = tr(CASA, cx, cy, s, fdx, fdy, fk)
    if fundo_contorno:  # contorno nítido entre as duas casas
        d.line(frente + [frente[0]], fill=fundo_contorno, width=int(2 * CONTORNO * s), joint="curve")
        for x, y in frente:
            r = CONTORNO * s
            d.ellipse([x - r, y - r, x + r, y + r], fill=fundo_contorno)
    d.polygon(frente, fill=casa_frente)
    for p in (PERNA_E, PERNA_D, V):
        d.polygon(tr(p, cx, cy, s, fdx, fdy, 1), fill=letra)
    d.polygon(tr(HASTE, cx, cy, s, fdx, fdy, 1), fill=acento)
    d.polygon(tr(PONTA, cx, cy, s, fdx, fdy, 1), fill=acento)


def largura(txt, f, t):
    return sum(f.getlength(c) for c in txt) + t * (len(txt) - 1)


def escreve(d, x, y, txt, f, t, cor):
    for c in txt:
        d.text((x, y), c, font=f, fill=cor); x += f.getlength(c) + t


def texto(d, x, y, tam, c1, c2, centro=False):
    fb = ImageFont.truetype(F_BOLD, tam); fr = ImageFont.truetype(F_REG, int(tam * 0.42))
    tb = tam * 0.06; w1 = largura("MASCARENHAS", fb, tb)
    tr_ = (w1 - largura("SUPLEMENTOS", fr, 0)) / 10
    if centro:
        x -= w1 / 2
    escreve(d, x, y, "MASCARENHAS", fb, tb, c1)
    escreve(d, x, y + tam * 1.02, "SUPLEMENTOS", fr, tr_, c2)
    fs = ImageFont.truetype(F_REG, int(tam * 0.30))
    lema = "LOJA FÍSICA  •  LOJA ONLINE"
    lx = x + (w1 - fs.getlength(lema)) / 2
    d.text((lx, y + tam * 1.72), lema, font=fs, fill=c2)


def salva(nome, w, h, desenho, fundo=None):
    img = Image.new("RGBA", (w * SS, h * SS), fundo or (0, 0, 0, 0))
    desenho(ImageDraw.Draw(img), SS)
    img.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, nome + ".png"))


# horizontal (claro e escuro)
salva("logo-horizontal", 1500, 460, lambda d, k: (simbolo(d, 235 * k, 238 * k, 1.85 * k), texto(d, 505 * k, 118 * k, 104 * k, ESCURO, VERDE)))
salva("logo-horizontal-fundo-escuro", 1500, 460,
      lambda d, k: (simbolo(d, 235 * k, 238 * k, 1.85 * k, fundo_contorno=ESCURO, casa_tras="#2b3a33"),
                    texto(d, 505 * k, 118 * k, 104 * k, BRANCO, VERDE_CLARO)), ESCURO)
# vertical
salva("logo-vertical", 1200, 1060, lambda d, k: (simbolo(d, 600 * k, 360 * k, 2.6 * k), texto(d, 600 * k, 700 * k, 112 * k, ESCURO, VERDE, centro=True)))
# ícone de perfil (cabe no recorte redondo)
salva("icone-perfil", 1080, 1080, lambda d, k: simbolo(d, 548 * k, 560 * k, 3.6 * k), BRANCO)
# símbolo sem fundo
salva("simbolo", 300, 300, lambda d, k: simbolo(d, 150 * k, 156 * k, 1.3 * k))
print("ok ->", OUT)
