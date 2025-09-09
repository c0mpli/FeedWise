from app import db

class FollowingRecommendation(db.Model):
    __tablename__ = 'following_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    recommended_user = db.Column(db.String(100), nullable=False) # platform handle
    reason = db.Column(db.String(200))                            # e.g., "common_interest"
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
