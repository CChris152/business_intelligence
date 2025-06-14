from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class RealTimeRecommendation(db.Model):
    __tablename__ = 'real_time_recommendations'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.String(20),
        db.ForeignKey('users.user_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    recommended_news = db.Column(db.JSON, nullable=True)
    recommendation_scores = db.Column(db.JSON, nullable=True)
    recommendation_reasons = db.Column(db.JSON, nullable=True)
    context_factors = db.Column(db.JSON, nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    clicked_news = db.Column(db.JSON, nullable=True)
    recommendation_effectiveness = db.Column(db.Numeric(3, 2), nullable=True, default=None)

    # 建立和用户表的关联
    user = db.relationship('User', backref=db.backref('real_time_recommendations', lazy=True))

    __table_args__ = (
        db.Index('idx_user_generated', 'user_id', 'generated_at'),
        db.Index('idx_effectiveness', 'recommendation_effectiveness'),
    )