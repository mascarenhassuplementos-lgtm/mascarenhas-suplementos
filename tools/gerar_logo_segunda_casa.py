#!/usr/bin/env python3
"""
Logo "A segunda casa" da Mascarenhas Suplementos  ->  pasta logo/segunda-casa/

Inspiração: Ageu 2:9 — a glória da segunda casa será maior do que a da primeira.
  • Primeira casa: menor, atrás, em tom apagado — a sombra da loja antiga.
  • Segunda casa: maior, na frente, verde sombreado (degradê) com o M e a seta da marca,
    e raios dourados no telhado — a glória maior do recomeço.
Sombras suaves embaixo das casas dão profundidade.

Uso (na pasta da loja):  python3 tools/gerar_logo_segunda_casa.py   (precisa de Pillow)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "logo", "segunda-casa")
os.makedirs(OUT, exist_ok=True)

ESCURO, OURO, BRANCO, VERDE, VERDE_CLARO = "#14201b", "#f2b705", "#ffffff", "#14894a", "#3ddc84"
F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_IT = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
SS = 3

CASA = [(0, -84), (82, -12), (64, -12), (64, 78), (-64, 78), (-64, -12), (-82, -12)]
PORTA = [(-13, 78), (-13, 46), (13, 46), (13, 78)]
PERNA_E = [(-40, -6), (-22, -6), (-22, 62), (-40, 62)]
PERNA_D = [(22, -6), (40, -6), (40, 62), (22, 62)]
V = [(-40, -6), (-22, -6), (0, 24), (22, -6), (40, -6), (0, 46)]
HASTE = [(-4.5, 20), (4.5, 20), (4.5, -22), (-4.5, -22)]
PONTA = [(-15, -20), (0, -42), (15, -20)]

PRIMEIRA = (-62, 22, 0.62)   # dx, dy, escala (menor, à esquerda e atrás)
SEGUNDA = (22, 0, 1.0)       # maior, na frente


def tr(poly, cx, cy, s, dx, dy, k):
    return [(cx + (dx + x * k) * s, cy + (dy + y * k) * s) for x, y in poly]


def degrade(size, topo, base):
    w, h = size
    g = Image.new("RGBA", (1, h))
    t = tuple(int(topo[i:i + 2], 16) for i in (1, 3, 5)); b = tuple(int(base[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        f = y / max(1, h - 1)
        g.putpixel((0, y), tuple(int(t[i] + (b[i] - t[i]) * f) for i in range(3)) + (255,))
    return g.resize((w, h))


def simbolo(img, cx, cy, s, fundo_claro=True):
    W, H = img.size
    # 1) sombras suaves no chão
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sombra)
    for dx, dy, k in (PRIMEIRA, SEGUNDA):
        ds.polygon(tr(CASA, cx + 7 * s, cy + 9 * s, s, dx, dy, k), fill=(0, 0, 0, 70 if fundo_claro else 140))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(9 * s)))
    d = ImageDraw.Draw(img)
    # 2) primeira casa — a sombra da loja antiga
    dx, dy, k = PRIMEIRA
    cor1_topo, cor1_base = ("#b9d6c4", "#8fb9a0") if fundo_claro else ("#3c5a4a", "#2c4438")
    m1 = Image.new("L", (W, H), 0); ImageDraw.Draw(m1).polygon(tr(CASA, cx, cy, s, dx, dy, k), fill=255)
    img.paste(degrade((W, H), cor1_topo, cor1_base), (0, 0), m1)
    d.polygon(tr(PORTA, cx, cy, s, dx, dy, k), fill="#ffffff" if fundo_claro else "#1d2a24")
    # 3) contorno que separa as casas
    contorno = BRANCO if fundo_claro else ESCURO
    seg = tr(CASA, cx, cy, s, *SEGUNDA)
    d.line(seg + [seg[0]], fill=contorno, width=int(14 * s), joint="curve")
    for x, y in seg:
        d.ellipse([x - 7 * s, y - 7 * s, x + 7 * s, y + 7 * s], fill=contorno)
    # 4) segunda casa — maior, verde sombreado
    m2 = Image.new("L", (W, H), 0); ImageDraw.Draw(m2).polygon(seg, fill=255)
    img.paste(degrade((W, H), "#22b765", "#0c4f2b"), (0, 0), m2)
    dx, dy, _ = SEGUNDA
    for p in (PERNA_E, PERNA_D, V):
        d.polygon(tr(p, cx, cy, s, dx, dy, 1), fill=BRANCO)
    d.polygon(tr(HASTE, cx, cy, s, dx, dy, 1), fill=OURO)
    d.polygon(tr(PONTA, cx, cy, s, dx, dy, 1), fill=OURO)
    # 5) glória: raios dourados acima do telhado da segunda casa
    px, py = cx + dx * s, cy + (dy - 84) * s
    for ang, comp in ((-90, 26), (-125, 20), (-55, 20), (-155, 14), (-25, 14)):
        import math
        a = math.radians(ang)
        x1, y1 = px + math.cos(a) * 16 * s, py + math.sin(a) * 16 * s
        x2, y2 = px + math.cos(a) * (16 + comp) * s, py + math.sin(a) * (16 + comp) * s
        d.line([(x1, y1), (x2, y2)], fill=OURO, width=int(5.5 * s))
        d.ellipse([x2 - 2.7 * s, y2 - 2.7 * s, x2 + 2.7 * s, y2 + 2.7 * s], fill=OURO)


def larg(t, f, tr_):
    return sum(f.getlength(c) for c in t) + tr_ * (len(t) - 1)


def escreve(d, x, y, t, f, tr_, cor):
    for c in t:
        d.text((x, y), c, font=f, fill=cor); x += f.getlength(c) + tr_


def texto(img, x, y, tam, c1, c2, centro=False, versiculo=False):
    d = ImageDraw.Draw(img)
    fb = ImageFont.truetype(F_BOLD, tam); fr = ImageFont.truetype(F_REG, int(tam * 0.42))
    tb = tam * 0.06; w1 = larg("MASCARENHAS", fb, tb); tr_ = (w1 - larg("SUPLEMENTOS", fr, 0)) / 10
    if centro:
        x -= w1 / 2
    escreve(d, x, y, "MASCARENHAS", fb, tb, c1)
    escreve(d, x, y + tam * 1.02, "SUPLEMENTOS", fr, tr_, c2)
    if versiculo:
        fi = ImageFont.truetype(F_IT, int(tam * 0.27))
        linha = "“A glória da segunda casa será maior que a da primeira” · Ageu 2:9"
        while fi.getlength(linha) > w1 * 1.02 and fi.size > 8:
            fi = ImageFont.truetype(F_IT, fi.size - 1)
        d.text((x + (w1 - fi.getlength(linha)) / 2, y + tam * 1.72), linha, font=fi, fill=c2)


def gera(nome, w, h, cx, cy, s, fundo=None, txt=None, claro=True):
    img = Image.new("RGBA", (w * SS, h * SS), fundo or (0, 0, 0, 0))
    simbolo(img, cx * SS, cy * SS, s * SS, fundo_claro=claro)
    if txt:
        x, y, tam, c1, c2, centro, vers = txt
        texto(img, x * SS, y * SS, tam * SS, c1, c2, centro, vers)
    img.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, nome + ".png"))


gera("logo-horizontal", 1560, 470, 250, 252, 1.9, txt=(545, 140, 104, ESCURO, VERDE, False, False))
gera("logo-horizontal-versiculo", 1560, 500, 250, 262, 1.9, txt=(545, 140, 104, ESCURO, VERDE, False, True))
gera("logo-horizontal-fundo-escuro", 1560, 470, 250, 252, 1.9, fundo=ESCURO, claro=False,
     txt=(545, 140, 104, BRANCO, VERDE_CLARO, False, False))
gera("logo-vertical", 1200, 1080, 610, 380, 2.7, txt=(600, 720, 112, ESCURO, VERDE, True, True))
gera("icone-perfil", 1080, 1080, 548, 600, 3.5, fundo=BRANCO)
gera("simbolo", 340, 320, 170, 180, 1.3)
print("ok ->", OUT)
