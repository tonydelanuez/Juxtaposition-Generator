import uuid
from app import db
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.sql import func


class UUIDMixin(object):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

class TimeStampedMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

class Wallpaper(UUIDMixin, TimeStampedMixin, db.Model):
    raw = db.Column(BYTEA, default=None, nullable=False)

class Comment(UUIDMixin, TimeStampedMixin, db.Model):
    text = db.Column(db.Text, nullable=False)

class GeneratedCombo(UUIDMixin, TimeStampedMixin, db.Model):
    wallpaper = db.Column(UUID(as_uuid=True), db.ForeignKey('wallpaper.id'))


