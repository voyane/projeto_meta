"""Adicionar comprovativo ao pedido

Revision ID: b6a4d2e91c0f
Revises: 9f2c1a7b6d3e
Create Date: 2026-07-15 14:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "b6a4d2e91c0f"
down_revision = "9f2c1a7b6d3e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("pedidos", schema=None) as batch_op:
        batch_op.add_column(sa.Column("comprovativo", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("comprovativo_enviado_em", sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table("pedidos", schema=None) as batch_op:
        batch_op.drop_column("comprovativo_enviado_em")
        batch_op.drop_column("comprovativo")
