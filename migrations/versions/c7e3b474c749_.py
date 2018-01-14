"""empty message

Revision ID: c7e3b474c749
Revises: 536562bed58a
Create Date: 2018-01-13 15:29:42.243171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7e3b474c749'
down_revision = '536562bed58a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email_confirmed', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('email_confirmed_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email_confirmed_at')
    op.drop_column('users', 'email_confirmed')
    # ### end Alembic commands ###
