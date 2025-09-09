from app.db.repository.posts_seen_repository import PostsSeenRepository
from app.models.posts_seen_model import PostsSeen
from app.utils.errors import ValidationError, NotFoundError, ConflictError
from sqlalchemy.exc import IntegrityError

class PostsSeenService:
    @staticmethod
    def get_all_posts_seen(account_id=None):
        if account_id:
            return PostsSeenRepository.get_by_account_id(account_id)
        return PostsSeenRepository.get_all()

    @staticmethod
    def get_post_seen_by_id(post_id):
        post = PostsSeenRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post seen record with id {post_id} not found")
        return post

    @staticmethod
    def create_posts_seen(post_data):
        PostsSeenService._validate_post_data(post_data)
        
        try:
            post = PostsSeen(
                account_id=post_data['account_id'],
                post_url=post_data['post_url'],
                status=post_data.get('status', 'neutral')
            )
            return PostsSeenRepository.create(post)
        except IntegrityError:
            PostsSeenRepository.rollback()
            raise ConflictError("Failed to create post seen record")

    @staticmethod
    def update_posts_seen(post_id, post_data):
        PostsSeenService._validate_post_data(post_data, is_update=True)
        
        post = PostsSeenRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post seen record with id {post_id} not found")
        
        try:
            post.status = post_data.get('status', post.status)
            return PostsSeenRepository.update(post)
        except IntegrityError:
            PostsSeenRepository.rollback()
            raise ConflictError("Failed to update post seen record")

    @staticmethod
    def delete_posts_seen(post_id):
        post = PostsSeenRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post seen record with id {post_id} not found")
        PostsSeenRepository.delete(post)

    @staticmethod
    def _validate_post_data(post_data, is_update=False):
        if not is_update:
            required_fields = ['account_id', 'post_url']
            for field in required_fields:
                if field not in post_data or not post_data[field]:
                    raise ValidationError(f"Field '{field}' is required")

        if 'post_url' in post_data and post_data['post_url']:
            if not post_data['post_url'].startswith(('http://', 'https://')):
                raise ValidationError("Post URL must be a valid URL")

        if 'status' in post_data and post_data['status']:
            valid_statuses = ['liked', 'disliked', 'neutral', 'saved']
            if post_data['status'] not in valid_statuses:
                raise ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")