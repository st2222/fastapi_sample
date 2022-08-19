import datetime
from typing import Dict, Optional
import jwt
from db.repositories.user import UserRepositoryImpl
from domain.models.user.email import Email
from domain.models.user.password import HashedPassword
from domain.models.user.user import User

rep = UserRepositoryImpl()

ALGO = 'HS256'
KEY = 'secret'


def login(username: Email, password: HashedPassword) -> Dict:
    user: Optional[User] = rep.find_user_by_email(email=username)
    if user is None:
        raise Exception('user is None')

    if user.password.value == password.value:
        access_token = jwt.encode(
            {'email': username.value, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, KEY,
            algorithm='HS256')
        refresh_token = ''
    else:
        # 例外でもいい？
        # raise HTTPException?
        # raise InValidError的なやつ?
        raise Exception('password invalid')

    return {'access_token': access_token, 'refresh_token': refresh_token}


def verify_token(token: str):
    res = jwt.decode(token, key=KEY, algorithms=ALGO)
    print(res)
    # if False:
    #     raise InvalidException()
