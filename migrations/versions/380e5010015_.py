"""Add verify match table

Revision ID: 380e5010015
Revises: 384b88178a6
Create Date: 2016-03-11 10:38:01.322679

"""

# revision identifiers, used by Alembic.
revision = '380e5010015'
down_revision = '384b88178a6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verify_match',
    sa.Column('verify_pid', sa.String(), nullable=False),
    sa.Column('borrower_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['borrower_id'], ['borrower.id'], ),
    sa.PrimaryKeyConstraint('verify_pid', 'borrower_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verify_match')
    ### end Alembic commands ###
