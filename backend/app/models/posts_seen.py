from app import db

class PostsSeen(db.Model):
    __tablename__ = 'posts_seen'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    post_url = db.Column(db.String(100), nullable=False)      # platform-specific ID
    status = db.Column(db.String(20), default='neutral')     # "liked", "disliked", "neutral"
    seen_at = db.Column(db.DateTime, default=db.func.current_timestamp())
