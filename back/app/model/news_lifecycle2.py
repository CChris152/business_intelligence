from app.init import db
from datetime import datetime


class NewsLifecycle2(db.Model):
    __tablename__ = 'news_lifecycle2'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.String(50), nullable=True)
    time_period = db.Column(db.String(20), nullable=True)
    total_reads = db.Column(db.Integer, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=True,
        server_default=db.func.current_timestamp()
    )
