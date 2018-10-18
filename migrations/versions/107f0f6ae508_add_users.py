"""
Create Users table

Revision ID: 107f0f6ae508
Revises:
Create Date: 2018-10-15 21:38:44.913464

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '107f0f6ae508'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=80), nullable=False),
                    sa.Column('email', sa.String(length=80), nullable=False),
                    sa.Column('password', sa.Binary(), nullable=True),
                    sa.Column('first_name', sa.String(length=30), nullable=True),
                    sa.Column('last_name', sa.String(length=30), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=True),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
                    sa.Column('email_confirmed_at', sa.DateTime(timezone='America/Chicago'),
                              nullable=True),
                    sa.Column('locale', sa.String(length=2), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone='America/Chicago'),
                              nullable=False),
                    sa.Column('last_seen', sa.DateTime(timezone='America/Chicago'), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###