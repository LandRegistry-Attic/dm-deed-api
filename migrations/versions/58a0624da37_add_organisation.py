# flake8: noqa
"""empty message

Revision ID: 58a0624da37
Revises: 34e2c47a334
Create Date: 2016-02-17 09:33:27.849071

"""

# revision identifiers, used by Alembic.
revision = '58a0624da37'
down_revision = '34e2c47a334'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deed', sa.Column('organisation_id', sa.String(), nullable=True))
    op.add_column('deed', sa.Column('organisation_name', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('deed', 'organisation_name')
    op.drop_column('deed', 'organisation_id')
    ### end Alembic commands ###
