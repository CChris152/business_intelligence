from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class UserInterestEvolution(db.Model):
    __tablename__ = 'user_interest_evolution'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.String(20),
        db.ForeignKey('users.user_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    date_period = db.Column(db.Date, nullable=False)
    interest_categories = db.Column(db.JSON, nullable=True)
    interest_scores = db.Column(db.JSON, nullable=True)
    reading_patterns = db.Column(db.JSON, nullable=True)
    behavior_changes = db.Column(db.JSON, nullable=True)
    engagement_trend = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    diversity_score = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    user = db.relationship('User', backref=db.backref('interest_evolutions', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date_period', name='unique_user_period'),
        db.Index('idx_user_date', 'user_id', 'date_period'),
        db.Index('idx_engagement_trend_user', 'engagement_trend'),
        db.Index('idx_diversity', 'diversity_score'),
    )