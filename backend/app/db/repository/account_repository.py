from app.db.database import db
from app.models.account_model import Account

class AccountRepository:
    @staticmethod
    def get_all():
        return Account.query.all()

    @staticmethod
    def get_by_id(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def get_by_username(username):
        return Account.query.filter_by(username=username).first()

    @staticmethod
    def create(account):
        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def update(account):
        db.session.commit()
        return account

    @staticmethod
    def delete(account):
        db.session.delete(account)
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()