"""empty message

Revision ID: d73baf5f0211
Revises: afb6df13e233
Create Date: 2021-08-09 13:50:27.891125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd73baf5f0211'
down_revision = 'afb6df13e233'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tenders', 'modified_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tenders', 'modified_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
