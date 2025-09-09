from app.db.database import db
from app.models.posts_seen_model import PostsSeen

class PostsSeenRepository:
    @staticmethod
    def get_all():
        return PostsSeen.query.all()

    @staticmethod
    def get_by_id(post_id):
        return PostsSeen.query.get(post_id)

    @staticmethod
    def get_by_account_id(account_id):
        return PostsSeen.query.filter_by(account_id=account_id).all()

    @staticmethod
    def create(post):
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def update(post):
        db.session.commit()
        return post

    @staticmethod
    def delete(post):
        db.session.delete(post)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()