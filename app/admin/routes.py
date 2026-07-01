from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Produto, User, Cart, Rating
import os
import re

admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return current_user.is_authenticated and current_user.is_admin

@admin.route("/")
@login_required
def dashboard():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    total_produtos = Produto.query.count()
    total_users = User.query.count()
    total_carrinhos = Cart.query.count()
    total_avaliacoes = Rating.query.count()

    return render_template(
        "admin/dashboard.html",
        total_produtos=total_produtos,
        total_users=total_users,
        total_carrinhos=total_carrinhos,
        total_avaliacoes=total_avaliacoes
    ) 

def gerar_slug(nome):
    slug = nome.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


@admin.route("/produtos")
@login_required
def produtos():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    produtos = Produto.query.order_by(Produto.id.desc()).all()
    return render_template("admin/produtos.html", produtos=produtos)


@admin.route("/produtos/novo", methods=["GET", "POST"])
@login_required
def novo_produto():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        nome = request.form.get("nome")
        preco = float(request.form.get("preco"))
        preco_antigo = request.form.get("preco_antigo") or None
        desconto = request.form.get("desconto") or None
        categoria = request.form.get("categoria")
        descricao = request.form.get("descricao")
        stock = int(request.form.get("stock") or 0)

        promocao = request.form.get("promocao") == "on"
        destaque = request.form.get("destaque") == "on"
        ativo = request.form.get("ativo") == "on"

        imagem_file = request.files.get("imagem")
        imagem_path = ""

        if imagem_file and imagem_file.filename:
            filename = secure_filename(imagem_file.filename)
            upload_path = os.path.join("app/static/img/produtos", filename)
            imagem_file.save(upload_path)
            imagem_path = f"img/produtos/{filename}"

        produto = Produto(
            nome=nome,
            slug=gerar_slug(nome),
            preco=preco,
            preco_antigo=float(preco_antigo) if preco_antigo else None,
            desconto=int(desconto) if desconto else None,
            categoria=categoria,
            descricao=descricao,
            imagem=imagem_path,
            stock=stock,
            promocao=promocao,
            destaque=destaque,
            ativo=ativo
        )

        db.session.add(produto)
        db.session.commit()

        flash("Produto criado com sucesso.", "success")
        return redirect(url_for("admin.produtos"))

    return render_template("admin/produto_form.html", produto=None)


@admin.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_produto(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    produto = Produto.query.get_or_404(id)

    if request.method == "POST":
        produto.nome = request.form.get("nome")
        produto.slug = gerar_slug(produto.nome)
        produto.preco = float(request.form.get("preco"))
        produto.preco_antigo = float(request.form.get("preco_antigo")) if request.form.get("preco_antigo") else None
        produto.desconto = int(request.form.get("desconto")) if request.form.get("desconto") else None
        produto.categoria = request.form.get("categoria")
        produto.descricao = request.form.get("descricao")
        produto.stock = int(request.form.get("stock") or 0)

        produto.promocao = request.form.get("promocao") == "on"
        produto.destaque = request.form.get("destaque") == "on"
        produto.ativo = request.form.get("ativo") == "on"

        imagem_file = request.files.get("imagem")

        if imagem_file and imagem_file.filename:
            filename = secure_filename(imagem_file.filename)
            upload_path = os.path.join("app/static/img/produtos", filename)
            imagem_file.save(upload_path)
            produto.imagem = f"img/produtos/{filename}"

        db.session.commit()

        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("admin.produtos"))

    return render_template("admin/produto_form.html", produto=produto)


@admin.route("/produtos/apagar/<int:id>", methods=["POST"])
@login_required
def apagar_produto(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()

    flash("Produto apagado com sucesso.", "success")
    return redirect(url_for("admin.produtos"))