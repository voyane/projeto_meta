from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Produto, User, Rating, Categoria, Promocao, Pedido
import os
import re
from datetime import datetime
from sqlalchemy import or_

admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return current_user.is_authenticated and current_user.is_admin


def gerar_slug(nome):
    slug = nome.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def parse_datetime_field(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M")


def datetime_local_value(value):
    if not value:
        return ""
    return value.strftime("%Y-%m-%dT%H:%M")


def atualizar_categoria_from_form(categoria):
    nome = request.form.get("nome", "").strip()

    if not nome:
        flash("Informe o nome da categoria.", "danger")
        return False

    categoria.nome = nome
    categoria.slug = gerar_slug(nome)
    categoria.descricao = request.form.get("descricao")
    categoria.ativo = request.form.get("ativo") == "on"
    return True


def atualizar_promocao_from_form(promocao):
    nome = request.form.get("nome", "").strip()
    data_inicio = parse_datetime_field(request.form.get("data_inicio"))
    data_fim = parse_datetime_field(request.form.get("data_fim"))

    if not nome:
        flash("Informe o nome da promoção.", "danger")
        return False

    if data_inicio and data_fim and data_fim <= data_inicio:
        flash("A data de fim deve ser posterior à data de início.", "danger")
        return False

    promocao.nome = nome
    promocao.slug = gerar_slug(nome)
    promocao.descricao = request.form.get("descricao")
    promocao.produto_id = int(request.form.get("produto_id"))
    promocao.desconto = int(request.form.get("desconto"))
    promocao.selo = request.form.get("selo") or "PROMO"
    promocao.data_inicio = data_inicio or datetime.utcnow()
    promocao.data_fim = data_fim
    promocao.ativo = request.form.get("ativo") == "on"
    return True


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
        total_pedidos=Pedido.query.count(),
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

    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    return render_template("admin/categorias.html", categorias=categorias)

#============================= NOVA CATEGORIA =========================
@admin.route("/categorias/nova", methods=["GET", "POST"])
@login_required
def nova_categoria():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        categoria = Categoria()

        if not atualizar_categoria_from_form(categoria):
            return redirect(url_for("admin.nova_categoria"))

        if Categoria.query.filter_by(nome=categoria.nome).first():
            flash("Categoria já existe.", "warning")
            return redirect(url_for("admin.nova_categoria"))

        db.session.add(categoria)
        db.session.commit()

        flash("Categoria criada com sucesso.", "success")
        return redirect(url_for("admin.categorias"))

    return render_template("admin/categoria_form.html", categoria=None)

#============================= EDITAR CATEGORIA =========================
@admin.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    categoria = Categoria.query.get_or_404(id)

    if request.method == "POST":
        if not atualizar_categoria_from_form(categoria):
            return redirect(url_for("admin.editar_categoria", id=id))

        categoria_existente = Categoria.query.filter(
            Categoria.id != categoria.id,
            Categoria.nome == categoria.nome
        ).first()

        if categoria_existente:
            flash("Categoria já existe.", "warning")
            return redirect(url_for("admin.editar_categoria", id=id))

        db.session.commit()

        flash("Categoria atualizada com sucesso.", "success")
        return redirect(url_for("admin.categorias"))

    return render_template("admin/categoria_form.html", categoria=categoria)

#============================= APAGAR CATEGORIA =========================
@admin.route("/categorias/apagar/<int:id>", methods=["POST"])
@login_required
def apagar_categoria(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    categoria = Categoria.query.get_or_404(id)

    produto_com_categoria = Produto.query.filter_by(categoria=categoria.slug).first()

    if produto_com_categoria:
        flash("Não é possível apagar categoria com produtos associados.", "danger")
        return redirect(url_for("admin.categorias"))

    db.session.delete(categoria)
    db.session.commit()

    flash("Categoria apagada com sucesso.", "success")
    return redirect(url_for("admin.categorias"))

#============================= PROMOÇÕES =========================
@admin.route("/promocoes")
@login_required
def promocoes():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    promocoes = Promocao.query.order_by(Promocao.id.desc()).all()
    return render_template(
        "admin/promocoes.html",
        promocoes=promocoes,
        agora=datetime.utcnow()
    )

#============================= NOVA PROMOÇÃO =========================
@admin.route("/promocoes/nova", methods=["GET", "POST"])
@login_required
def nova_promocao():
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    produtos = Produto.query.order_by(Produto.nome.asc()).all()

    if request.method == "POST":
        promocao = Promocao()

        if not atualizar_promocao_from_form(promocao):
            return redirect(url_for("admin.nova_promocao"))

        db.session.add(promocao)
        db.session.commit()

        flash("Promoção criada com sucesso.", "success")
        return redirect(url_for("admin.promocoes"))

    return render_template(
        "admin/promocao_form.html",
        promocao=None,
        produtos=produtos,
        datetime_local_value=datetime_local_value
    )

#============================= EDITAR PROMOÇÃO =========================
@admin.route("/promocoes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_promocao(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    promocao = Promocao.query.get_or_404(id)
    produtos = Produto.query.order_by(Produto.nome.asc()).all()

    if request.method == "POST":
        if not atualizar_promocao_from_form(promocao):
            return redirect(url_for("admin.editar_promocao", id=id))

        db.session.commit()

        flash("Promoção atualizada com sucesso.", "success")
        return redirect(url_for("admin.promocoes"))

    return render_template(
        "admin/promocao_form.html",
        promocao=promocao,
        produtos=produtos,
        datetime_local_value=datetime_local_value
    )

#============================= APAGAR PROMOÇÃO =========================
@admin.route("/promocoes/apagar/<int:id>", methods=["POST"])
@login_required
def apagar_promocao(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    promocao = Promocao.query.get_or_404(id)
    db.session.delete(promocao)
    db.session.commit()

    flash("Promoção apagada com sucesso.", "success")
    return redirect(url_for("admin.promocoes"))


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
    status = request.args.get("status", "").strip()
    pesquisa = request.args.get("q", "").strip()
    query = Pedido.query

    if status:
        query = query.filter(Pedido.status == status)

    if pesquisa:
        termo = f"%{pesquisa}%"
        query = query.join(User).filter(
            or_(
                User.name.ilike(termo),
                User.email.ilike(termo),
                User.phone.ilike(termo)
            )
        )

    pagination = query.order_by(Pedido.created_at.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "admin/pedidos.html",
        pedidos=pagination.items,
        pagination=pagination,
        status=status,
        pesquisa=pesquisa
    )

#============================= CONFIRMAR PAGAMENTO =========================
@admin.route("/pedidos/<int:id>/confirmar-pagamento", methods=["POST"])
@login_required
def confirmar_pagamento(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    pedido = Pedido.query.get_or_404(id)

    if pedido.status == "pago":
        flash("Este pedido já foi confirmado.", "info")
        return redirect(url_for("admin.pedidos"))

    if pedido.status in ("cancelado", "entregue"):
        flash("Este pedido já foi encerrado.", "warning")
        return redirect(url_for("admin.pedidos"))

    produtos_sem_stock = []

    for item in pedido.items:
        if not item.produto:
            produtos_sem_stock.append(f"{item.produto_nome} já não existe")
            continue

        stock_atual = item.produto.stock or 0

        if stock_atual < item.quantidade:
            produtos_sem_stock.append(
                f"{item.produto_nome} tem apenas {stock_atual} em stock"
            )

    if produtos_sem_stock:
        flash(
            "Não foi possível confirmar o pagamento: "
            + "; ".join(produtos_sem_stock),
            "danger"
        )
        return redirect(url_for("admin.pedidos"))

    for item in pedido.items:
        item.produto.stock = (item.produto.stock or 0) - item.quantidade

    pedido.status = "pago"
    db.session.commit()

    flash("Pagamento confirmado e stock atualizado.", "success")
    return redirect(url_for("admin.pedidos"))

#============================= ALTERAR ESTADO DO PEDIDO =========================
@admin.route("/pedidos/<int:id>/estado", methods=["POST"])
@login_required
def alterar_estado_pedido(id):
    if not admin_required():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    pedido = Pedido.query.get_or_404(id)
    novo_status = request.form.get("status")
    status_permitidos = {"cancelado", "entregue"}

    if novo_status not in status_permitidos:
        flash("Estado inválido.", "danger")
        return redirect(url_for("admin.pedidos"))

    if pedido.status == "pago" and novo_status == "cancelado":
        flash("Pedido pago não pode ser cancelado por esta ação.", "warning")
        return redirect(url_for("admin.pedidos"))

    if novo_status == "entregue" and pedido.status != "pago":
        flash("Apenas pedidos pagos podem ser marcados como entregues.", "warning")
        return redirect(url_for("admin.pedidos"))

    pedido.status = novo_status
    db.session.commit()

    flash("Estado do pedido atualizado.", "success")
    return redirect(url_for("admin.pedidos"))

#============================= PERFIL =========================
@admin.route("/perfil")
@login_required
def perfil():
    return redirect(url_for("main.perfil"))
