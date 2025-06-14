from app.init import db
from datetime import datetime
from decimal import Decimal
import enum

class CategoryTrend(db.Model):
    __tablename__ = 'category_trends'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(100), nullable=True)
    date_hour = db.Column(db.DateTime, nullable=False)
    total_articles = db.Column(db.Integer, nullable=True, default=0)
    total_reads = db.Column(db.Integer, nullable=True, default=0)
    total_interactions = db.Column(db.Integer, nullable=True, default=0)
    avg_engagement = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    trending_keywords = db.Column(db.JSON, nullable=True)
    hot_topics = db.Column(db.JSON, nullable=True)
    calculated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('category', 'topic', 'date_hour', name='unique_category_hour'),
        db.Index('idx_category_time', 'category', 'date_hour'),
        db.Index('idx_engagement_trend', 'avg_engagement'),
        db.Index('idx_hot_topics', 'date_hour'),
        db.Index('idx_category_trends_time', 'category', 'date_hour'),
    )