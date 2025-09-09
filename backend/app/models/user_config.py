from app import db

class UserConfig(db.Model):
    __tablename__ = 'user_config'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    interest = db.Column(db.String(50), nullable=False)        # e.g., "AI", "Sports"
    sentiment_filter = db.Column(db.String(20), default='all') # "positive", "negative", "neutral", "all"
    noise_blocker_enabled = db.Column(db.Boolean, default=True)
    ai_rewrite_enabled = db.Column(db.Boolean, default=True)
