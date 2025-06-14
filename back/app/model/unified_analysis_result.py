from app.init import db
from datetime import datetime
from decimal import Decimal
import enum


class UnifiedAnalysisResult(db.Model):
    __tablename__ = 'unified_analysis_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batch_id = db.Column(db.String(64), nullable=True)
    analysis_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)