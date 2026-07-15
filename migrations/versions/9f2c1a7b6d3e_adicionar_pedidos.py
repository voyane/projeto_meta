"""Adicionar pedidos

Revision ID: 9f2c1a7b6d3e
Revises: 8c9450e40ad7
Create Date: 2026-07-15 11:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "9f2c1a7b6d3e"
down_revision = "8c9450e40ad7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("payment_method", sa.String(length=30), nullable=False),
        sa.Column("payment_label", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pedidos_user_id"), "pedidos", ["user_id"], unique=False)

    op.create_table(
        "pedido_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pedido_id", sa.Integer(), nullable=False),
        sa.Column("produto_id", sa.Integer(), nullable=True),
        sa.Column("produto_nome", sa.String(length=150), nullable=False),
        sa.Column("produto_imagem", sa.String(length=255), nullable=True),
        sa.Column("produto_slug", sa.String(length=100), nullable=True),
        sa.Column("preco_unitario", sa.Float(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.CheckConstraint("quantidade > 0", name="check_pedido_item_quantidade_positiva"),
        sa.ForeignKeyConstraint(["pedido_id"], ["pedidos.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["produto_id"], ["produtos.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pedido_items_pedido_id"), "pedido_items", ["pedido_id"], unique=False)
    op.create_index(op.f("ix_pedido_items_produto_id"), "pedido_items", ["produto_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_pedido_items_produto_id"), table_name="pedido_items")
    op.drop_index(op.f("ix_pedido_items_pedido_id"), table_name="pedido_items")
    op.drop_table("pedido_items")
    op.drop_index(op.f("ix_pedidos_user_id"), table_name="pedidos")
    op.drop_table("pedidos")
