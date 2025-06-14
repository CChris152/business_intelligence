from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class NewsLifecycle(db.Model):
    __tablename__ = 'news_lifecycle'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    news_id = db.Column(
        db.String(20),
        db.ForeignKey('news_articles.news_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    time_period = db.Column(db.String(20), nullable=False)
    total_reads = db.Column(db.Integer, nullable=True, default=0)
    total_shares = db.Column(db.Integer, nullable=True, default=0)
    total_likes = db.Column(db.Integer, nullable=True, default=0)
    total_comments = db.Column(db.Integer, nullable=True, default=0)
    unique_readers = db.Column(db.Integer, nullable=True, default=0)
    avg_dwell_time = db.Column(db.Numeric(8, 2), nullable=True, default=Decimal("0.00"))
    popularity_score = db.Column(db.Numeric(5, 2), nullable=True, default=Decimal("0.00"))
    growth_rate = db.Column(db.Numeric(5, 2), nullable=True, default=Decimal("0.00"))
    calculated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    # 建立与新闻表的关系
    news_article = db.relationship('NewsArticle', backref=db.backref('lifecycle', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('news_id', 'time_period', name='unique_news_period'),
        db.Index('idx_period', 'time_period'),
        db.Index('idx_popularity', 'popularity_score'),
        db.Index('idx_growth', 'growth_rate'),
    )
