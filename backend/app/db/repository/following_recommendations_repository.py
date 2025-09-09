from app.db.database import db
from app.models.following_recommendations_model import FollowingRecommendation

class FollowingRecommendationsRepository:
    @staticmethod
    def get_all():
        return FollowingRecommendation.query.all()

    @staticmethod
    def get_by_id(rec_id):
        return FollowingRecommendation.query.get(rec_id)

    @staticmethod
    def get_by_account_id(account_id):
        return FollowingRecommendation.query.filter_by(account_id=account_id).all()

    @staticmethod
    def create(recommendation):
        db.session.add(recommendation)
        db.session.commit()
        return recommendation

    @staticmethod
    def update(recommendation):
        db.session.commit()
        return recommendation

    @staticmethod
    def delete(recommendation):
        db.session.delete(recommendation)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()