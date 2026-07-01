from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Produto, Cart, CartItem, Rating
from app.extensions import db, mail
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func
from urllib.parse import urlparse, urljoin
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from twilio.rest import Client
from app.services.whatsapp_service import enviar_whatsapp
import random
from datetime import datetime, timedelta


main = Blueprint("main", __name__)
cart_bp = Blueprint("cart", __name__)

#==================Login=========================
def is_safe_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

@main.route("/login", methods=["GET", "POST"])
def login():

    # se já estiver logado
    if current_user.is_authenticated:
        next_page = request.args.get("next")
        if not next_page or not is_safe_url(next_page):
            next_page = url_for("main.index")
        return redirect(next_page)

    # GET
    next_page = request.args.get("next")
    if not next_page or not is_safe_url(next_page):
        next_page = url_for("main.index")

    # POST
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash("Login realizado com sucesso!", "success")

            next_page_post = request.form.get("next")

            if not next_page_post or not is_safe_url(next_page_post):
                next_page_post = url_for("main.index")

            return redirect(next_page_post)

        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template("login.html", next=next_page)

# ==================== REGISTRO ====================
@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        name = request.form.get("name")
        phone = request.form.get("phone")

        # Verifica se o usuário já existe
        if User.query.filter_by(email=email).first():
            flash("Email já cadastrado!", "danger")
            return redirect(url_for("main.register"))

        # Cria novo usuário
        novo_user = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password)
        )
        db.session.add(novo_user)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")

# ================= ESQUECEU SENHA =================
@main.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        country_code = request.form.get("country_code", "+258")
        phone = request.form.get("phone", "").strip()
        phone = phone.replace(" ", "").replace("-", "")

        user = User.query.filter_by(phone=phone).first()

        if user:
            code = str(random.randint(100000, 999999))

            user.reset_code = code
            user.reset_code_expires = datetime.utcnow() + timedelta(minutes=10)

            db.session.commit()

            destino = f"{country_code}{phone}"

            whatsapp_enviado = enviar_whatsapp(destino, code)

            if whatsapp_enviado:
                flash("Código enviado pelo WhatsApp.", "success")
            else:
                flash("Não foi possível enviar pelo WhatsApp agora. Use o código mostrado no terminal.", "warning")

            return redirect(url_for("main.verify_code", phone=phone))

        flash("Se o telefone existir, enviaremos um código.", "success")

    return render_template("forgot_password.html")

#==================VERIFICAR CÓDIGO=========================
@main.route("/verify-code", methods=["GET", "POST"])
def verify_code():
    phone = request.args.get("phone")

    if not phone:
        flash("Telefone inválido.", "danger")
        return redirect(url_for("main.forgot_password"))

    user = User.query.filter_by(phone=phone).first()
    phone = phone.replace(" ", "").replace("-", "")

    if not user:
        flash("Utilizador não encontrado.", "danger")
        return redirect(url_for("main.forgot_password"))

    if request.method == "POST":
        code = request.form.get("code", "").strip()

        if not user.reset_code or not user.reset_code_expires:
            flash("Código inválido. Solicite um novo.", "danger")
            return redirect(url_for("main.forgot_password"))

        if datetime.utcnow() > user.reset_code_expires:
            flash("Código expirado. Solicite outro.", "danger")
            return redirect(url_for("main.forgot_password"))

        if code != user.reset_code:
            flash("Código incorreto.", "danger")
            return redirect(url_for("main.verify_code", phone=phone))

        return redirect(url_for("main.reset_password", phone=phone))

    return render_template("verify_code.html", phone=phone)

#==================RESETAR SENHA=========================
@main.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    phone = request.args.get("phone")

    if not phone:
        flash("Telefone inválido.", "danger")
        return redirect(url_for("main.forgot_password"))

    user = User.query.filter_by(phone=phone).first()

    if not user:
        flash("Utilizador não encontrado.", "danger")
        return redirect(url_for("main.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not password or not confirm_password:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("main.reset_password", phone=phone))

        if password != confirm_password:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for("main.reset_password", phone=phone))

        user.set_password(password)

        user.reset_code = None
        user.reset_code_expires = None

        db.session.commit()

        flash("Senha alterada com sucesso. Faça login.", "success")
        return redirect(url_for("main.login"))

    return render_template("reset_password.html", phone=phone)

#=======================Logout========================
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

#========================Home==========================
@main.route("/")
def index():
    produtos = Produto.query.all()
    return render_template("index.html", produtos=produtos)

#==================Páginas de Produtos=====================
@main.route("/categoria/<categoria>")
def categoria(categoria):
    produtos = Produto.query.filter_by(categoria=categoria).all()

    if not produtos:
        flash("Nenhum produto encontrado!", "warning")

    #=====Calcula a média de rating para cada produto====
    for produto in produtos:
        media = db.session.query(func.avg(Rating.valor)) \
            .filter(Rating.produto_id == produto.id) \
            .scalar()
        produto.media_rating = round(media or 0, 1)

    return render_template("categoria.html", produtos=produtos, categoria=categoria)

#==================Detalhe do Produto=====================
@main.route("/produto/<slug>")
def produto_detalhe(slug):
    #=====Busca o produto pelo slug=====
    produto = Produto.query.filter_by(slug=slug).first()
    if not produto:
        abort(404)  # se não existir, retorna 404

    #====Calcula a média do rating do produto======
    media = db.session.query(func.avg(Rating.valor)) \
        .filter(Rating.produto_id == produto.id) \
        .scalar() or 0

    produto.media_rating = round(media or 0, 1)  # arredonda para 1 casa decimal

    return render_template("produto_detalhe.html", produto=produto)

#======================API Produtos=============================
@main.route("/api/produtos")
def list_produto():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])

#===================Ratings====================================
@main.route("/api/rating", methods=["POST"])
@login_required
def salvar_rating():
    data = request.get_json()
    produto_id = data.get("produto_id")
    valor = data.get("valor")

    rating = Rating.query.filter_by(user_id=current_user.id, produto_id=produto_id
    ).first()

    if rating:
        rating.valor = valor
    else:
        rating = Rating(valor=valor, user_id=current_user.id, produto_id=produto_id)
        db.session.add(rating)

    db.session.commit()

    # calcular nova média
    media = db.session.query(func.avg(Rating.valor))\
        .filter(Rating.produto_id == produto_id)\
        .scalar()

    return jsonify({
        "success": True,
        "media": round(media, 1)
    })

#====================VIEW CART ===============================
@cart_bp.route("/cart")
@login_required
def view_cart():
    cart = get_or_create_cart(current_user)
    total = sum(item.quantidade * item.produto.preco for item in cart.items)

    return render_template("cart.html", cart=cart, total=total)

#=====================ADICIONAR CART (API)================================
@cart_bp.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    if not current_user.is_authenticated:
        return jsonify({"login_required": True})

    data = request.get_json()
    slug = data.get("slug")

    produto = Produto.query.filter_by(slug=slug).first()

    if not produto:
        return jsonify({"success": False})

    cart = get_or_create_cart(current_user)

    # verificar se já existe
    item = CartItem.query.filter_by(cart_id=cart.id, produto_id=produto.id).first()

    if item:
        item.quantidade += 1
    else:
        item = CartItem(cart_id=cart.id, produto_id=produto.id, quantidade=1)
        db.session.add(item)

    db.session.commit()
    return jsonify({"success": True})

#=====================ATUALIZAR QUANTIDADE============================
@cart_bp.route("/api/cart/update", methods=["POST"])
@login_required
def update_cart():
    data = request.get_json()
    item_id = data.get("item_id")
    action = data.get("action")

    # pegar item do usuário atual
    item = CartItem.query.join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if not item:
        return jsonify({"success": False})

    if action == "increase":
        item.quantidade += 1

    elif action == "decrease":
        item.quantidade -= 1
        if item.quantidade <= 0:
            db.session.delete(item)

    db.session.commit()
    return jsonify({"success": True})

#===================== REMOVER ============================
@cart_bp.route("/api/cart/remove", methods=["POST"])
@login_required
def remove_item():
    data = request.get_json()
    item_id = data.get("item_id")

    item = CartItem.query.join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()

    return jsonify({"success": True})

#==================CART COUNT=========================
@cart_bp.route("/api/cart/count")
def cart_count():
    if not current_user.is_authenticated:
        return jsonify({"count": 0})

    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if not cart:
        return jsonify({"count": 0})

    total = sum(item.quantidade for item in cart.items)

    return jsonify({"count": total})

#===================FUNÇÃO AUXILIAR=======================
def get_or_create_cart(user):
    cart = Cart.query.filter_by(user_id=user.id).first()

    if not cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

    return cart

