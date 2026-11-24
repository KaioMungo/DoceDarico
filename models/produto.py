from database import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    imagem = db.Column(db.String, nullable=True)
    estoque = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Produto {self.nome}>"