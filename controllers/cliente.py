from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from models.produto import Produto
from models.pedido import Pedido, ItemPedido
import urllib.parse

cliente_bp = Blueprint("cliente", __name__)

WHATSAPP_NUMERO = "5511997630932"

@cliente_bp.route("/")
def index():
    produtos = Produto.query.filter_by(disponivel=True).all()
    return render_template("index.html", produtos=produtos)

@cliente_bp.route("/sobre")
def sobre():
    return render_template("sobre.html")

@cliente_bp.route("/fazer_pedido", methods=["POST"])
def fazer_pedido():
    cliente = request.form.get("cliente")
    telefone = request.form.get("telefone")
    produtos_ids = request.form.getlist("produtos")

    if not cliente or not telefone or not produtos_ids:
        return redirect(url_for("cliente.index"))

    pedido = Pedido(cliente=cliente, telefone=telefone, total=0)
    db.session.add(pedido)
    db.session.flush()

    total = 0
    itens_mensagem = []

    for produto_id in produtos_ids:
        quantidade = int(request.form.get(f"quantidade_{produto_id}", 0))

        if quantidade <= 0:
            continue

        produto = Produto.query.get(produto_id)

        if produto.estoque < quantidade:
            quantidade = produto.estoque

        if quantidade <= 0:
            continue

        item = ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=produto.preco
        )
        subtotal = produto.preco * quantidade
        total += subtotal

        produto.estoque -= quantidade
        if produto.estoque == 0:
            produto.disponivel = False

        db.session.add(item)
        itens_mensagem.append(f"• {produto.nome} x{quantidade} — R${subtotal:.2f}")

    pedido.total = total
    db.session.commit()

    # monta a mensagem do whatsapp
    itens_texto = "\n".join(itens_mensagem)
    mensagem = f""" *Novo Pedido - Doce Darico*

  *Cliente:* {cliente}
  *Telefone:* {telefone}

*Itens:*
{itens_texto}

  *Total: R${total:.2f}*"""

    mensagem_encoded = urllib.parse.quote(mensagem)
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMERO}?text={mensagem_encoded}"

    return redirect(whatsapp_url)