from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class PerformanceMetric(db.Model):
    __tablename__ = 'performance_metrics'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    metric_type = db.Column(db.String(50), nullable=False)
    metric_value = db.Column(db.Numeric(10, 2), nullable=False)
    metric_unit = db.Column(db.String(20), nullable=True)
    dimensions = db.Column(db.JSON, nullable=True)
    measured_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_metric_type', 'metric_type'),
        db.Index('idx_measured_time', 'measured_at'),
    )