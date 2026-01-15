# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from application.models import User
from application.jwt import create_jwt, parse_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


async def get_user_by_config_sync_token(config_sync_token: str) -> User:
    """Get the user by config sync token."""

    user = await User.filter(config_sync_token=config_sync_token).first()
    return user


async def get_user_by_jwt_token(jwt_token: str) -> User:
    """Get the user by jwt token."""

    try:
        payload = parse_jwt(jwt_token)
        user_id = int(payload["sub"])
        return await User.get_or_none(id=user_id)
    except PyJWTError:
        return None


async def get_user_auto(token: str) -> User:
    """Get the user by token."""

    if "." in token:
        return await get_user_by_jwt_token(token)
    else:
        return await get_user_by_config_sync_token(token)


def require_user(token_type: str = "auto") -> User:
    """Require the user to be authenticated."""

    async def _require_user(token: str = Depends(oauth2_scheme)) -> User:
        if token_type == "auto":
            user = await get_user_auto(token)
        elif token_type == "jwt":
            user = await get_user_by_jwt_token(token)
        elif token_type == "sync":
            user = await get_user_by_config_sync_token(token)
        else:
            raise ValueError("token_type must be 'auto', 'jwt' or 'sync'.")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    return _require_user


def create_user_jwt(user: User, expires_minutes: int | None = None) -> str:
    """Create a jwt token for the user."""

    return create_jwt({"sub": str(user.id)}, expires_minutes)
