"""add metadata fields to Message

Revision ID: bce67f0c9bd7
Revises: ae21d50cbaa0
Create Date: 2026-06-03 12:50:10.670875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "bce67f0c9bd7"
down_revision: Union[str, Sequence[str], None] = "ae21d50cbaa0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


llm_route_enum = postgresql.ENUM(
    "DIRECT",
    "RAG",
    "CLARIFY",
    "TOOL",
    name="llm_route",
    create_type=False
)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    # PostgreSQL enum types must exist before a column can use them.
    llm_route_enum.create(bind, checkfirst=True)

    op.add_column("messages", sa.Column("model", sa.String(length=255), nullable=True))
    op.add_column("messages", sa.Column("route", llm_route_enum, nullable=True))
    op.add_column("messages", sa.Column("finish_reason", sa.String(length=100), nullable=True))
    op.add_column("messages", sa.Column("prompt_tokens", sa.Integer(), nullable=True))
    op.add_column("messages", sa.Column("completion_tokens", sa.Integer(), nullable=True))
    op.add_column("messages", sa.Column("total_tokens", sa.Integer(), nullable=True))
    op.add_column("messages", sa.Column("retrieval_embedding_model", sa.String(length=255), nullable=True))
    op.add_column("messages", sa.Column("retrieval_reranking_model", sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    op.drop_column("messages", "retrieval_reranking_model")
    op.drop_column("messages", "retrieval_embedding_model")
    op.drop_column("messages", "total_tokens")
    op.drop_column("messages", "completion_tokens")
    op.drop_column("messages", "prompt_tokens")
    op.drop_column("messages", "finish_reason")
    op.drop_column("messages", "route")
    op.drop_column("messages", "model")

    # Drop the enum type after no columns depend on it.
    llm_route_enum.drop(bind, checkfirst=True)
