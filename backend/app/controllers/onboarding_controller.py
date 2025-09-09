from flask import request, jsonify
from app.services.onboarding_service import OnboardingService
from app.utils.errors import APIError, ValidationError
import json

class OnboardingController:
    @staticmethod
    def process_onboarding_step():
        """Process onboarding flow based on step parameter and HTTP method"""
        try:
            step = request.args.get('step')
            if not step:
                raise ValidationError("Step parameter is required")
            
            step = int(step)
            
            if request.method == 'POST':
                return OnboardingController._execute_post_step(step)
            elif request.method == 'GET':
                return OnboardingController._execute_get_step(step)
            
        except ValueError:
            raise ValidationError("Step must be a valid number")
        except (ValidationError, APIError):
            raise
        except Exception as e:
            print(f"Onboarding error: {str(e)}")  # Debug logging
            raise APIError(f"Failed to handle onboarding request: {str(e)}", status_code=500)
    
    @staticmethod
    def _execute_post_step(step):
        """Execute POST operations for specific onboarding steps"""
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        if step == 0:
            # Step 0: Create account
            return OnboardingController._create_new_account(data)
        else:
            raise ValidationError(f"Invalid POST step: {step}")
    
    @staticmethod
    def _create_new_account(account_data):
        """Create a new user account (Step 0)"""
        account = OnboardingService.create_account(account_data)
        return jsonify({
            'message': 'Account created successfully',
            'account': {
                'id': account.id,
                'username': account.username,
                'platform': account.platform.value if account.platform else None,
                'created_at': account.created_at.isoformat() if account.created_at else None
            },
            'next_step': 1
        }), 201
    
    @staticmethod
    def _execute_get_step(step):
        """Execute GET operations for specific onboarding steps"""
        if step == 2:
            return OnboardingController._fetch_user_recommendations()
        elif step == 3:
            return OnboardingController._complete_user_onboarding()
        else:
            raise ValidationError(f"Invalid GET step: {step}")
    
    @staticmethod
    def _fetch_user_recommendations():
        """Fetch pending recommendations for user (Step 2)"""
        account_id = request.args.get('account_id')
        if not account_id:
            raise ValidationError("account_id parameter is required for step 2")
        
        try:
            account_id = int(account_id)
        except ValueError:
            raise ValidationError("account_id must be a valid number")
        
        pending_recommendations = OnboardingService.get_pending_recommendations(account_id)
        
        return jsonify({
            'message': 'Recommendations fetched successfully',
            'recommendations': [{
                'id': rec.id,
                'recommended_user': rec.recommended_user,
                'reason': rec.reason,
                'follow_status': rec.follow_status.value if rec.follow_status else None
            } for rec in pending_recommendations],
            'next_step': 'dashboard'
        }), 200
    
    @staticmethod
    def _complete_user_onboarding():
        """Complete onboarding process and return final data (Step 3)"""
        account_id = request.args.get('account_id')
        if not account_id:
            raise ValidationError("account_id parameter is required for step 3")
        
        try:
            account_id = int(account_id)
        except ValueError:
            raise ValidationError("account_id must be a valid number")
        
        onboarding_data = OnboardingService.complete_onboarding(account_id)
        account = onboarding_data['account']
        stats = onboarding_data['stats']
        
        return jsonify({
            'message': 'Onboarding completed successfully',
            'account': {
                'id': account.id,
                'username': account.username,
                'platform': account.platform.value if account.platform else None,
                'interests': json.loads(account.interests) if account.interests else [],
                'sentiment_filter': account.sentiment_filter.value if account.sentiment_filter else None,
                'noise_blocker_enabled': account.noise_blocker_enabled
            },
            'stats': stats,
            'status': 'onboarding_complete'
        }), 200
    
    @staticmethod
    def update_onboarding_data():
        """Update onboarding data based on request type (preferences or follow status)"""
        try:
            data = request.get_json()
            if not data:
                raise ValidationError("Request body is required")
            
            update_type = data.get('type')
            if not update_type:
                raise ValidationError("Update type is required")
            
            if update_type == 'preferences':
                return OnboardingController._update_user_preferences(data)
            elif update_type == 'follow_status':
                return OnboardingController._update_follow_status(data)
            else:
                raise ValidationError(f"Invalid update type: {update_type}")
                
        except (ValidationError, APIError):
            raise
        except Exception as e:
            print(f"Update error: {str(e)}")  # Debug logging
            raise APIError(f"Failed to handle update request: {str(e)}", status_code=500)
    
    @staticmethod
    def _update_user_preferences(data):
        """Update user preferences and generate recommendations (Step 1)"""
        account_id = data.get('account_id')
        if not account_id:
            raise ValidationError("account_id is required for preferences update")
        
        preferences_data = data.get('data', {})
        account = OnboardingService.set_preferences(account_id, preferences_data)
        
        # Generate recommendations based on interests
        OnboardingService.generate_recommendations(account_id)
        
        return jsonify({
            'message': 'Preferences set successfully',
            'account': {
                'id': account.id,
                'username': account.username,
                'platform': account.platform.value if account.platform else None,
                'interests': json.loads(account.interests) if account.interests else [],
                'sentiment_filter': account.sentiment_filter.value if account.sentiment_filter else None,
                'noise_blocker_enabled': account.noise_blocker_enabled,
                'created_at': account.created_at.isoformat() if account.created_at else None
            },
            'next_step': 2
        }), 200
    
    @staticmethod
    def _update_follow_status(data):
        """Update follow status for recommendations (Step 2)"""
        recommendation_updates = data.get('recommendations', [])
        updated_recommendations = OnboardingService.update_follow_decisions(recommendation_updates)
        
        formatted_recommendations = [{
            'id': rec.id,
            'recommended_user': rec.recommended_user,
            'follow_status': rec.follow_status.value if rec.follow_status else None
        } for rec in updated_recommendations]
        
        return jsonify({
            'message': 'Follow status updated successfully',
            'updated_recommendations': formatted_recommendations,
            'next_step': 3
        }), 200