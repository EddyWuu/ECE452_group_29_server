"""Add test2 column to events

Revision ID: b1234b732edb
Revises: cc4ab5507ab5
Create Date: 2024-07-01 22:24:05.122275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1234b732edb'
down_revision = 'cc4ab5507ab5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test2', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('test2')

    # ### end Alembic commands ###
