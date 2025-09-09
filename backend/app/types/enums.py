from enum import Enum

class Platform(Enum):
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"

class PostStatus(Enum):
    LIKED = "liked"
    DISLIKED = "disliked"
    SAVED = "saved"
    NOT_SEEN = "not_seen"

class SentimentFilter(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    ALL = "all"

class FollowStatus(Enum):
    PENDING = "pending"      # Not yet decided
    FOLLOWED = "followed"    # User chose to follow
    SKIPPED = "skipped"      # User chose not to follow
