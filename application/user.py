from domain.models.user.user_id import UserId
from typing import List
from db.repositories.user import UserRepositoryImpl
from domain.models.user.user import User
from domain.services.user import exists
from exception.exception import NotFoundException

user_rep = UserRepositoryImpl()


def register(user: User) -> None:
    user_rep.insert(user)


def select_all_users() -> List[User]:
    return user_rep.select()


def find_user_by_id(user_id: UserId) -> User:
    user: User = user_rep.find_user_by_id(user_id)
    if not exists(user):
        raise NotFoundException(f'{user_id.value} is not found user')
    return user


def find_user_by_email(user_id: UserId) -> User:
    user: User = user_rep.find_user_by_id(user_id)
    if not exists(user):
        raise NotFoundException(f'{user_id.value} is not found user')
    return user


def delete_user(user_id: UserId) -> None:
    user: User = user_rep.find_user_by_id(user_id)
    if not exists(user):
        raise NotFoundException(f'{user_id.value} is not found user')
    user_rep.delete_user(user)


def update_user(user_id: UserId, body) -> None:
    user: User = user_rep.find_user_by_id(user_id)
    if not exists(user):
        raise NotFoundException(f'{user_id.value} is not found user')
    user_rep.update_user(user_id, body)
