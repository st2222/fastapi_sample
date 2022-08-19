from http import HTTPStatus
from pydantic import BaseModel
from typing import Dict, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException

from application.auth import login
from application.util import hash_password
from domain.models.user.email import Email
from domain.models.user.password import HashedPassword, RawPassword
from domain.models.user.user_id import UserId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginModel(BaseModel):
    # email: Optional[str] = None
    user_id: Optional[int] = None
    password: Optional[str] = None


# HeaderにAuthorizationがなかったらID/Passでトークンを返すあれば認証する。
# 返されたTokenをDecodeし検証する。
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        res: Dict = login(Email(form_data.username), hash_password(RawPassword(form_data.password)))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Incorrect username or password{e}")

    return {"access_token": res['access_token'], "token_type": "bearer"}
