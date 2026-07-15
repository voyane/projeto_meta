from .extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#==================USERS========================
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)
    
    reset_code = db.Column(db.String(6), nullable=True)
    reset_code_expires = db.Column(db.DateTime, nullable=True)

    # criar senha
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # verificar senha
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#=====================Produtos===================================
class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    ratings = db.relationship('Rating', backref='produto', lazy=True)

    preco_antigo = db.Column(db.Float, nullable=True)
    desconto = db.Column(db.Integer, nullable=True)
    promocao = db.Column(db.Boolean, default=False)
    destaque = db.Column(db.Boolean, default=False)
    ativo = db.Column(db.Boolean, default=True)

    stock = db.Column(db.Integer, default=0)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "nome": self.nome,
            "preco": self.preco,
            "imagem": self.imagem,
            "categoria": self.categoria,
            "descricao": self.descricao
        }
    
    def __repr__(self):
        return f"<Produto {self.nome}>"
    
    def media_rating(self):
        if not self.ratings:
            return 0
        return round(sum(r.valor for r in self.ratings) / len(self.ratings), 1)

    def total_avaliacoes(self):
        return len(self.ratings)
    
    def promocao_ativa(self):
        agora = datetime.utcnow()

        for promocao in self.promocoes:
            if not promocao.ativo:
                continue

            if promocao.data_inicio and promocao.data_inicio > agora:
                continue

            if promocao.data_fim and promocao.data_fim < agora:
                continue

            return promocao

        return None

    def preco_promocional(self):
        promocao = self.promocao_ativa()

        if not promocao:
            return self.preco

        desconto = promocao.desconto / 100
        return round(self.preco * (1 - desconto), 2)

    def valor_poupado(self):
        promocao = self.promocao_ativa()

        if not promocao:
            return 0

        return round(self.preco - self.preco_promocional(), 2)
    
#================Ratting========================
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'))
    
    # impede votar duas vezes
    __table_args__ = (
        db.UniqueConstraint('user_id', 'produto_id', name='unique_user_rating'),
    )

from datetime import datetime

# ================= CART =================
class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relacionamento com User
    user = db.relationship("User", backref="cart", uselist=False)

    # itens do carrinho
    items = db.relationship("CartItem", backref="cart", cascade="all, delete-orphan"
    )

# ================= CART ITEM =================
class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True )

    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    quantidade = db.Column(db.Integer, nullable=False, default=1)

    produto = db.relationship(
        "Produto",
        backref=db.backref("cart_items", lazy=True)
    )

    __table_args__ = (
        db.UniqueConstraint(
            "cart_id",
            "produto_id",
            name="unique_cart_item"
        ),
        db.CheckConstraint(
            "quantidade > 0",
            name="check_cart_item_quantidade_positiva"
        )
    )

# ================= PEDIDO =================
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    payment_method = db.Column(db.String(30), nullable=False)
    payment_label = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="pendente")
    total = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("pedidos", lazy=True))
    items = db.relationship(
        "PedidoItem",
        backref="pedido",
        cascade="all, delete-orphan",
        lazy=True
    )

    def total_quantidade(self):
        return sum(item.quantidade for item in self.items)

# ================= PEDIDO ITEM =================
class PedidoItem(db.Model):
    __tablename__ = "pedido_items"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    produto_nome = db.Column(db.String(150), nullable=False)
    produto_imagem = db.Column(db.String(255), nullable=True)
    produto_slug = db.Column(db.String(100), nullable=True)
    preco_unitario = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    produto = db.relationship(
        "Produto",
        backref=db.backref("pedido_items", lazy=True)
    )

    __table_args__ = (
        db.CheckConstraint(
            "quantidade > 0",
            name="check_pedido_item_quantidade_positiva"
        ),
    )

#========================CATEGORIAS========================
class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

#========================PROMOÇÕES========================
class Promocao(db.Model):
    __tablename__ = "promocoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    descricao = db.Column(db.Text)

    # Produto que receberá a promoção
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)

    produto = db.relationship("Produto", backref=db.backref("promocoes", lazy=True))

    # Percentagem de desconto
    desconto = db.Column(db.Integer, nullable=False)

    # Texto da faixa (PROMO, BLACK FRIDAY, HALFWAY DAY...)
    selo = db.Column(db.String(50), default="PROMO")

    # Datas da promoção
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)

    data_fim = db.Column(db.DateTime)

    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

