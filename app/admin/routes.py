from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Produto, User, Cart, Rating, Categoria, Promocao
import os
import re
from sqlalchemy import or_

admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return current_user.is_authenticated and current_user.is_admin


def gerar_slug(nome):
    slug = nome.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def salvar_imagem(imagem_file):
    if not imagem_file or not imagem_file.filename:
        return None

    filename = secure_filename(imagem_file.filename)

    pasta = os.path.join("app", "static", "img", "produtos")
    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, filename)
    imagem_file.save(caminho)

    return f"img/produtos/{filename}"

#============================= DASHBOARD =========================
@admin.route("/")
@login_required
def dashboard():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    return render_template(
        "admin/dashboard.html",
        total_produtos=Produto.query.count(),
        total_users=User.query.count(),
        total_carrinhos=Cart.query.count(),
        total_avaliacoes=Rating.query.count()
    )

#============================= PRODUTOS =========================
@admin.route("/produtos")
@login_required
def produtos():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    page = request.args.get("page", 1, type=int)

    pagination = Produto.query.order_by(Produto.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    produtos = pagination.items

    return render_template(
        "admin/produtos.html",
        produtos=produtos,
        pagination=pagination
    )

#============================= NOVO PRODUTO =========================
@admin.route("/produtos/novo", methods=["GET", "POST"])
@login_required
def novo_produto():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":

        nome = request.form.get("nome")
        preco = float(request.form.get("preco"))
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

            upload_path = os.path.join("app", "static", "img", "produtos", filename)

            imagem_file.save(upload_path)

            imagem_path = f"img/produtos/{filename}"

        produto = Produto(
            nome=nome,
            slug=gerar_slug(nome),
            preco=preco,
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

#============================= EDITAR PRODUTO =========================
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

        nova_imagem = salvar_imagem(request.files.get("imagem"))

        if nova_imagem:
            produto.imagem = nova_imagem

        db.session.commit()

        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("admin.produtos"))

    return render_template("admin/produto_form.html", produto=produto)

#============================= APAGAR PRODUTO =========================
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

#============================= CATEGORIAS =========================
@admin.route("/categorias")
@login_required
def categorias():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo") == "on"

        categoria = Categoria(
            nome=nome,
            slug=gerar_slug(nome),
            descricao=descricao,
            ativo=ativo
        )

        db.session.add(categoria)
        db.session.commit()

        flash("Categoria criada com sucesso.", "success")
        return redirect(url_for("admin.categorias"))

    return render_template("admin/categoria_form.html", categoria=None)

#============================= PROMOÇÕES =========================
@admin.route("/promocoes")
@login_required
def promocoes():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    promocoes = Promocao.query.order_by(Promocao.id.desc()).all()
    return render_template("admin/promocoes.html", promocoes=promocoes)

#============================= NOVA PROMOÇÃO =========================
@admin.route("/promocoes/nova", methods=["GET", "POST"])
@login_required
def nova_promocao():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    produtos = Produto.query.order_by(Produto.nome.asc()).all()

    if request.method == "POST":
        nome = request.form.get("nome")

        promocao = Promocao(
            nome=nome,
            slug=gerar_slug(nome),
            descricao=request.form.get("descricao"),
            produto_id=int(request.form.get("produto_id")),
            desconto=int(request.form.get("desconto")),
            selo=request.form.get("selo") or "PROMO",
            ativo=request.form.get("ativo") == "on"
        )

        db.session.add(promocao)
        db.session.commit()

        flash("Promoção criada com sucesso.", "success")
        return redirect(url_for("admin.promocoes"))

    return render_template("admin/promocao_form.html", produtos=produtos)


#========================CLIENTES========================
@admin.route("/clientes")
@login_required
def clientes():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    page = request.args.get("page", 1, type=int)
    pesquisa = request.args.get("q", "").strip()

    query = User.query

    if pesquisa:
        termo = f"%{pesquisa}%"

        query = query.filter(
            or_(
                User.name.ilike(termo),
                User.email.ilike(termo),
                User.phone.ilike(termo)
            )
        )

    pagination = query.order_by(User.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    total_clientes = User.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    total_clientes_comuns = User.query.filter_by(is_admin=False).count()

    return render_template(
        "admin/clientes.html",
        clientes=pagination.items,
        pagination=pagination,
        pesquisa=pesquisa,
        total_clientes=total_clientes,
        total_admins=total_admins,
        total_clientes_comuns=total_clientes_comuns
    )

#========================CLIENTES ID========================
@admin.route("/clientes/<int:id>")
@login_required
def detalhe_cliente(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    cliente = User.query.get_or_404(id)

    return render_template(
        "admin/cliente_detalhe.html",
        cliente=cliente
    )

#====================CLIENTE DETALHE========================
@admin.route("/clientes/<int:id>/alternar-admin", methods=["POST"])
@login_required
def alternar_admin(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    cliente = User.query.get_or_404(id)

    if cliente.id == current_user.id:
        flash(
            "Não podes remover o teu próprio acesso de administrador.",
            "warning"
        )
        return redirect(url_for("admin.clientes"))

    cliente.is_admin = not cliente.is_admin

    db.session.commit()

    if cliente.is_admin:
        flash(
            f"{cliente.name or cliente.email} agora é administrador.",
            "success"
        )
    else:
        flash(
            f"{cliente.name or cliente.email} deixou de ser administrador.",
            "success"
        )

    return redirect(url_for("admin.clientes"))

#============================= PEDIDOS =========================
@admin.route("/pedidos")
@login_required
def pedidos():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    page = request.args.get("page", 1, type=int)

    pagination = Cart.query.order_by(Cart.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "admin/pedidos.html",
        pedidos=pagination.items,
        pagination=pagination
    )