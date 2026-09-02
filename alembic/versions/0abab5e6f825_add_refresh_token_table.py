"""add refresh token table

Revision ID: 0abab5e6f825
Revises: fc158a72e6d0
Create Date: 2026-06-11 10:44:25.802273
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0abab5e6f825"
down_revision: Union[str, Sequence[str], None] = "fc158a72e6d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "token_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "token_hash",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "user_fk",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["user_fk"],
            ["users.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_refresh_tokens_id"),
        "refresh_tokens",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_refresh_tokens_token_id"),
        "refresh_tokens",
        ["token_id"],
        unique=True,
    )

    op.create_index(
        op.f("ix_refresh_tokens_token_hash"),
        "refresh_tokens",
        ["token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_refresh_tokens_token_hash"),
        table_name="refresh_tokens",
    )

    op.drop_index(
        op.f("ix_refresh_tokens_token_id"),
        table_name="refresh_tokens",
    )

    op.drop_index(
        op.f("ix_refresh_tokens_id"),
        table_name="refresh_tokens",
    )

    op.drop_table("refresh_tokens")
