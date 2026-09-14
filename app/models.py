from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

def utcnow():
    return datetime.now(timezone.utc)

class OpportunityRecord(Base):
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(80), index=True)
    external_id: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(Text, default="")
    expected_revenue_usd: Mapped[float] = mapped_column(Float, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0)
    automation_score: Mapped[int] = mapped_column(Integer, default=0)
    payment_probability: Mapped[float] = mapped_column(Float, default=0)
    success_probability: Mapped[float] = mapped_column(Float, default=0)
    category: Mapped[str] = mapped_column(String(80), default="", index=True)
    provider: Mapped[str] = mapped_column(String(200), default="", index=True)
    network: Mapped[str] = mapped_column(String(100), default="", index=True)
    asset: Mapped[str] = mapped_column(String(100), default="")
    price_atomic: Mapped[str] = mapped_column(String(100), default="")
    pay_to: Mapped[str] = mapped_column(String(200), default="")
    decision: Mapped[str] = mapped_column(String(20), default="review")
    status: Mapped[str] = mapped_column(String(30), default="discovered", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class ActivityEvent(Base):
    __tablename__ = "activity_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(40), index=True)
    worker: Mapped[str] = mapped_column(String(40), index=True)
    message: Mapped[str] = mapped_column(Text)
    opportunity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount_usd: Mapped[float] = mapped_column(Float, default=0)
    is_error: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    recovered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

class LedgerEntry(Base):
    __tablename__ = "ledger"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(30), index=True)
    amount_usd: Mapped[float] = mapped_column(Float)
    asset: Mapped[str] = mapped_column(String(20), default="USD")
    tx_ref: Mapped[str] = mapped_column(String(200), default="")
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
