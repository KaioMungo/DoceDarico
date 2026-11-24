from database import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pendente")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

    def __repr__(self):
        return f"<Pedido {self.id} - {self.cliente}>"


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    produto = db.relationship("Produto")

    def __repr__(self):
        return f"<ItemPedido {self.produto_id} x{self.quantidade}>"