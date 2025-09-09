from app.db.database import db
from app.types.enums import PostStatus
class PostsSeen(db.Model):
    __tablename__ = 'posts_seen'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    post_url = db.Column(db.String(100), nullable=False)      # platform-specific ID
    status = db.Column(db.Enum(PostStatus), default=PostStatus.NOT_SEEN)     # "liked", "disliked", "neutral"
    seen_at = db.Column(db.DateTime, default=db.func.current_timestamp())
