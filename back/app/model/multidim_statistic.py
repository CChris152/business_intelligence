from app.init import db
from datetime import datetime
from decimal import Decimal
import enum

class StatTypeEnum(enum.Enum):
    time_based = 'time_based'
    topic_based = 'topic_based'
    title_length = 'title_length'
    content_length = 'content_length'
    user_based = 'user_based'

class MultidimStatistic(db.Model):
    __tablename__ = 'multidim_statistics'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    stat_type = db.Column(db.Enum(StatTypeEnum, name='stat_type_enum'), nullable=False)
    dimension_keys = db.Column(db.JSON, nullable=True)
    time_range = db.Column(db.String(50), nullable=True)
    result_metrics = db.Column(db.JSON, nullable=True)
    sample_size = db.Column(db.Integer, nullable=True, default=0)
    calculated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_stat_type', 'stat_type'),
        db.Index('idx_time_range', 'time_range'),
        db.Index('idx_calculated', 'calculated_at'),
    )