#!/usr/bin/env python3
"""
Passo único: autoriza o aplicativo na sua conta do Mercado Livre
e mostra o REFRESH TOKEN para salvar como segredo no GitHub.

Uso:  python3 tools/ml_autorizar.py
"""
import getpass, json, urllib.parse, urllib.request, urllib.error

client_id = input("Client ID (App ID) do seu aplicativo no ML: ").strip()
client_secret = getpass.getpass("Client Secret (não aparece ao digitar): ").strip()
redirect = input("URI de redirecionamento cadastrada no aplicativo: ").strip()

url = "https://auth.mercadolivre.com.br/authorization?" + urllib.parse.urlencode(
    {"response_type": "code", "client_id": client_id, "redirect_uri": redirect})
print("\n1) Abra este link, entre na sua conta do ML e clique em Permitir:\n")
print(url)
print("\n2) Você será levado para o endereço de redirecionamento. Copie o valor depois de 'code=' na barra de endereço.")
code = input("\nCole o code aqui: ").strip()

dados = urllib.parse.urlencode({"grant_type": "authorization_code", "client_id": client_id,
    "client_secret": client_secret, "code": code, "redirect_uri": redirect}).encode()
req = urllib.request.Request("https://api.mercadolibre.com/oauth/token", data=dados,
    headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"})
try:
    r = json.load(urllib.request.urlopen(req, timeout=30))
except urllib.error.HTTPError as e:
    raise SystemExit(f"Erro {e.code}: {e.read().decode(errors='replace')}")

print("\nPronto! Salve este valor no GitHub como o segredo ML_REFRESH_TOKEN:\n")
print(r["refresh_token"])
print("\n(Não compartilhe esse valor com ninguém.)")
