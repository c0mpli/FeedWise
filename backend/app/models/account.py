from app import db

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # e.g., "twitter"
    username = db.Column(db.String(50), nullable=False)
    access_token = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    configs = db.relationship('UserConfig', backref='account', lazy=True)
    posts_seen = db.relationship('PostsSeen', backref='account', lazy=True)
    following_recommendations = db.relationship('FollowingRecommendation', backref='account', lazy=True)
