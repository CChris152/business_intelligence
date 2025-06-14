from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class StatusEnum(enum.Enum):
    processing = 'processing'
    completed = 'completed'
    failed = 'failed'

class ProcessingBatch(db.Model):
    __tablename__ = 'processing_batches'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    batch_id = db.Column(db.String(50), unique=True, nullable=False)
    source = db.Column(db.String(50), nullable=True)
    records_count = db.Column(db.Integer, nullable=True, default=0)
    processing_start = db.Column(db.DateTime, nullable=True)
    processing_end = db.Column(db.DateTime, nullable=True)
    processing_duration_ms = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Enum(StatusEnum, name='status_enum'), nullable=True, default=StatusEnum.processing)
    error_details = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.Index('idx_batch_id', 'batch_id'),
        db.Index('idx_status', 'status'),
        db.Index('idx_processing_time', 'processing_start', 'processing_end'),
    )