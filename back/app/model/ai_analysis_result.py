from app.init import db
from datetime import datetime
from decimal import Decimal
import enum

class AiAnalysisResult(db.Model):
    __tablename__ = 'ai_analysis_results'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    news_id = db.Column(
        db.String(20),
        db.ForeignKey('news_articles.news_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    sentiment_score = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    topic_keywords = db.Column(db.JSON, nullable=True)
    viral_potential = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    trend_score = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    content_quality = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    analysis_timestamp = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    # 和新闻表建立关联
    news_article = db.relationship('NewsArticle', backref=db.backref('analysis_results', lazy=True))

    __table_args__ = (
        db.Index('idx_sentiment', 'sentiment_score'),
        db.Index('idx_viral', 'viral_potential'),
        db.Index('idx_trend', 'trend_score'),
        db.Index('idx_analysis_time', 'analysis_timestamp'),
        db.Index('idx_ai_analysis_news_time', 'news_id', 'analysis_timestamp'),
    )