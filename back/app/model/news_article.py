from sqlalchemy import func

from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci',
        'mysql_row_format': 'Dynamic'
    }

    # 主键字段：自增ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 其它字段
    news_id = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    topic = db.Column(db.String(200), nullable=True)
    headline = db.Column(db.Text, nullable=True)  # longtext对应Text
    news_body = db.Column(db.Text, nullable=True)  # longtext对应Text
    title_entity = db.Column(db.Text, nullable=True)  # longtext对应Text
    entity_content = db.Column(db.Text, nullable=True)  # longtext对应Text
    created_at = db.Column(
        db.DateTime,
        nullable=True,
        server_default=func.current_timestamp()
    )