from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
W,H=A4; VERDE=colors.HexColor("#14894a"); ESC=colors.HexColor("#14201b"); CINZA=colors.HexColor("#5b6b64")
c=canvas.Canvas("entregas/ficha-entrega-motoboy.pdf",pagesize=A4); c.setTitle("Ficha de entrega – Mascarenhas Suplementos"); c.setAuthor("Mascarenhas Suplementos")
M=12*mm; HW=W-2*M
def campo(x,y,w,rot,h=8*mm):
    c.setFont("Helvetica",7.5); c.setFillColor(CINZA); c.drawString(x+1.5*mm,y+h-3.2*mm,rot.upper())
    c.setStrokeColor(colors.HexColor("#9aa8a1")); c.setLineWidth(0.6); c.rect(x,y,w,h)
def caixa(x,y,txt,marc=False):
    c.setStrokeColor(ESC); c.setLineWidth(0.8); c.rect(x,y,3.6*mm,3.6*mm)
    c.setFont("Helvetica",9); c.setFillColor(ESC); c.drawString(x+5*mm,y+0.6*mm,txt)
def ficha(top):
    y=top
    c.setFillColor(VERDE); c.rect(M,y-12*mm,HW,12*mm,fill=1,stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold",15); c.setFillColor(colors.white); c.roundRect(M+1.5*mm, y-11.3*mm, 11*mm, 10.6*mm, 2*mm, fill=1, stroke=0)
    c.drawImage("logo/segunda-casa/simbolo.png", M+2*mm, y-11*mm, 10*mm, 10*mm*320/340, mask="auto")
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold",15); c.drawString(M+14*mm,y-8*mm,"MASCARENHAS SUPLEMENTOS")
    c.setFont("Helvetica",9); c.drawString(M+14*mm+c.stringWidth("MASCARENHAS SUPLEMENTOS","Helvetica-Bold",15)+5*mm,y-8*mm,"FICHA DE ENTREGA")
    c.setFont("Helvetica-Bold",9); c.drawRightString(M+HW-4*mm,y-5.5*mm,"Loja: (71) 99704-4675")
    c.setFont("Helvetica",8); c.drawRightString(M+HW-4*mm,y-9.5*mm,"Aquarius – Rua Magno Valente, 484")
    y-=12*mm+2*mm
    g=2*mm; L=8*mm
    w3=(HW-2*g)/3
    for i,r in enumerate(["Nº do pedido","Data","Entregar até (data e hora)"]): campo(M+i*(w3+g),y-L,w3,r)
    y-=L+g
    campo(M,y-L,HW*0.62,"Cliente (nome)"); campo(M+HW*0.62+g,y-L,HW*0.38-g,"Telefone / WhatsApp"); y-=L+g
    campo(M,y-L,HW*0.80,"Endereço (rua, avenida)"); campo(M+HW*0.80+g,y-L,HW*0.20-g,"Número"); y-=L+g
    campo(M,y-L,HW*0.40,"Complemento (apto, bloco)"); campo(M+HW*0.40+g,y-L,HW*0.35-g,"Bairro"); campo(M+HW*0.75+g,y-L,HW*0.25-g,"CEP"); y-=L+g
    campo(M,y-L,HW*0.62,"Ponto de referência"); campo(M+HW*0.62+g,y-L,HW*0.38-g,"Melhor horário"); y-=L+g
    # itens
    IH=24*mm; campo(M,y-IH,HW*0.62,"Itens (qtd e produto)",IH)
    for k in range(1,4):
        c.setStrokeColor(colors.HexColor("#dbe3df")); c.line(M+2*mm,y-IH+k*5.5*mm,M+HW*0.62-2*mm,y-IH+k*5.5*mm)
    # pagamento
    px=M+HW*0.62+g; pw=HW*0.38-g; campo(px,y-IH,pw,"Pagamento",IH)
    caixa(px+2*mm,y-9*mm,"JÁ PAGO (Pix)"); caixa(px+2*mm,y-14*mm,"COBRAR na entrega")
    c.setFont("Helvetica-Bold",9); c.setFillColor(ESC); c.drawString(px+2*mm,y-20*mm,"Valor a cobrar: R$ ________")
    y-=IH+g
    campo(M,y-L,HW,"Observações"); y-=L+g
    # recebimento
    RH=13*mm; campo(M,y-RH,HW*0.5,"Recebido por (nome legível)",RH); campo(M+HW*0.5+g,y-RH,HW*0.25-g,"Data e hora",RH); campo(M+HW*0.75+g,y-RH,HW*0.25-g,"Assinatura",RH)
    y-=RH+g
    campo(M,y-L,HW*0.5,"Motoboy"); campo(M+HW*0.5+g,y-L,HW*0.5-g,"Taxa de entrega paga ao motoboy (R$)")
    c.setFont("Helvetica-Oblique",7.5); c.setFillColor(CINZA)
    c.drawString(M,y-L-4*mm,"Motoboy: confira o nome do recebedor. Não entregue sem confirmação de pagamento quando estiver marcado \"COBRAR\". Dúvidas: ligue para a loja.")
top=H-M
ficha(top)
c.setStrokeColor(CINZA); c.setDash(4,3); c.line(M-6*mm,H/2,W-M+6*mm,H/2); c.setDash()
c.setFont("Helvetica",7); c.setFillColor(CINZA); c.drawCentredString(W/2,H/2+1.5*mm,"✂  recorte aqui")
ficha(H/2-6*mm)
c.save(); print("ok")
