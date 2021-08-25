"""empty message

Revision ID: 00550daa5fc5
Revises: 84a704ad14b3
Create Date: 2021-08-24 09:02:23.302553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00550daa5fc5'
down_revision = '84a704ad14b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(length=400), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('contracts', sa.Column('contract_status_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contracts', 'contract_status', ['contract_status_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contracts', type_='foreignkey')
    op.drop_column('contracts', 'contract_status_id')
    op.drop_table('contract_status')
    # ### end Alembic commands ###
