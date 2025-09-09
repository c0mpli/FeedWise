from app.db.repository.account_repository import AccountRepository
from app.models.account_model import Account
from app.utils.errors import ValidationError, NotFoundError, ConflictError
from app.types.enums import Platform, SentimentFilter
from sqlalchemy.exc import IntegrityError
import json

class AccountService:
    @staticmethod
    def get_all_accounts():
        return AccountRepository.get_all()

    @staticmethod
    def get_account_by_username(username):
        return AccountRepository.get_by_username(username)

    @staticmethod
    def get_account_by_id(account_id):
        account = AccountRepository.get_by_id(account_id)
        if not account:
            raise NotFoundError(f"Account with id {account_id} not found")
        return account

    @staticmethod
    def create_account(account_data):
        AccountService._validate_account_data(account_data)
        
        existing_account = AccountRepository.get_by_username(account_data['username'])
        if existing_account:
            raise ConflictError(f"Account with username {account_data['username']} already exists")
        
        try:
            # Handle platform enum
            platform = Platform(account_data['platform']) if isinstance(account_data['platform'], str) else account_data['platform']
            
            # Handle interests as JSON string
            interests_json = json.dumps(account_data.get('interests', [])) if account_data.get('interests') else None
            
            # Handle sentiment filter enum
            sentiment_filter = SentimentFilter(account_data.get('sentiment_filter', 'all')) if account_data.get('sentiment_filter') else SentimentFilter.ALL
            
            account = Account(
                username=account_data['username'],
                password=account_data['password'],  # TODO: Hash passwords in production
                platform=platform,
                interests=interests_json,
                sentiment_filter=sentiment_filter,
                noise_blocker_enabled=account_data.get('noise_blocker_enabled', True)
            )
            return AccountRepository.create(account)
        except IntegrityError:
            AccountRepository.rollback()
            raise ConflictError(f"Account with username {account_data['username']} already exists")

    @staticmethod
    def update_account(account_id, account_data):
        AccountService._validate_account_data(account_data, is_update=True)
        
        account = AccountRepository.get_by_id(account_id)
        if not account:
            raise NotFoundError(f"Account with id {account_id} not found")
        
        if 'username' in account_data:
            existing_account = AccountRepository.get_by_username(account_data['username'])
            if existing_account and existing_account.id != account_id:
                raise ConflictError(f"Username {account_data['username']} already exists")
        
        try:
            account.username = account_data.get('username', account.username)
            account.password = account_data.get('password', account.password)  # TODO: Hash passwords in production
            
            if 'platform' in account_data:
                account.platform = Platform(account_data['platform']) if isinstance(account_data['platform'], str) else account_data['platform']
            
            if 'interests' in account_data:
                account.interests = json.dumps(account_data['interests']) if account_data['interests'] else None
            
            if 'sentiment_filter' in account_data:
                account.sentiment_filter = SentimentFilter(account_data['sentiment_filter']) if isinstance(account_data['sentiment_filter'], str) else account_data['sentiment_filter']
            
            if 'noise_blocker_enabled' in account_data:
                account.noise_blocker_enabled = account_data['noise_blocker_enabled']
            
            return AccountRepository.update(account)
        except IntegrityError:
            AccountRepository.rollback()
            raise ConflictError("Failed to update account")

    @staticmethod
    def delete_account(account_id):
        account = AccountRepository.get_by_id(account_id)
        if not account:
            raise NotFoundError(f"Account with id {account_id} not found")
        AccountRepository.delete(account)

    @staticmethod
    def _validate_account_data(account_data, is_update=False):
        if not is_update:
            required_fields = ['username', 'password', 'platform']
            for field in required_fields:
                if field not in account_data or not account_data[field]:
                    raise ValidationError(f"Field '{field}' is required")

        if 'username' in account_data and account_data['username']:
            if len(account_data['username']) < 2:
                raise ValidationError("Username must be at least 2 characters long")

        if 'password' in account_data and account_data['password']:
            if len(account_data['password']) < 6:
                raise ValidationError("Password must be at least 6 characters long")

        if 'platform' in account_data and account_data['platform']:
            try:
                Platform(account_data['platform'])
            except ValueError:
                valid_platforms = [p.value for p in Platform]
                raise ValidationError(f"Platform must be one of: {', '.join(valid_platforms)}")
        
        if 'sentiment_filter' in account_data and account_data['sentiment_filter']:
            try:
                SentimentFilter(account_data['sentiment_filter'])
            except ValueError:
                valid_filters = [f.value for f in SentimentFilter]
                raise ValidationError(f"Sentiment filter must be one of: {', '.join(valid_filters)}")
        
        if 'interests' in account_data and account_data['interests']:
            if not isinstance(account_data['interests'], list):
                raise ValidationError("Interests must be a list of strings")