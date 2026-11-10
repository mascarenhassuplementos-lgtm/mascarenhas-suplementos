# Guia: atualização automática de preços e prazos

O site lê os preços e prazos do arquivo `site/produtos.json`.
A cada 6 horas o GitHub roda `tools/atualizar_precos.py`, que:

1. consulta na **API oficial do Mercado Livre** o preço atual de cada produto;
2. consulta o **frete e o prazo de entrega até o seu CEP**;
3. calcula o preço do site (**preço do ML + 10%**);
4. calcula o prazo para o cliente (**prazo do ML + 24h** suas);
5. marca como **indisponível** o produto sem estoque ou que o ML entregue em mais de 24h;
6. publica o site atualizado.

Custo: **R$ 0** (API do ML, GitHub e GitHub Pages são gratuitos).

---

## Passo 1 — Ajustar a configuração

Abra `tools/config.json` e preencha:

| Campo | O que é | Valor atual |
|---|---|---|
| `cep_entrega` | CEP onde você recebe as compras do ML | **vazio — preencher** |
| `margem_sobre_ml` | quanto somar ao preço do ML | `0.10` (10%) |
| `tempo_proprio_horas` | seu tempo para embalar e entregar | `24` |
| `prazo_max_ml_horas` | acima disso o produto sai do ar | `24` |
| `prazo_max_cliente_horas` | prazo prometido | `48` |

Em `site/index.html`, troque também `whatsapp` e `chavePix`.

## Passo 2 — Criar o repositório no GitHub

1. Crie uma conta em **github.com** (grátis), se ainda não tiver.
2. Crie um repositório novo, por exemplo `mascarenhas-suplementos`.
3. Envie para ele **todo o conteúdo desta pasta** (`site/`, `tools/`, `.github/` e este guia).
4. Em **Settings → Pages**, em *Source*, escolha **GitHub Actions**.

O endereço do site será `https://SEU-USUARIO.github.io/mascarenhas-suplementos/`.

## Passo 3 — Criar o aplicativo no Mercado Livre

1. Entre em **developers.mercadolivre.com.br** com a sua conta do ML.
2. Vá em **Minhas aplicações → Criar aplicação**.
3. Preencha nome (ex.: "Mascarenhas Suplementos Preços") e descrição.
4. Em **URI de redirecionamento**, coloque o endereço do seu site do Passo 2
   (ex.: `https://SEU-USUARIO.github.io/mascarenhas-suplementos/`).
5. Em permissões/escopos, marque leitura (*read*) e **offline_access**
   (necessário para o acesso continuar funcionando sozinho).
6. Salve. Anote o **App ID (Client ID)** e a **Secret Key (Client Secret)**.

## Passo 4 — Autorizar e pegar o refresh token

No seu computador, dentro desta pasta, rode:

```
python3 tools/ml_autorizar.py
```

Ele pede o Client ID, o Client Secret e a URI, mostra um link, você clica em
**Permitir** no ML e cola o `code` que aparece na barra de endereço.
No fim, ele mostra o **refresh token**.

## Passo 5 — Salvar os segredos no GitHub

No repositório: **Settings → Secrets and variables → Actions → New repository secret**.
Crie estes 4 segredos:

| Nome | Valor |
|---|---|
| `ML_CLIENT_ID` | App ID do Passo 3 |
| `ML_CLIENT_SECRET` | Secret Key do Passo 3 |
| `ML_REFRESH_TOKEN` | o valor do Passo 4 |
| `GH_PAT` | um token do GitHub (veja abaixo) |

**Por que o `GH_PAT`?** O Mercado Livre troca o refresh token toda vez que ele é usado.
O GitHub precisa de permissão para guardar o novo valor sozinho.
Crie em **github.com → Settings → Developer settings → Fine-grained tokens**,
só para o repositório `mascarenhas-suplementos`, com permissão **Secrets: Read and write**.

## Passo 6 — Rodar pela primeira vez

No repositório: **Actions → Atualizar preços e publicar site → Run workflow**.
Em 1–2 minutos o site estará no ar com preços do dia.
No rodapé do site aparece "Preços e prazos atualizados em …".

---

## Se algo der errado

- **A tarefa falhou com "HTTP 400/401" no token:** o refresh token expirou ou foi usado
  fora do GitHub. Rode o Passo 4 de novo e atualize o segredo `ML_REFRESH_TOKEN`.
- **Um produto aparece como "Indisponível":** o ML está sem oferta ou entrega em mais de 24h
  no seu CEP. Ele volta sozinho quando normalizar.
- **"FALHA (mantido valor anterior)" no log:** a API não respondeu para aquele produto;
  o site mantém o último preço conhecido.
- **Produtos com código `MLBU…`** (Growth pouch 500 g e Dux Whey 900 g) usam outro tipo de
  anúncio no ML. Se aparecerem sempre como indisponíveis, troque o `ml_id` em
  `site/produtos.json` pelo código `MLB…` do anúncio de catálogo do mesmo produto.

## Adicionar ou remover produtos

Edite `site/produtos.json`. Cada produto precisa de `id`, `cat`, `nome`, `tam`, `img` e
`ml_id` (o código `MLB…` que aparece no link do produto no ML, depois de `/p/`).
O resto o atualizador preenche.

## Antes de comprar para um cliente (produtos da Amazon e do ML)

Os preços da Amazon não se atualizam sozinhos. Sempre que chegar um pedido:

1. Abra **https://mascarenhassuplementos-lgtm.github.io/mascarenhas-suplementos/conferir.html** (salve nos favoritos do celular).
2. Cole a mensagem inteira do pedido que chegou no WhatsApp e toque em **Conferir itens**.
3. Para cada item, toque em **Comprar na Amazon** / **Comprar no Mercado Livre**, veja o preço de hoje e digite no campo.
4. A página mostra:
   - verde **"OK, pode comprar"**: lucro de pelo menos R$ 5 por unidade;
   - amarelo **"Lucro baixo"**: o preço subiu, mas ainda não dá prejuízo;
   - vermelho **"PREJUÍZO"**: fale com o cliente antes de comprar (ou procure outra oferta).
5. Se um produto subiu de vez, me peça para atualizar o preço no site.
