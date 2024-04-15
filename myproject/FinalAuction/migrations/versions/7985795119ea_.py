"""empty message

Revision ID: 7985795119ea
Revises: abfa2082f09f
Create Date: 2023-05-06 16:59:41.432201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7985795119ea'
down_revision = 'abfa2082f09f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('itemImageURL', sa.String(length=64), nullable=True),
    sa.Column('Bid', sa.Float(), nullable=True),
    sa.Column('highestBidder', sa.Integer(), nullable=True),
    sa.Column('endTime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('lastname', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('phoneNum', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('contactInfo', sa.String(length=128), nullable=True))
        batch_op.drop_index('ix_users_username')
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=64), nullable=True))
        batch_op.create_index('ix_users_username', ['username'], unique=False)
        batch_op.drop_column('contactInfo')
        batch_op.drop_column('phoneNum')
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')

    op.drop_table('item')
    # ### end Alembic commands ###