from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class ActionTypeEnum(enum.Enum):
    read = "read"
    skip = "skip"
    share = "share"
    like = "like"
    comment = "comment"
    click = "click"

# 定义阅读时段枚举
class ReadingTimeOfDayEnum(enum.Enum):
    morning = "morning"
    afternoon = "afternoon"
    evening = "evening"
    night = "night"

class UserEvent(db.Model):
    __tablename__ = 'user_events'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.String(20),
        db.ForeignKey('users.user_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    news_id = db.Column(
        db.String(20),
        db.ForeignKey('news_articles.news_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    action_type = db.Column(db.Enum(ActionTypeEnum, name="action_type_enum"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.String(50), nullable=True)
    dwell_time = db.Column(db.Integer, nullable=True, default=0)
    device_type = db.Column(db.String(20), nullable=True)
    os = db.Column(db.String(20), nullable=True)
    browser = db.Column(db.String(30), nullable=True)
    scroll_depth = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    clicks_count = db.Column(db.Integer, nullable=True, default=0)
    shares_count = db.Column(db.Integer, nullable=True, default=0)
    comments_count = db.Column(db.Integer, nullable=True, default=0)
    likes_count = db.Column(db.Integer, nullable=True, default=0)
    reading_time_of_day = db.Column(db.Enum(ReadingTimeOfDayEnum, name="reading_time_of_day_enum"), nullable=True)
    is_weekend = db.Column(db.Boolean, nullable=True, default=False)
    engagement_score = db.Column(db.Numeric(3, 2), nullable=True, default=Decimal("0.00"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    # 建立和用户、新闻文章的关联
    user = db.relationship('User', backref=db.backref('user_events', lazy=True))
    news_article = db.relationship('NewsArticle', backref=db.backref('user_events', lazy=True))

    __table_args__ = (
        db.Index('idx_user_time', 'user_id', 'timestamp'),
        db.Index('idx_news_time', 'news_id', 'timestamp'),
        db.Index('idx_action_time', 'action_type', 'timestamp'),
        db.Index('idx_session', 'session_id'),
        db.Index('idx_dwell_time', 'dwell_time'),
        db.Index('idx_engagement', 'engagement_score'),
        db.Index('idx_user_events_composite', 'user_id', 'news_id', 'timestamp'),
    )