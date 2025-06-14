from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(20), primary_key=True)
    registration_date = db.Column(db.DateTime, nullable=True)
    location_country = db.Column(db.String(50), nullable=True)
    location_province = db.Column(db.String(50), nullable=True)
    location_city = db.Column(db.String(50), nullable=True)
    interests = db.Column(db.JSON, nullable=True)
    demographics = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )

    __table_args__ = (
        db.Index('idx_location', 'location_country', 'location_province', 'location_city'),
        db.Index('idx_registration', 'registration_date'),
    )