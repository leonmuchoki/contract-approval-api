"""empty message

Revision ID: eda8b98c095b
Revises: d44244e4f8ad
Create Date: 2021-08-06 11:19:08.393230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eda8b98c095b'
down_revision = 'd44244e4f8ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'contract_products', 'contracts', ['contract_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contract_products', type_='foreignkey')
    # ### end Alembic commands ###
