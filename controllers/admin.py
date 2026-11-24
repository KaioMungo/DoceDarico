import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from models.produto import Produto
from models.pedido import Pedido

UPLOAD_FOLDER = "static/img/produtos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

admin_bp = Blueprint("admin", __name__)

SENHA_ADMIN = "doce123"

def admin_logado():
    return session.get("admin") == True

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == SENHA_ADMIN:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
        return render_template("admin/login.html", erro="Senha incorreta!")
    return render_template("admin/login.html")

@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("cliente.index"))

@admin_bp.route("/dashboard")
def dashboard():
    if not admin_logado():
        return redirect(url_for("admin.login"))
    pedidos = Pedido.query.order_by(Pedido.criado_em.desc()).all()
    produtos = Produto.query.all()
    return render_template("admin/dashboard.html", pedidos=pedidos, produtos=produtos)

@admin_bp.route("/produto/novo", methods=["GET", "POST"])
def novo_produto():
    if not admin_logado():
        return redirect(url_for("admin.login"))
    if request.method == "POST":
        nome = request.form.get("nome")
        preco = float(request.form.get("preco"))
        categoria = request.form.get("categoria")

        imagem = None
        if "imagem" in request.files:
            file = request.files["imagem"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imagem = filename

        produto = Produto(nome=nome, preco=preco, categoria=categoria, imagem=imagem)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/novo_produto.html")

@admin_bp.route("/produto/deletar/<int:id>")
def deletar_produto(id):
    if not admin_logado():
        return redirect(url_for("admin.login"))
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/produto/estoque/<int:id>", methods=["POST"])
def atualizar_estoque(id):
    if not admin_logado():
        return redirect(url_for("admin.login"))
    produto = Produto.query.get(id)
    novo_estoque = int(request.form.get("estoque"))
    produto.estoque = novo_estoque
    if novo_estoque > 0:
        produto.disponivel = True
    else:
        produto.disponivel = False
    db.session.commit()
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/produto/editar/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    if not admin_logado():
        return redirect(url_for("admin.login"))
    produto = Produto.query.get(id)
    if request.method == "POST":
        produto.nome = request.form.get("nome")
        produto.preco = float(request.form.get("preco"))
        produto.categoria = request.form.get("categoria")

        if "imagem" in request.files:
            file = request.files["imagem"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                produto.imagem = filename

        db.session.commit()
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/editar_produto.html", produto=produto)