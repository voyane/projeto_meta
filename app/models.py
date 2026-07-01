from .extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


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

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)

    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)

    quantidade = db.Column(db.Integer, default=1)

    # relacionamento com Produto
    produto = db.relationship("Produto")

    # 🚨 MUITO IMPORTANTE (evita duplicados)
    __table_args__ = (
        db.UniqueConstraint("cart_id", "produto_id", name="unique_cart_item"),
    )