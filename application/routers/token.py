# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from application.models import User
from application.auth import create_user_jwt

router = APIRouter(tags=["token"])


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get the jwt token."""

    user = await User.filter(username=form_data.username).first()
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_user_jwt(user)
    return {"access_token": token, "token_type": "bearer"}
