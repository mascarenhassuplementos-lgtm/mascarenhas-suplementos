#!/usr/bin/env python3
"""
Adiciona ao site/produtos.json os produtos listados em tools/dados/novos.txt
(formato: Categoria|Nome|tamanho|ASIN|preço Amazon|dias de entrega Amazon|id da imagem)
e regenera a lista reserva dentro de site/index.html.
Preço de venda = preço Amazon + 10%; prazo ao cliente = prazo Amazon + 24 h.
Uso (na pasta da loja):  python3 tools/adicionar_amazon.py
"""
import json, os, re, unicodedata
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(RAIZ)
cfg = json.load(open("tools/config.json"))
MARGEM = cfg.get("margem_sobre_ml", 0.10)
CAT = {"Vitaminas": "Vitaminas e Saúde"}
# categoria nova -> entra logo depois desta categoria existente
ANCORA = {"Hipercalórico": "Whey Protein", "Albumina": "Hipercalórico", "Aminoácidos": "BCAA",
          "Hidratação": "Pré-treino", "Colágeno": "Vitaminas e Saúde", "Alimentos Fit": "Barra de Proteína"}
PREF = {"Whey Protein": "whey", "Creatina": "creat", "Pré-treino": "pre", "Glutamina": "glut", "BCAA": "bcaa",
        "Termogênico": "termo", "Vitaminas e Saúde": "vit", "Barra de Proteína": "barra", "Acessórios": "acess",
        "Hipercalórico": "hiper", "Albumina": "albu", "Aminoácidos": "amino", "Hidratação": "hidra",
        "Colágeno": "colag", "Alimentos Fit": "fit"}

d = json.load(open("site/produtos.json", encoding="utf-8"))
ps = d["produtos"]
asins = {p.get("amazon_asin") for p in ps if p.get("amazon_asin")}
ids = {p["id"] for p in ps}
novos = {}
for l in open("tools/dados/novos.txt", encoding="utf-8"):
    f = l.rstrip("\n").split("|")
    if len(f) != 7 or f[3] in asins: continue
    cat, nome, tam, asin, preco, dias, img = f
    cat = CAT.get(cat, cat); asins.add(asin)
    pid = f"{PREF.get(cat, 'prod')}-{asin.lower()}"
    if pid in ids: continue
    ids.add(pid); preco = float(preco); h = int(dias) * 24
    novos.setdefault(cat, []).append({
        "id": pid, "cat": cat, "nome": nome, "tam": tam,
        "img": "https://m.media-amazon.com/images/I/" + img,
        "fonte": "amazon", "amazon_asin": asin, "ml_id": None, "amazon_preco": preco, "preco_ml": None,
        "prazo_ml_horas": h, "preco": round(preco * (1 + MARGEM), 2),
        "prazo_cliente_horas": h + cfg.get("tempo_proprio_horas", 24), "disponivel": True})

# monta a nova ordem: cada categoria com seus novos itens no fim, categorias novas depois da âncora
ordem = []
for p in ps:
    if p["cat"] not in ordem: ordem.append(p["cat"])
pend = [c for c in novos if c not in ordem]
while pend:
    for c in list(pend):
        a = ANCORA.get(c)
        if a is None or a in ordem:
            ordem.insert(ordem.index(a) + 1 if a else len(ordem), c); pend.remove(c)
saida = []
for c in ordem:
    saida += [p for p in ps if p["cat"] == c] + novos.get(c, [])
d["produtos"] = saida
json.dump(d, open("site/produtos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# lista reserva no index.html
def js(p):
    s = f'  {{id:{json.dumps(p["id"])}, cat:{json.dumps(p["cat"], ensure_ascii=False)}, img:{json.dumps(p["img"])}, ' \
        f'nome:{json.dumps(p["nome"], ensure_ascii=False)}, tam:{json.dumps(p["tam"], ensure_ascii=False)}, preco:{p["preco"]:.2f}'
    if p.get("fonte") == "amazon": s += f', fonte:"amazon", prazo_cliente_horas:{p["prazo_cliente_horas"]}'
    if p.get("disponivel") is False: s += ", disponivel:false"
    return s + "}"
html = open("site/index.html", encoding="utf-8").read()
html = re.sub(r"let PRODUTOS = \[\n.*?\n\];", lambda m: "let PRODUTOS = [\n" + ",\n".join(js(p) for p in saida) + "\n];",
              html, count=1, flags=re.S)
open("site/index.html", "w", encoding="utf-8").write(html)
n = sum(len(v) for v in novos.values())
print(f"{n} novos; total {len(saida)}; à venda {sum(1 for p in saida if p.get('disponivel', True))}")
print("ordem:", " > ".join(ordem))
