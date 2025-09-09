from app.services.account_service import AccountService
from app.services.following_recommendations_service import FollowingRecommendationsService
from app.services.posts_seen_service import PostsSeenService
from app.utils.errors import ValidationError, NotFoundError
import json

class OnboardingService:
    @staticmethod
    def create_account(account_data):
        """Step 0: Create account with basic info"""
        return AccountService.create_account(account_data)
    
    @staticmethod
    def set_preferences(account_id, preferences_data):
        """Step 1: Update account with interests and preferences"""
        return AccountService.update_account(account_id, preferences_data)
    
    @staticmethod
    def generate_recommendations(account_id):
        """Generate recommendations based on account interests"""
        account = AccountService.get_account_by_id(account_id)
        
        if not account.interests:
            raise ValidationError("Account must have interests set before generating recommendations")
        
        interests = json.loads(account.interests)
        platform = account.platform.value
        
        # Generate sample recommendations based on interests and platform
        sample_recommendations = OnboardingService._get_sample_recommendations(interests, platform)
        
        # Create recommendation records
        created_recommendations = []
        for rec_data in sample_recommendations:
            rec_data['account_id'] = account_id
            recommendation = FollowingRecommendationsService.create_following_recommendation(rec_data)
            created_recommendations.append(recommendation)
        
        return created_recommendations
    
    @staticmethod
    def get_pending_recommendations(account_id):
        """Step 2: Get pending recommendations for the account"""
        recommendations = FollowingRecommendationsService.get_all_following_recommendations(account_id=account_id)
        return [rec for rec in recommendations if rec.follow_status.value == 'pending']
    
    @staticmethod
    def update_follow_decisions(recommendation_updates):
        """Step 2: Update follow status for multiple recommendations"""
        updated_recommendations = []
        
        for update in recommendation_updates:
            rec_id = update.get('id')
            follow_status = update.get('follow_status')
            
            if not rec_id or not follow_status:
                continue
            
            recommendation = FollowingRecommendationsService.update_following_recommendation(
                rec_id, {'follow_status': follow_status}
            )
            updated_recommendations.append(recommendation)
        
        return updated_recommendations
    
    @staticmethod
    def complete_onboarding(account_id):
        """Complete onboarding and return dashboard summary"""
        account = AccountService.get_account_by_id(account_id)
        recommendations = FollowingRecommendationsService.get_all_following_recommendations(account_id=account_id)
        
        followed_count = len([rec for rec in recommendations if rec.follow_status.value == 'followed'])
        skipped_count = len([rec for rec in recommendations if rec.follow_status.value == 'skipped'])
        
        return {
            'account': account,
            'stats': {
                'followed_count': followed_count,
                'skipped_count': skipped_count,
                'total_recommendations': len(recommendations)
            }
        }
    
    @staticmethod
    def _get_sample_recommendations(interests, platform):
        """Generate sample recommendations based on interests and platform"""
        recommendations_map = {
            'twitter': {
                'technology': [
                    {'recommended_user': '@elonmusk', 'reason': 'Tech industry leader and innovator'},
                    {'recommended_user': '@sundarpichai', 'reason': 'Google CEO, technology insights'},
                    {'recommended_user': '@satyanadella', 'reason': 'Microsoft CEO, tech leadership'}
                ],
                'sports': [
                    {'recommended_user': '@espn', 'reason': 'Sports news and updates'},
                    {'recommended_user': '@sportscenter', 'reason': 'Sports highlights and analysis'},
                    {'recommended_user': '@nfl', 'reason': 'Official NFL account'}
                ],
                'fitness': [
                    {'recommended_user': '@therock', 'reason': 'Fitness motivation and workouts'},
                    {'recommended_user': '@nike', 'reason': 'Fitness and athletic content'},
                    {'recommended_user': '@fitnessmotivation', 'reason': 'Daily fitness inspiration'}
                ],
                'travel': [
                    {'recommended_user': '@natgeotravel', 'reason': 'Beautiful travel photography'},
                    {'recommended_user': '@lonelyplanet', 'reason': 'Travel guides and tips'},
                    {'recommended_user': '@wanderlust', 'reason': 'Travel inspiration and stories'}
                ]
            },
            'instagram': {
                'technology': [
                    {'recommended_user': '@apple', 'reason': 'Latest tech products and innovations'},
                    {'recommended_user': '@google', 'reason': 'Tech updates and behind the scenes'},
                    {'recommended_user': '@tesla', 'reason': 'Electric vehicles and tech'}
                ],
                'fitness': [
                    {'recommended_user': '@mrolympia', 'reason': 'Bodybuilding and fitness content'},
                    {'recommended_user': '@nike', 'reason': 'Athletic wear and fitness motivation'},
                    {'recommended_user': '@adidas', 'reason': 'Sports and fitness lifestyle'}
                ]
            }
        }
        
        sample_recommendations = []
        platform_recs = recommendations_map.get(platform, {})
        
        for interest in interests:
            interest_recs = platform_recs.get(interest.lower(), [])
            sample_recommendations.extend(interest_recs[:2])  # Limit to 2 per interest
        
        # Add some default recommendations if no specific interests found
        if not sample_recommendations and platform == 'twitter':
            sample_recommendations = [
                {'recommended_user': '@twitter', 'reason': 'Official Twitter account'},
                {'recommended_user': '@twitterapi', 'reason': 'Twitter API updates'}
            ]
        elif not sample_recommendations and platform == 'instagram':
            sample_recommendations = [
                {'recommended_user': '@instagram', 'reason': 'Official Instagram account'},
                {'recommended_user': '@creators', 'reason': 'Creator community content'}
            ]
        
        return sample_recommendations[:5]  # Limit to 5 total recommendations