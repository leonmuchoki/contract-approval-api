"""empty message

Revision ID: 25965ad35599
Revises: ce4820ff6b02
Create Date: 2021-08-17 07:52:45.289190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25965ad35599'
down_revision = 'ce4820ff6b02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contract_stages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contract_stage', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['modified_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('contracts', sa.Column('contract_stage_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contracts', 'contract_stages', ['contract_stage_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contracts', type_='foreignkey')
    op.drop_column('contracts', 'contract_stage_id')
    op.drop_table('contract_stages')
    # ### end Alembic commands ###
