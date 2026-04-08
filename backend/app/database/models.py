from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(10), index=True, nullable=False)
    bias = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    analysis_text = Column(Text, nullable=False)
    indicators_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CacheEntry(Base):
    __tablename__ = "cache_entries"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
