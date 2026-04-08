import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Any
from sqlalchemy.orm import Session
from app.database.models import CacheEntry
from app.config import settings


class CacheManager:
    def __init__(self, ttl: int = None):
        self.ttl = ttl or settings.cache_ttl

    def get(self, db: Session, key: str) -> Optional[Any]:
        entry = db.query(CacheEntry).filter(CacheEntry.key == key).first()
        if entry is None:
            return None
        if entry.expires_at < datetime.now(timezone.utc):
            db.delete(entry)
            db.commit()
            return None
        return json.loads(entry.value)

    def set(self, db: Session, key: str, value: Any) -> None:
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.ttl)
        entry = db.query(CacheEntry).filter(CacheEntry.key == key).first()
        if entry:
            entry.value = json.dumps(value)
            entry.expires_at = expires_at
        else:
            entry = CacheEntry(key=key, value=json.dumps(value), expires_at=expires_at)
            db.add(entry)
        db.commit()

    def clear(self, db: Session) -> int:
        count = db.query(CacheEntry).count()
        db.query(CacheEntry).delete()
        db.commit()
        return count


cache_manager = CacheManager()
