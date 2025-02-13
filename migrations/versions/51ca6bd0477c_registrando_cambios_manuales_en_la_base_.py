"""Registrando cambios manuales en la base de datos

Revision ID: 51ca6bd0477c
Revises: 7f8bee995623
Create Date: 2025-02-03 22:52:03.875037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51ca6bd0477c'
down_revision = '7f8bee995623'
branch_labels = None
depends_on = None


def upgrade():
    # Asegurar que la FOREIGN KEY tenga un nombre y ON DELETE CASCADE
    with op.batch_alter_table('detalles_propiedades', schema=None) as batch_op:
        batch_op.drop_constraint('fk_detalle', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_detalle', 'propiedades', ['propiedad_id'], ['id'], ondelete='CASCADE'
        )

def downgrade():
    # Revertir los cambios en caso de rollback
    with op.batch_alter_table('detalles_propiedades', schema=None) as batch_op:
        batch_op.drop_constraint('fk_detalle', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_detalle', 'propiedades', ['propiedad_id'], ['id'], ondelete='CASCADE'
        )
