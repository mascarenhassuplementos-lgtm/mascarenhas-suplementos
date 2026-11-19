// Funções de frete (navegador: window.FRETE; Node: module.exports)
const FRETE = (function () {
  const r2 = n => Math.round(n * 100) / 100;
  const r3 = n => Math.round(n * 1000) / 1000;

  // kg de 1 unidade, a partir do campo "tam" (ou peso_kg explícito)
  function pesoUnidade(p) {
    if (typeof p.peso_kg === "number") return p.peso_kg;
    const t = p.tam || "";
    const m = t.match(/(\d+(?:,\d+)?)\s*(kg|g)\b/i);
    if (m) {
      let kg = parseFloat(m[1].replace(",", ".")) / (m[2].toLowerCase() === "g" ? 1000 : 1);
      const mult = t.match(/(\d+)\s*(?:un\.?\s*)?[×x]/i);
      if (mult) kg *= parseInt(mult[1], 10);
      return r3(kg);
    }
    const cx = t.match(/caixa\s+(\d+)\s*un/i);
    if (cx) return r3(parseInt(cx[1], 10) * 0.05 + 0.1);
    if (/c[aá]psula|comprimido|tablete|softgel|goma|sach[eê]|dose/i.test(t)) return 0.3;
    if (/\d\s*(ml|L)\b/i.test(t)) return 0.4;
    return 0.5;
  }

  // caixa {a: altura, l: largura, c: comprimento} em cm
  function caixaPara(kg) {
    if (kg <= 1) return { a: 15, l: 15, c: 20 };
    if (kg <= 3) return { a: 20, l: 20, c: 30 };
    if (kg <= 6) return { a: 25, l: 30, c: 40 };
    return { a: 30, l: 40, c: 50 };
  }

  // peso = soma × 1,15 + 0,2 kg; valor declarado = subtotal
  function pacote(its) {
    let soma = 0, valor = 0;
    for (const i of its) {
      soma += pesoUnidade(i) * i.q;
      valor += i.preco * i.q;
    }
    const peso = r2(soma * 1.15 + 0.2);
    return { peso, caixa: caixaPara(peso), valor: r2(valor) };
  }

  function prazoTotalDias(prazoHorasLoja, diasTransp) {
    return Math.ceil(prazoHorasLoja / 24) + 1 + diasTransp;
  }

  // até 3 opções: mais barata, mais rápida e a próxima por preço; ordem por preço
  function escolherOpcoes(lista, taxaEmbalagem) {
    const ops = lista
      .filter(o => typeof o.preco === "number" && isFinite(o.preco))
      .map(o => Object.assign({}, o, { preco: r2(o.preco + (taxaEmbalagem || 0)) }))
      .sort((a, b) => a.preco - b.preco);
    if (!ops.length) return [];
    const esc = [ops[0]];
    const rapida = ops.reduce((m, o) => (o.dias < m.dias ? o : m), ops[0]);
    if (!esc.includes(rapida)) esc.push(rapida);
    for (const o of ops) if (esc.length < 3 && !esc.includes(o)) esc.push(o);
    return esc.sort((a, b) => a.preco - b.preco);
  }

  // soma n dias úteis (pula sábado e domingo) sem alterar a data recebida
  function somaDiasUteis(data, n) {
    const d = new Date(data.getTime());
    let falta = Math.max(0, Math.floor(n) || 0);
    while (falta > 0) {
      d.setDate(d.getDate() + 1);
      const w = d.getDay();
      if (w !== 0 && w !== 6) falta--;
    }
    return d;
  }

  return { pesoUnidade, caixaPara, pacote, prazoTotalDias, escolherOpcoes, somaDiasUteis };
})();

if (typeof module!=="undefined") module.exports = FRETE; else window.FRETE = FRETE;
