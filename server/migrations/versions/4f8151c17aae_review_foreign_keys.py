"""Review foreign keys

Revision ID: 4f8151c17aae
Revises: 61425eea10ae
Create Date: 2024-11-26 20:06:47.445325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f8151c17aae'
down_revision = '61425eea10ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_reviews_trail_id_trails'), 'trails', ['trail_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_reviews_user_id_users'), 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_reviews_user_id_users'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_reviews_trail_id_trails'), type_='foreignkey')

    # ### end Alembic commands ###