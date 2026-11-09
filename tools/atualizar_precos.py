#!/usr/bin/env python3
"""
Atualiza preços, frete e prazo de entrega dos produtos do site
consultando a API oficial do Mercado Livre.

Lê e reescreve: site/produtos.json
Configuração:   tools/config.json  (margem, CEP, prazos)

Variáveis de ambiente (segredos — nunca coloque no código):
  ML_CLIENT_ID, ML_CLIENT_SECRET, ML_REFRESH_TOKEN
  NOVO_REFRESH_TOKEN_ARQUIVO  (opcional) arquivo onde salvar o novo refresh token
  ML_SIMULAR                  (opcional) JSON com respostas falsas, para teste sem internet

Uso:  python3 tools/atualizar_precos.py
"""
import json, math, os, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ_PRODUTOS = os.path.join(RAIZ, "site", "produtos.json")
ARQ_CONFIG = os.path.join(RAIZ, "tools", "config.json")
API = "https://api.mercadolibre.com"
BRT = timezone(timedelta(hours=-3))

SIMULADO = None
if os.environ.get("ML_SIMULAR"):
    with open(os.environ["ML_SIMULAR"], encoding="utf-8") as f:
        SIMULADO = json.load(f)


def http(metodo, caminho, token=None, form=None):
    """Faz a chamada à API e devolve o JSON (ou None em 404)."""
    if SIMULADO is not None:
        chave = caminho.split("?")[0]
        if chave not in SIMULADO:
            return None
        return SIMULADO[chave]
    url = API + caminho
    dados = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=dados, method=metodo)
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if form:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        corpo = e.read().decode(errors="replace")[:300]
        raise RuntimeError(f"{metodo} {caminho} -> HTTP {e.code}: {corpo}") from None


def obter_token():
    if SIMULADO is not None:
        return "token-simulado"
    faltando = [v for v in ("ML_CLIENT_ID", "ML_CLIENT_SECRET", "ML_REFRESH_TOKEN") if not os.environ.get(v)]
    if faltando:
        sys.exit(f"Faltam as variáveis: {', '.join(faltando)}. Veja o GUIA-ATUALIZACAO.md.")
    r = http("POST", "/oauth/token", form={
        "grant_type": "refresh_token",
        "client_id": os.environ["ML_CLIENT_ID"],
        "client_secret": os.environ["ML_CLIENT_SECRET"],
        "refresh_token": os.environ["ML_REFRESH_TOKEN"],
    })
    # O Mercado Livre troca o refresh token a cada uso: é preciso guardar o novo.
    novo = r.get("refresh_token")
    destino = os.environ.get("NOVO_REFRESH_TOKEN_ARQUIVO")
    if novo and destino:
        with open(destino, "w") as f:
            f.write(novo)
    return r["access_token"]


def oferta_do_catalogo(token, ml_id):
    """Devolve (item_id, preco) da melhor oferta do produto no ML."""
    if ml_id.startswith("MLBU"):
        itens = http("GET", f"/user-products/{ml_id}/items", token)
        lista = (itens or {}).get("results") or []
        if lista:
            item = http("GET", f"/items/{lista[0]}", token) if isinstance(lista[0], str) else lista[0]
            if item and item.get("price") is not None and item.get("status", "active") == "active":
                return item.get("id"), float(item["price"])
        return None, None
    prod = http("GET", f"/products/{ml_id}", token)
    if not prod:
        return None, None
    bbw = prod.get("buy_box_winner")
    if bbw and bbw.get("price") is not None:
        return bbw.get("item_id"), float(bbw["price"])
    # sem "ganhador": pega a oferta mais barata do catálogo
    itens = http("GET", f"/products/{ml_id}/items", token) or {}
    ofertas = [i for i in itens.get("results", []) if i.get("price") is not None]
    if not ofertas:
        return None, None
    melhor = min(ofertas, key=lambda i: i["price"])
    return melhor.get("item_id"), float(melhor["price"])


def frete_e_prazo(token, item_id, cep):
    """Devolve (custo_frete, horas_ate_chegar) para o CEP, ou (None, None)."""
    if not cep or not item_id:
        return None, None
    r = http("GET", f"/items/{item_id}/shipping_options?zip_code={cep}", token)
    opcoes = (r or {}).get("options") or []
    melhor = None
    agora = datetime.now(BRT)
    for o in opcoes:
        data = ((o.get("estimated_delivery_time") or {}).get("date"))
        if not data:
            continue
        try:
            quando = datetime.fromisoformat(data.replace("Z", "+00:00"))
        except ValueError:
            continue
        horas = max(1, math.ceil((quando - agora).total_seconds() / 3600))
        custo = o.get("cost", o.get("list_cost"))
        if melhor is None or horas < melhor[1]:
            melhor = (float(custo) if custo is not None else None, horas)
    return melhor if melhor else (None, None)


def main():
    cfg = json.load(open(ARQ_CONFIG, encoding="utf-8"))
    dados = json.load(open(ARQ_PRODUTOS, encoding="utf-8"))
    cep = "".join(ch for ch in str(cfg.get("cep_entrega", "")) if ch.isdigit())
    if not cep:
        print("AVISO: cep_entrega vazio em tools/config.json — o prazo não será atualizado.")
    token = obter_token()

    ok, falhas, fora = 0, [], []
    for p in dados["produtos"]:
        if p.get("fonte") == "amazon" or not p.get("ml_id"):
            continue  # produto da Amazon: sem API, o preço é atualizado à mão
        try:
            item_id, preco_ml = oferta_do_catalogo(token, p["ml_id"])
        except Exception as e:  # erro de rede/API: mantém o valor anterior
            falhas.append(f"{p['id']}: {e}")
            continue
        if preco_ml is None:
            p["disponivel"] = False
            fora.append(f"{p['id']}: sem oferta ativa no ML")
            continue
        p["ml_item_id"] = item_id
        p["preco_ml"] = round(preco_ml, 2)
        p["preco"] = round(preco_ml * (1 + cfg["margem_sobre_ml"]), 2)
        try:
            frete, horas = frete_e_prazo(token, item_id, cep)
        except Exception as e:
            frete, horas = None, None
            falhas.append(f"{p['id']} (frete): {e}")
        if horas is not None:
            p["frete_ml"] = frete
            p["prazo_ml_horas"] = horas
        prazo_ml = p.get("prazo_ml_horas") or 0
        p["prazo_cliente_horas"] = prazo_ml + cfg["tempo_proprio_horas"]
        p["disponivel"] = prazo_ml <= cfg["prazo_max_ml_horas"]
        if not p["disponivel"]:
            fora.append(f"{p['id']}: ML entrega em {prazo_ml}h (> {cfg['prazo_max_ml_horas']}h)")
        ok += 1

    dados["atualizado_em"] = datetime.now(BRT).isoformat(timespec="minutes")
    dados["fonte"] = "API do Mercado Livre"
    with open(ARQ_PRODUTOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)

    print(f"Atualizados: {ok}/{sum(1 for p in dados['produtos'] if p.get('ml_id'))} (produtos da Amazon não entram)")
    for linha in fora:
        print("  FORA DO AR:", linha)
    for linha in falhas:
        print("  FALHA (mantido valor anterior):", linha)
    # Só falha o processo se nada foi atualizado (ex.: token inválido)
    if ok == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
