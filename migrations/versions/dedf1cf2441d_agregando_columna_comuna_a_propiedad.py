"""Agregando columna comuna a Propiedad

Revision ID: dedf1cf2441d
Revises: 8ece7fb0cac0
Create Date: 2025-02-03 23:42:34.971697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dedf1cf2441d'
down_revision = '8ece7fb0cac0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propiedades', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comuna', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propiedades', schema=None) as batch_op:
        batch_op.drop_column('comuna')

    # ### end Alembic commands ###
