from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

def utcnow(): return datetime.now(timezone.utc)

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_name: Mapped[str] = mapped_column(String(255))
    precision_at_k: Mapped[float] = mapped_column(Float, default=0)
    recall_at_k: Mapped[float] = mapped_column(Float, default=0)
    hit_rate: Mapped[float] = mapped_column(Float, default=0)
    mrr: Mapped[float] = mapped_column(Float, default=0)
    citation_accuracy: Mapped[float] = mapped_column(Float, default=0)
    unsupported_claim_rate: Mapped[float] = mapped_column(Float, default=0)
    average_latency_ms: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
