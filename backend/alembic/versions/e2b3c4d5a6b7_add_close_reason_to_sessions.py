"""add_close_reason_to_sessions

Revision ID: e2b3c4d5a6b7
Revises: fc29a7f754f8
Create Date: 2026-06-08 12:00:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "e2b3c4d5a6b7"
down_revision: Union[str, None] = "fc29a7f754f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sessions",
        sa.Column(
            "close_reason",
            sa.Enum("manual", "timeout", "ble_disconnect", name="closereason"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("sessions", "close_reason")
    op.execute("DROP TYPE IF EXISTS closereason")
