from app.db.repository.following_recommendations_repository import FollowingRecommendationsRepository
from app.models.following_recommendations_model import FollowingRecommendation
from app.utils.errors import ValidationError, NotFoundError, ConflictError
from app.types.enums import FollowStatus
from sqlalchemy.exc import IntegrityError

class FollowingRecommendationsService:
    @staticmethod
    def get_all_following_recommendations(account_id=None):
        if account_id:
            return FollowingRecommendationsRepository.get_by_account_id(account_id)
        return FollowingRecommendationsRepository.get_all()

    @staticmethod
    def get_following_recommendation_by_id(rec_id):
        recommendation = FollowingRecommendationsRepository.get_by_id(rec_id)
        if not recommendation:
            raise NotFoundError(f"Following recommendation with id {rec_id} not found")
        return recommendation

    @staticmethod
    def create_following_recommendation(rec_data):
        FollowingRecommendationsService._validate_recommendation_data(rec_data)
        
        try:
            # Handle follow status enum
            follow_status = FollowStatus(rec_data.get('follow_status', 'pending')) if rec_data.get('follow_status') else None
            
            recommendation = FollowingRecommendation(
                account_id=rec_data['account_id'],
                recommended_user=rec_data['recommended_user'],
                reason=rec_data.get('reason'),
                follow_status=follow_status
            )
            return FollowingRecommendationsRepository.create(recommendation)
        except IntegrityError:
            FollowingRecommendationsRepository.rollback()
            raise ConflictError("Failed to create following recommendation")

    @staticmethod
    def update_following_recommendation(rec_id, rec_data):
        FollowingRecommendationsService._validate_recommendation_data(rec_data, is_update=True)
        
        recommendation = FollowingRecommendationsRepository.get_by_id(rec_id)
        if not recommendation:
            raise NotFoundError(f"Following recommendation with id {rec_id} not found")
        
        try:
            recommendation.recommended_user = rec_data.get('recommended_user', recommendation.recommended_user)
            recommendation.reason = rec_data.get('reason', recommendation.reason)
            
            if 'follow_status' in rec_data:
                recommendation.follow_status = FollowStatus(rec_data['follow_status']) if isinstance(rec_data['follow_status'], str) else rec_data['follow_status']
            
            return FollowingRecommendationsRepository.update(recommendation)
        except IntegrityError:
            FollowingRecommendationsRepository.rollback()
            raise ConflictError("Failed to update following recommendation")

    @staticmethod
    def delete_following_recommendation(rec_id):
        recommendation = FollowingRecommendationsRepository.get_by_id(rec_id)
        if not recommendation:
            raise NotFoundError(f"Following recommendation with id {rec_id} not found")
        FollowingRecommendationsRepository.delete(recommendation)

    @staticmethod
    def _validate_recommendation_data(rec_data, is_update=False):
        if not is_update:
            required_fields = ['account_id', 'recommended_user']
            for field in required_fields:
                if field not in rec_data or not rec_data[field]:
                    raise ValidationError(f"Field '{field}' is required")

        if 'recommended_user' in rec_data and rec_data['recommended_user']:
            if len(rec_data['recommended_user']) < 2:
                raise ValidationError("Recommended user must be at least 2 characters long")