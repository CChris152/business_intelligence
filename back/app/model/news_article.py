from app.init import db
from datetime import datetime
from decimal import Decimal
import enum

class NewsArticle(db.Model):
    __tablename__ = 'news_articles'

    news_id = db.Column(db.String(20), primary_key=True)
    headline = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)  # longtext 可映射为 Text
    category = db.Column(db.String(50), nullable=True)
    topic = db.Column(db.String(100), nullable=True)
    word_count = db.Column(db.Integer, nullable=True, default=0)
    publish_time = db.Column(db.DateTime, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.JSON, nullable=True)
    entities = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.Index('idx_category', 'category'),
        db.Index('idx_topic', 'topic'),
        db.Index('idx_publish_time', 'publish_time'),
        db.Index('idx_word_count', 'word_count'),
        db.Index('idx_news_articles_category_topic', 'category', 'topic'),
    )