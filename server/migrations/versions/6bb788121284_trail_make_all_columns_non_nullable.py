"""Trail: make all columns non nullable

Revision ID: 6bb788121284
Revises: 59bbc3c4193c
Create Date: 2025-01-04 16:14:08.133371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb788121284'
down_revision = '59bbc3c4193c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trails', schema=None) as batch_op:
        batch_op.alter_column('length',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trails', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('length',
               existing_type=sa.FLOAT(),
               nullable=True)

    # ### end Alembic commands ###