"""Initial migration

Revision ID: 4671234fe748
Revises: 
Create Date: 2025-05-12 14:06:05.076646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4671234fe748'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('subject')
    )
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tieude', sa.String(length=255), nullable=False),
    sa.Column('noidung', sa.Text(), nullable=True),
    sa.Column('hinhanh', sa.String(length=255), nullable=True),
    sa.Column('linkgoc', sa.String(length=255), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('linkgoc')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    op.drop_table('category')
    # ### end Alembic commands ###
