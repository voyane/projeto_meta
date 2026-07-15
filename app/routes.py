from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Produto, Cart, CartItem, Rating, Pedido, PedidoItem
from app.extensions import db, mail
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func
from urllib.parse import quote, urlparse, urljoin
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from twilio.rest import Client
from app.services.whatsapp_service import enviar_whatsapp
import random
import os
import uuid
from datetime import datetime, timedelta


main = Blueprint("main", __name__)
cart_bp = Blueprint("cart", __name__)
ALLOWED_PROOF_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "pdf"}


def allowed_proof_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_PROOF_EXTENSIONS
    )

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
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()

        if not email or not password or not name or not phone:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("main.register"))

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
    phone = request.args.get("phone", "").strip()
    phone = phone.replace(" ", "").replace("-", "")

    if not phone:
        flash("Telefone inválido.", "danger")
        return redirect(url_for("main.forgot_password"))

    user = User.query.filter_by(phone=phone).first()

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
    phone = request.args.get("phone", "").strip()
    phone = phone.replace(" ", "").replace("-", "")

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
    produtos = Produto.query.filter_by(ativo=True).all()
    return render_template("index.html", produtos=produtos)

#========================Perfil==========================
@main.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", user=current_user)

#==================Páginas de Produtos=====================
@main.route("/categoria/<categoria>")
def categoria(categoria):
    produtos = Produto.query.filter_by(
        categoria=categoria,
        ativo=True
    ).all()

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
    produto = Produto.query.filter_by(
        slug=slug,
        ativo=True
    ).first()
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
    produtos = Produto.query.filter_by(ativo=True).all()
    return jsonify([p.to_dict() for p in produtos])

#===================Ratings====================================
@main.route("/api/rating", methods=["POST"])
@login_required
def salvar_rating():
    data = request.get_json(silent=True) or {}

    try:
        produto_id = int(data.get("produto_id"))
        valor = int(data.get("valor"))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Dados inválidos."}), 400

    if valor < 1 or valor > 5:
        return jsonify({"success": False, "message": "Avaliação inválida."}), 400

    if not db.session.get(Produto, produto_id):
        return jsonify({"success": False, "message": "Produto não encontrado."}), 404

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

    data = request.get_json(silent=True) or {}
    slug = data.get("slug")

    if not slug:
        return jsonify({"success": False, "message": "Produto inválido."}), 400

    produto = Produto.query.filter_by(slug=slug).first()

    if not produto:
        return jsonify({"success": False, "message": "Produto não encontrado."}), 404

    if not produto.ativo:
        return jsonify({"success": False, "message": "Produto indisponível."}), 400

    if (produto.stock or 0) <= 0:
        return jsonify({"success": False, "message": "Produto sem stock."}), 400

    cart = get_or_create_cart(current_user)

    # verificar se já existe
    item = CartItem.query.filter_by(cart_id=cart.id, produto_id=produto.id).first()

    if item:
        if item.quantidade + 1 > (produto.stock or 0):
            return jsonify({
                "success": False,
                "message": "Quantidade solicitada excede o stock disponível."
            }), 400

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
    data = request.get_json(silent=True) or {}
    item_id = data.get("item_id")
    action = data.get("action")

    if action not in ("increase", "decrease"):
        return jsonify({"success": False, "message": "Ação inválida."}), 400

    # pegar item do usuário atual
    item = CartItem.query.join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if not item:
        return jsonify({"success": False})

    if action == "increase":
        if item.quantidade + 1 > (item.produto.stock or 0):
            return jsonify({
                "success": False,
                "message": "Quantidade solicitada excede o stock disponível."
            }), 400

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
    data = request.get_json(silent=True) or {}
    item_id = data.get("item_id")

    item = CartItem.query.join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()

    return jsonify({"success": True})

#===================== FINALIZAR PEDIDO ============================
@cart_bp.route("/api/cart/checkout", methods=["POST"])
@login_required
def checkout_cart():
    data = request.get_json(silent=True) or {}
    payment_method = data.get("payment_method", "mpesa")
    payment_options = {
        "mpesa": {
            "label": "M-Pesa",
            "manual": True,
            "number": current_app.config.get("MPESA_NUMBER", "845421616"),
            "instructions": (
                "Faça o pagamento por M-Pesa para o número abaixo."
            )
        },
        "emola": {
            "label": "e-Mola",
            "manual": True,
            "number": current_app.config.get("EMOLA_NUMBER", "875421616"),
            "instructions": (
                "Faça o pagamento por e-Mola para o número abaixo."
            )
        },
        "whatsapp": {
            "label": "WhatsApp",
            "manual": False,
            "number": None,
            "instructions": (
                "Pagamento: A combinar por WhatsApp"
            )
        }
    }

    payment = payment_options.get(payment_method)

    if not payment:
        return jsonify({
            "success": False,
            "message": "Forma de pagamento inválida."
        }), 400

    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if not cart or not cart.items:
        return jsonify({
            "success": False,
            "message": "O carrinho está vazio."
        }), 400

    for item in cart.items:
        if not item.produto or not item.produto.ativo:
            return jsonify({
                "success": False,
                "message": f"{item.produto.nome if item.produto else item.produto_id} está indisponível."
            }), 400

        if item.quantidade > (item.produto.stock or 0):
            return jsonify({
                "success": False,
                "message": (
                    f"{item.produto.nome} tem apenas "
                    f"{item.produto.stock or 0} em stock."
                )
            }), 400

    linhas = [
        "Olá, quero finalizar este pedido:",
        "",
        f"Cliente: {current_user.name or current_user.email}",
        f"Telefone: {current_user.phone}",
        f"Forma de pagamento: {payment['label']}",
        "",
        "Produtos:"
    ]

    total = 0
    pedido = Pedido(
        user_id=current_user.id,
        payment_method=payment_method,
        payment_label=payment["label"],
        status="aguardando_comprovativo" if payment["manual"] else "em_contacto",
        total=0
    )
    db.session.add(pedido)

    for item in cart.items:
        subtotal = item.quantidade * item.produto.preco
        total += subtotal
        pedido.items.append(PedidoItem(
            produto_id=item.produto.id,
            produto_nome=item.produto.nome,
            produto_imagem=item.produto.imagem,
            produto_slug=item.produto.slug,
            preco_unitario=item.produto.preco,
            quantidade=item.quantidade,
            subtotal=subtotal
        ))
        linhas.append(
            f"- {item.produto.nome} | Qtd: {item.quantidade} | "
            f"{subtotal:.2f} MT"
        )

    pedido.total = total

    linhas.extend([
        "",
        f"Total: {total:.2f} MT",
        "",
        payment["instructions"]
    ])

    numero = current_app.config.get("STORE_WHATSAPP_NUMBER", "258845421616")
    numero = "".join(caractere for caractere in numero if caractere.isdigit())
    mensagem = quote("\n".join(linhas))

    if payment["manual"]:
        db.session.delete(cart)
        db.session.commit()

        comprovativo = quote(
            "\n".join([
                "Olá, já fiz o pagamento e quero enviar o comprovativo.",
                "",
                f"Pedido: #{pedido.id}",
                f"Cliente: {current_user.name or current_user.email}",
                f"Telefone: {current_user.phone}",
                f"Forma de pagamento: {payment['label']}",
                f"Total: {total:.2f} MT"
            ])
        )

        return jsonify({
            "success": True,
            "manual_payment": True,
            "pedido_id": pedido.id,
            "payment_label": payment["label"],
            "payment_number": payment["number"],
            "total": f"{total:.2f} MT",
            "instructions": payment["instructions"],
            "proof_whatsapp_url": f"https://wa.me/{numero}?text={comprovativo}"
        })

    db.session.delete(cart)
    db.session.commit()

    linhas[1:1] = [f"Pedido: #{pedido.id}"]
    mensagem = quote("\n".join(linhas))

    return jsonify({
        "success": True,
        "pedido_id": pedido.id,
        "whatsapp_url": f"https://wa.me/{numero}?text={mensagem}"
    })

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

#==================MEUS PEDIDOS=========================
@main.route("/meus-pedidos")
@login_required
def meus_pedidos():

    pedidos = Pedido.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Pedido.created_at.desc()
    ).all()

    return render_template(
        "meus_pedidos.html",
        pedidos=pedidos
    )

#==================ENVIAR COMPROVATIVO=========================
@main.route("/meus-pedidos/<int:id>/comprovativo", methods=["POST"])
@login_required
def enviar_comprovativo(id):
    pedido = Pedido.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if pedido.status not in ("aguardando_comprovativo", "comprovativo_enviado"):
        flash("Este pedido não aceita comprovativo neste estado.", "warning")
        return redirect(url_for("main.meus_pedidos"))

    comprovativo = request.files.get("comprovativo")

    if not comprovativo or not comprovativo.filename:
        flash("Selecione o ficheiro do comprovativo.", "danger")
        return redirect(url_for("main.meus_pedidos"))

    if not allowed_proof_file(comprovativo.filename):
        flash("Formato inválido. Use PNG, JPG, WEBP ou PDF.", "danger")
        return redirect(url_for("main.meus_pedidos"))

    filename = secure_filename(comprovativo.filename)
    extensao = filename.rsplit(".", 1)[1].lower()
    novo_nome = f"pedido-{pedido.id}-{uuid.uuid4().hex}.{extensao}"
    pasta = os.path.join("app", "static", "uploads", "comprovativos")
    os.makedirs(pasta, exist_ok=True)

    comprovativo.save(os.path.join(pasta, novo_nome))

    pedido.comprovativo = f"uploads/comprovativos/{novo_nome}"
    pedido.comprovativo_enviado_em = datetime.utcnow()
    pedido.status = "comprovativo_enviado"
    db.session.commit()

    flash("Comprovativo enviado com sucesso. Aguarde confirmação.", "success")
    return redirect(url_for("main.meus_pedidos"))
