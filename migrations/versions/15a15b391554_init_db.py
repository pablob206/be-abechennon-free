"""init db

Revision ID: 15a15b391554
Revises: 
Create Date: 2023-05-18 18:11:13.021897

"""
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "15a15b391554"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "binancesettings",
        sa.Column("pairs_list", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("binance_api_key", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "binance_api_secret", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("order_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("max_open_position", sa.Integer(), nullable=True),
        sa.Column("max_open_position_per_coin", sa.Integer(), nullable=True),
        sa.Column("currency_base", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("amount_per_order", sa.Float(), nullable=True),
        sa.Column("take_profit_at", sa.Float(), nullable=True),
        sa.Column("enable_stop_loss", sa.Boolean(), nullable=True),
        sa.Column("stop_loss", sa.Integer(), nullable=True),
        sa.Column("enable_trailing_stop_loss", sa.Boolean(), nullable=True),
        sa.Column("trailing_stop_loss", sa.Integer(), nullable=True),
        sa.Column("time_frame", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_real_time", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("close_all_position", sa.Boolean(), nullable=True),
        sa.Column("flag_back_testing", sa.Boolean(), nullable=True),
        sa.Column("invert_signal", sa.Boolean(), nullable=True),
        sa.Column("flag_on_magic", sa.Boolean(), nullable=True),
        sa.Column("magic_amount", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("binancesettings")
    # ### end Alembic commands ###
