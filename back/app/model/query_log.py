from sqlalchemy import Index, text

from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class QueryLog(db.Model):
    __tablename__ = 'query_logs'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    query_id = db.Column(db.String(50), unique=True, nullable=False)
    query_type = db.Column(
        db.Enum(
            'lifecycle',
            'category_trend',
            'user_interest',
            'multidim_stat',
            'viral_prediction',
            'recommendation',
            'other'
        ),
        nullable=False
    )
    sql_query = db.Column(db.Text, nullable=False)
    query_parameters = db.Column(db.JSON, nullable=True)
    execution_time_ms = db.Column(db.Integer, nullable=True, default=0)
    result_count = db.Column(db.Integer, nullable=True, default=0)
    user_agent = db.Column(db.String(200), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    query_timestamp = db.Column(db.DateTime, nullable=True, server_default=text('CURRENT_TIMESTAMP'))
    error_message = db.Column(db.Text, nullable=True)

    __table_args__ = (
        Index('idx_query_type', 'query_type'),
        Index('idx_execution_time', 'execution_time_ms'),
        Index('idx_timestamp', 'query_timestamp'),
        Index('idx_performance', 'execution_time_ms', 'result_count'),
    )

    def __repr__(self):
        return f"<QueryLog(id={self.id}, query_id='{self.query_id}', query_type='{self.query_type}')>"