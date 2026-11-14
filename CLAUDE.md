# Mascarenhas Suplementos — contexto do projeto

> Arquivo de memória do projeto. Numa conversa nova com o Claude, envie este arquivo
> (ou conecte o repositório) e diga: **"Leia o CLAUDE.md e continue de onde paramos."**
> Atualize a seção "Histórico" ao fim de cada sessão.
> Última atualização: **14/11/2026, 19h**.

## A loja

- **Nome:** Mascarenhas Suplementos — loja de suplementos em **Salvador/BA**.
- **Lema (bio do Instagram):** "A glória da segunda casa será maior – Ageu 2:9".
- **Modelo:** revenda de marcas originais (Growth, Dux, Max Titanium, Integralmédica, True Source,
  Dark Lab, Soldiers, Vitafor, Black Skull, FTW etc.). Preço do site = custo no Mercado Livre/Amazon **+ 10%**.
  A loja só compra o produto depois que o cliente paga.
- **Entrega:** até 48h em Salvador (taxa R$ 15) · **retirada grátis** no Loteamento Aquarius,
  Rua Magno Valente, 484 – Edf. Georges Pompidou.
- **Pagamento:** **Pix antecipado** (chave celular **(71) 99704-4675**, QR Code gerado no site) ou cartão (link pelo WhatsApp).
  CNPJ novo ainda não aberto.
- **Contatos:** WhatsApp (71) 99704-4675 · mascarenhassuplementos@gmail.com · Instagram @mascarenhassuplementos.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| **Site oficial** | https://mascarenhassuplementos-lgtm.github.io/mascarenhas-suplementos/ (GitHub Pages) |
| **Site novo (prévia)** | `.../index-novo.html` — visual "Ouro Estrutural" + Pix antecipado + ficha + email. **Ainda não está no endereço principal.** |
| Ficha do pedido | `site/pedido.html` — aberta pelo link que vem em cada pedido |
| Repositório | github.com/mascarenhassuplementos-lgtm/mascarenhas-suplementos (login: "Continue with Google" com o Gmail da loja) |
| Página principal | `site/index.html` (configuração no objeto `CONFIG`; a lista `let PRODUTOS = [...]` é só reserva) |
| Preços e prazos | `site/produtos.json` — 457 produtos: 104 do Mercado Livre, 353 da Amazon |
| Atualizador de preços | `tools/atualizar_precos.py` + `.github/workflows/atualizar-precos.yml` |
| Configuração do atualizador | `tools/config.json` (margem 10%, **sem mínimo em R$**, CEP 41771080, prazo máx. ML 24h) |
| Conferir pedido antes de comprar | `site/conferir.html` |
| Catálogos | `catalogo/` (PDFs e textos para WhatsApp) — **ainda com preços antigos** |
| Guia passo a passo | `GUIA-ATUALIZACAO.md` |
| Cópia local | Área de Trabalho › `Mascarenhas Suplementos` (desatualizada — o GitHub vale) |
| Imagens novas | Área de Trabalho › `Mascarenhas Suplementos - Imagens` › `instagram-nova-logo/` (9 posts + legendas) e `design-site/` (proposta visual) |

## Como funciona um pedido (site novo)

1. Cliente monta o carrinho, preenche a ficha e escolhe **Pix antecipado** ou cartão.
2. **Pix:** aparece o valor, o **QR Code** e o **Pix copia e cola** já com o valor exato (padrão EMV do Banco Central,
   chave `+5571997044675`, favorecido "MASCARENHAS SUPLEMENTOS", cidade SALVADOR). O cliente paga e toca em
   **"Já paguei · enviar pedido pelo WhatsApp"**; manda o comprovante na conversa.
   O site **não confirma** o pagamento sozinho — conferir o comprovante no app do banco antes de comprar.
3. A mensagem do WhatsApp traz o link **"Ficha do pedido"** (`pedido.html#p=...`, dados do pedido codificados no link).
   - O cliente que abrir vê só o resumo.
   - Na **área da loja** (rodapé da ficha → "Área da loja" → senha **813125**, uma vez por aparelho) aparecem
     o botão **"Comprar no Amazon / Mercado Livre"** de cada item, o custo de referência e a margem estimada.
4. Ao mesmo tempo, chega um **email automático** em mascarenhassuplementos@gmail.com (via **FormSubmit**, gratuito,
   **ativado em 14/11**) com itens, links de compra do estoque e ficha de entrega. O cliente não vê.
   - Configuração: `CONFIG.emailPedidos` no `index-novo.html`. O email da loja aparece no código da página;
     o FormSubmit oferece um código aleatório para esconder o endereço (trocar quando quiser).

## Como os preços funcionam

- **Regra (desde 14/11):** preço do site = custo × 1,10, arredondado em centavos. Sem lucro mínimo em R$.
- **Mercado Livre (104):** a automação roda a cada 6h, mas **NÃO atualiza preços**: faltam os segredos do ML no GitHub
  (log: "Segredos do Mercado Livre ainda não cadastrados"). Última conferência: **manual, 14/11 13h10**.
  Prazos de entrega do ML são de 9/11.
- **Amazon (353):** conferência manual. A Amazon pede CAPTCHA depois de ~130 consultas seguidas.
- **Segredos** (Settings → Secrets and variables → Actions): `ML_CLIENT_ID`, `ML_CLIENT_SECRET`, `ML_REFRESH_TOKEN`,
  `GH_PAT`. Passo a passo no `GUIA-ATUALIZACAO.md` (Passos 3 a 6). Nunca colar esses valores em conversa.

### Situação dos preços (14/11/2026)

| Grupo | Conferido em | Observação |
|---|---|---|
| Mercado Livre — 104 | 14/11 | 66 mudaram. Dux Cafeína 90 cáps fora do ar. |
| Amazon — Whey e Creatina (58) | 14/11 | 39 mudaram; combo Black Skull fora do ar. |
| Amazon — Hipercalórico, Albumina, Pré-treino, Hidratação, Glutamina, BCAA, Aminoácidos, parte de Termogênico (128) | 14/11 | 60 mudaram; 13 estavam abaixo do custo (corrigidos); 3 fora do ar. |
| Amazon — resto de Termogênico, Vitaminas, Colágeno, Barras, Alimentos Fit, Acessórios (166) | **9/11** | Falta conferir. |

## Identidade visual

- **Logo:** casa prata + casa dourada com haltere, "MASCARENHAS SUPLEMENTOS". Sempre sobre preto.
  Arquivos: `site/logo.png` (512) e `site/logo-horizontal.png` (664×438). Melhor cópia local: `mascarenhas-instagram-1080.png` (Área de Trabalho).
- **Cores:** preto `#0A0A0A` · dourado `#F5B800` · âmbar `#E8941A` · prata `#C9CDD2` · osso `#F2EFE8`.
- **Site novo ("Ouro Estrutural"):** títulos Big Shoulders Display, textos Instrument Sans, legendas Geist Mono,
  versículo em Instrument Serif. Desenho das duas casas no topo, régua de 48h, categorias como anilhas,
  cartões escuros com linha dourada. Manifesto: `design-site/filosofia-ouro-estrutural.md`.
- **Posts:** Inter 900/800 sobre preto com dourado (9 posts prontos).

## Outros lugares com dados da loja

- **Artefatos no Claude:**
  - Planilha "Revisão de preços Amazon — 14/11/2026" — https://claude.ai/artifact/Pwni5DxB2xa3R84cRFbcpX
  - "Nova Identidade Visual" (marca, banner, posts), "Painel Administrativo" (**logo antiga no ar**),
    "Plano de lançamento", "Quiz", quadros antigos verdes.
- **Instagram:** **9 posts novos publicados em 14/11** pelo conector **Windsor.ai for Social Media**
  (conta Windsor em plano Trial; imagens hospedadas em `site/instagram/*.jpg`). Os 24 posts antigos ainda estão
  no ar: o conector **não exclui posts** (só cria posts/stories e gerencia comentários) — excluir pelo app do celular.
- **Shopify** (mbses5-e7.myshopify.com): só teste, trial — não é a loja oficial.
- **Google:** Perfil da Empresa (9/11). **Asana:** "Rastreador de fornecedores".

## Pendências

- [ ] **Publicar o site novo**: dizer "pode publicar" → `index-novo.html` vira o `index.html` e a página de teste é apagada.
- [ ] **Instagram:** excluir os 24 posts antigos pelo app do celular (os 9 novos já estão publicados).
- [ ] Windsor.ai está em **Trial** — ver plano antes de vencer, se quiser continuar publicando pelo Claude.
- [ ] **Segredos do Mercado Livre no GitHub** (`GUIA-ATUALIZACAO.md`, Passos 3 a 6) e rodar "Run workflow". O `GH_PAT` vence em 1 ano.
- [ ] **Amazon:** conferir os 166 produtos que faltaram.
- [ ] **Painel com a logo nova:** abrir conversa a partir da página do Painel, anexar `painel-administrativo-logo-nova.html` e pedir para publicar.
- [ ] Refazer catálogo em PDF e textos de WhatsApp (`catalogo/`) com os preços novos.
- [ ] Liberar a "Área da loja" (senha 813125) no celular da loja.
- [ ] Abrir o CNPJ novo e preencher `cnpj` no `CONFIG` do site (a chave Pix pode passar a ser o CNPJ).
- [ ] Conseguir a logo em alta resolução. Decidir se a Shopify continua.

## Histórico

- **14/11/2026 (19h)** — 9 posts novos publicados no Instagram via Windsor.ai (ordem 09 → 01, com legendas).

- **14/11/2026 (16h)** —
  - Proposta visual "Ouro Estrutural" (imagem + manifesto) e site novo montado em `index-novo.html`.
  - **Pix antecipado** com QR Code e copia e cola (chave (71) 99704-4675).
  - **Ficha do pedido** (`pedido.html`) com área da loja protegida por senha: links de compra do estoque e custo.
  - **Email automático** de cada pedido para o Gmail da loja via FormSubmit (ativado; pedido de teste "TESTE" recebido).
  - Email enviado ao Gmail da loja com os links, a senha e as instruções.
  - 9 posts novos do Instagram criados com a logo nova (falta excluir os antigos e publicar).
- **14/11/2026 (tarde)** —
  - Apagado o ramo `nova-logo`. Painel Administrativo refeito com a logo nova (falta publicar pela página dele).
  - Conferidos na Amazon 186 produtos; parado por CAPTCHA. Conferidos à mão os 104 do Mercado Livre.
  - Regra de preço trocada para **custo + 10% sem mínimo** em todo o site.
  - Descoberto que a automação do ML nunca atualizou preços (segredos não cadastrados).
  - Criada a planilha "Revisão de preços Amazon — 14/11/2026".
- **14/11/2026 (manhã)** — Nova logo aplicada no site, quadro "Nova Identidade Visual", foto do Instagram,
  tema Shopify de teste e este arquivo de contexto.
- **12/11/2026** — Shopify de teste, quadros de identidade visual e posts, plano de lançamento e quiz.
- **9–10/11/2026** — Repositório e site no GitHub Pages, automação de preços pelo Mercado Livre, Perfil da Empresa no Google.
