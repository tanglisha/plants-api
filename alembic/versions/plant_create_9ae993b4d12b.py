"""plant create table

Revision ID: 9ae993b4d12b
Revises: 
Create Date: 2024-04-03 10:06:00.358832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9ae993b4d12b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plant',
    sa.Column('latin_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('min_germination_temp', sa.Integer(), nullable=True),
    sa.Column('max_germination_temp', sa.Integer(), nullable=True),
    sa.Column('min_soil_temp_transplant', sa.Integer(), nullable=True),
    sa.Column('max_soil_temp_transplant', sa.Integer(), nullable=True),
    sa.Column('pk', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_plant_latin_name'), 'plant', ['latin_name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_plant_latin_name'), table_name='plant')
    op.drop_table('plant')
    # ### end Alembic commands ###
