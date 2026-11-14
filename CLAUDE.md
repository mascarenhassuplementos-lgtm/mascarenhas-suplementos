# Mascarenhas Suplementos — contexto do projeto

> Arquivo de memória do projeto. Numa conversa nova com o Claude, envie este arquivo
> (ou conecte o repositório) e diga: **"Leia o CLAUDE.md e continue de onde paramos."**
> Atualize a seção "Histórico" ao fim de cada sessão.

## A loja

- **Nome:** Mascarenhas Suplementos — loja de suplementos em **Salvador/BA**.
- **Lema (bio do Instagram):** "A glória da segunda casa será maior – Ageu 2:9".
- **Modelo:** revenda de marcas originais (Growth, Dux, Max Titanium, Integralmédica, True Source,
  Dark Lab, Soldiers, Vitafor, Black Skull, FTW etc.). O preço vem do Mercado Livre/Amazon + margem.
- **Entrega:** até 48h em Salvador (taxa R$ 15) · **retirada grátis** no Loteamento Aquarius,
  Rua Magno Valente, 484 – Edf. Georges Pompidou.
- **Pagamento:** Pix ou cartão. A chave Pix é enviada pelo WhatsApp (CNPJ novo ainda não aberto).
- **Contatos:** WhatsApp (71) 99704-4675 · mascarenhassuplementos@gmail.com · Instagram @mascarenhassuplementos.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| **Site oficial** | https://mascarenhassuplementos-lgtm.github.io/mascarenhas-suplementos/ (GitHub Pages) |
| Repositório | github.com/mascarenhassuplementos-lgtm/mascarenhas-suplementos (login: "Continue with Google" com o Gmail da loja) |
| Página do site | `site/index.html` (configuração no objeto `CONFIG` dentro do `<script>`) |
| Preços e prazos | `site/produtos.json` — 457 produtos: 104 do Mercado Livre, 353 da Amazon |
| Atualizador de preços | `tools/atualizar_precos.py` + `.github/workflows/atualizar-precos.yml` |
| Configuração do atualizador | `tools/config.json` (margem 10%, mínimo R$ 5, CEP 41771080, prazo máx. 48h) |
| Catálogos e tabela de preços | `catalogo/` (PDFs e textos para WhatsApp) |
| Ficha de entrega do motoboy | `entregas/` |
| Logos antigas | `logo/segunda-casa/` |
| Guia passo a passo | `GUIA-ATUALIZACAO.md` |

## Como os preços se atualizam

- A automação roda **a cada 6h** (06h, 12h, 18h e 00h de Brasília), também a cada push na `main`.
- Produtos do **Mercado Livre**: preço = preço do ML + 10% (mínimo R$ 5 de margem); prazo = prazo do ML + 24h;
  sai do ar se não tiver estoque ou se o ML demorar mais de 24h.
- Produtos da **Amazon**: **não** se atualizam sozinhos (a Amazon não tem API gratuita) — preço trocado à mão.
- Segredos no GitHub (Settings → Secrets → Actions): `ML_CLIENT_ID`, `ML_CLIENT_SECRET`,
  `ML_REFRESH_TOKEN` (trocado sozinho a cada rodada) e `GH_PAT`. Nunca colar esses valores em conversa.

## Identidade visual (nova, desde 14/11/2026)

- **Logo:** casa prata + casa dourada com um haltere na frente, escrito "MASCARENHAS SUPLEMENTOS".
  Sempre sobre fundo **preto**; em fundo claro, dentro de um bloco preto.
- **Arquivos no site:** `site/logo.png` (quadrado 512, ícone e compartilhamento) e `site/logo-horizontal.png` (cabeçalho).
- **Cores:** preto `#0A0A0A` · dourado `#F5B800` · laranja ouro `#E8941A` · prata `#C9CDD2` · branco `#F5F5F5`.
- **Fonte:** Inter (títulos 900, texto 400–600). Nos posts: Barlow Condensed + Barlow.
- A logo original recebida tem só 512 px de largura — pedir/guardar a versão em alta resolução.

## Outros lugares com dados da loja

- **Artefatos no Claude:** "Mascarenhas Suplementos — Nova Identidade Visual" (marca, banner, 3 posts e
  página inicial, já com a logo nova), "Painel Administrativo" (ainda com a logo antiga),
  "Plano de lançamento", "Quiz", e os quadros antigos "Identidade Visual" e "Posts" (cores verdes).
- **Shopify** ("Minha loja", mbses5-e7.myshopify.com): **só teste, em plano trial — não é a loja oficial.**
  108 produtos em rascunho/arquivados, 0 pedidos. Existe um tema não publicado "Horizon — nova logo Mascarenhas".
- **Google:** Perfil da Empresa criado em 9/11/2026.
- **Asana:** projeto "Rastreador de fornecedores".
- **Instagram:** @mascarenhassuplementos — foto de perfil nova em `mascarenhas-instagram-1080.png` (Área de Trabalho).

## Pendências

- [ ] Abrir o CNPJ novo e preencher `cnpj` e `chavePix` no `CONFIG` do site.
- [ ] Trocar a logo do "Painel Administrativo" (abrir uma conversa a partir da página dele).
- [ ] Conseguir a logo em alta resolução.
- [ ] Decidir se a Shopify continua (se não, deixar o trial expirar).
- [ ] Apagar o ramo `nova-logo` no GitHub (sobra, não afeta o site).
- [ ] Preços da Amazon: revisar à mão periodicamente.

## Histórico

- **14/11/2026** — Nova logo aplicada no site (cabeçalho preto, cores preto e dourado), criado o quadro
  "Nova Identidade Visual" com posts, preparada a foto do Instagram, criada cópia do tema Shopify (não publicada)
  e este arquivo de contexto.
- **12/11/2026** — Shopify de teste, quadros de identidade visual e posts, plano de lançamento e quiz.
- **9–10/11/2026** — Repositório e site no GitHub Pages, automação de preços pelo Mercado Livre, Perfil da Empresa no Google.
