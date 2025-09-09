from app.db.database import db
from app.types.enums import Platform, SentimentFilter

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # TODO: Hash passwords in production
    platform = db.Column(db.Enum(Platform), nullable=False)
    interests = db.Column(db.Text)  # JSON string of interests
    sentiment_filter = db.Column(db.Enum(SentimentFilter), default=SentimentFilter.POSITIVE)
    noise_blocker_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    posts_seen = db.relationship('PostsSeen', backref='account', lazy=True)
    following_recommendations = db.relationship('FollowingRecommendation', backref='account', lazy=True)
