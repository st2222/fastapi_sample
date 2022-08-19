from datetime import datetime
from http import HTTPStatus

from starlette.responses import Response

from routers.auth import oauth2_scheme
from application.util import hash_password
from domain.models.user.role import Role
from domain.models.user.password import RawPassword
from domain.models.user.cost_per_hour import CostPerHour
from domain.models.user.image import Image
from domain.models.user.email import Email
from domain.models.user.user_id import UserId
from domain.models.user.user_name import UserName
from pydantic import BaseModel
from typing import Optional, List
from application.user import register, select_all_users, find_user_by_id, delete_user, update_user
from domain.models.user.user import User
from fastapi import APIRouter, HTTPException, Depends

from exception.exception import NotFoundException

router = APIRouter()


class UserModel(BaseModel):
    user_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None
    costPerHour: Optional[int] = None
    created: Optional[datetime] = None
    password: Optional[str] = None
    role: Optional[int] = None

    def to_user(self) -> User:
        return User(user_id=UserId(self.user_id), user_name=UserName(self.name), email=Email(self.email),
                    image=Image(self.image), cost_per_hour=CostPerHour(self.costPerHour),
                    created_at=self.created, password=hash_password(RawPassword(self.password)),
                    role=Role(self.role), delete_flag=False)


@router.post('/users')
def create_user(user_model: UserModel, token=Depends(oauth2_scheme)) -> Response:
    register(user_model.to_user())
    return Response(status_code=HTTPStatus.OK.value)


@router.get('/users')
def get_users(token=Depends(oauth2_scheme)) -> List:
    # verify_token(token)
    user_list = select_all_users()
    for user in user_list:
        print(user.user_id.value)
    return list(
        map(lambda x: UserModel(user_id=x.user_id.value, name=x.user_name.value, email=x.email.value,
                                image=x.image.value,
                                costPerHour=x.cost_per_hour.value, created=x.created_at,
                                role=x.role.value), user_list))


@router.get('/users/{user_id}')
def get_user_by_id(user_id: int, token=Depends(oauth2_scheme)) -> UserModel:
    try:
        user: User = find_user_by_id(UserId(user_id))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return UserModel(user_id=user.user_id.value, name=user.user_name.value, email=user.email.value,
                     image=user.image.value,
                     costPerHour=user.cost_per_hour.value, created=user.created_at,
                     role=user.role.value)


@router.patch('/users/{user_id}')
def update_user_by_id(user_id: int, user_model: UserModel, token=Depends(oauth2_scheme)) -> Response:
    try:
        update_user(UserId(user_id), user_model.dict(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return Response(status_code=HTTPStatus.OK.value)


@router.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user_by_id(user_id: int, token=Depends(oauth2_scheme)) -> Response:
    try:
        delete_user(UserId(user_id))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return Response(status_code=HTTPStatus.NO_CONTENT.value)
