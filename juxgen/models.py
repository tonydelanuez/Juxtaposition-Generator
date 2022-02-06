import random
import uuid
from app import db
from sqlalchemy.sql.expression import func, select
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.sql import func


class TimeStampedMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class Wallpaper(TimeStampedMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw = db.Column(BYTEA, default=None, nullable=False)


class Comment(TimeStampedMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)


class GeneratedCombo(TimeStampedMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallpaper = db.Column(db.Integer, db.ForeignKey("wallpaper.id"))
    comment = db.Column(db.Integer, db.ForeignKey("comment.id"))
