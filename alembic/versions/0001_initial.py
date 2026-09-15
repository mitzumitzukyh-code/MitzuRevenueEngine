"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-15
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("opportunities", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source", sa.String(80), nullable=False), sa.Column("external_id", sa.String(200), nullable=False), sa.Column("title", sa.String(500), nullable=False), sa.Column("url", sa.Text(), nullable=False), sa.Column("expected_revenue_usd", sa.Float(), nullable=False), sa.Column("estimated_cost_usd", sa.Float(), nullable=False), sa.Column("automation_score", sa.Integer(), nullable=False), sa.Column("payment_probability", sa.Float(), nullable=False), sa.Column("success_probability", sa.Float(), nullable=False), sa.Column("category", sa.String(80), nullable=False), sa.Column("provider", sa.String(200), nullable=False), sa.Column("network", sa.String(100), nullable=False), sa.Column("asset", sa.String(100), nullable=False), sa.Column("price_atomic", sa.String(100), nullable=False), sa.Column("pay_to", sa.String(200), nullable=False), sa.Column("calls_30d", sa.Integer(), nullable=False), sa.Column("unique_payers_30d", sa.Integer(), nullable=False), sa.Column("estimated_volume_30d_usd", sa.Float(), nullable=False), sa.Column("decision", sa.String(20), nullable=False), sa.Column("status", sa.String(30), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("external_id"))
    for col in ("source","external_id","category","provider","network","status"): op.create_index(f"ix_opportunities_{col}", "opportunities", [col])
    op.create_table("activity_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("kind", sa.String(40), nullable=False), sa.Column("worker", sa.String(40), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("opportunity_id", sa.Integer(), nullable=True), sa.Column("amount_usd", sa.Float(), nullable=False), sa.Column("is_error", sa.Boolean(), nullable=False), sa.Column("recovered", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for col in ("kind","worker","is_error","created_at"): op.create_index(f"ix_activity_events_{col}", "activity_events", [col])
    op.create_table("ledger", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("category", sa.String(30), nullable=False), sa.Column("amount_usd", sa.Float(), nullable=False), sa.Column("asset", sa.String(20), nullable=False), sa.Column("tx_ref", sa.String(200), nullable=False), sa.Column("verified", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for col in ("category","created_at"): op.create_index(f"ix_ledger_{col}", "ledger", [col])
    op.create_table("market_metrics", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("source", sa.String(80), nullable=False), sa.Column("category", sa.String(80), nullable=False), sa.Column("buyers_30d", sa.Integer(), nullable=False), sa.Column("transactions_30d", sa.Integer(), nullable=False), sa.Column("volume_30d_usd", sa.Float(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for col in ("source","category","created_at"): op.create_index(f"ix_market_metrics_{col}", "market_metrics", [col])

def downgrade():
    op.drop_table("market_metrics"); op.drop_table("ledger"); op.drop_table("activity_events"); op.drop_table("opportunities")
