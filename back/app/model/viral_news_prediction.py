from app.init import db
from datetime import datetime
from decimal import Decimal
import enum

class ViralNewsPrediction(db.Model):
    __tablename__ = 'viral_news_prediction'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    news_id = db.Column(
        db.String(20),
        db.ForeignKey('news_articles.news_id', ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False
    )
    viral_score = db.Column(db.Numeric(5, 2), nullable=True, default=Decimal("0.00"))
    predicted_peak_time = db.Column(db.DateTime, nullable=True)
    key_factors = db.Column(db.JSON, nullable=True)
    social_signals = db.Column(db.JSON, nullable=True)
    trend_indicators = db.Column(db.JSON, nullable=True)
    actual_performance = db.Column(db.JSON, nullable=True)
    prediction_accuracy = db.Column(db.Numeric(3, 2), nullable=True, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    news_article = db.relationship('NewsArticle', backref=db.backref('viral_predictions', lazy=True))

    __table_args__ = (
        db.Index('news_id', 'news_id'),
        db.Index('idx_viral_score', 'viral_score'),
        db.Index('idx_predicted_time', 'predicted_peak_time'),
        db.Index('idx_accuracy', 'prediction_accuracy'),
    )