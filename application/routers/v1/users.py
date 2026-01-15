# -*- coding: utf-8 -*-

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from application.models import User
from application.auth import require_user

router = APIRouter(tags=["users"])


class UserModel(BaseModel):
    id: int | None = None
    username: str | None = None
    password: str | None = None
    config_sync_token: str | None = None
    created_at: datetime | None = None
    modified_at: datetime | None = None

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            config_sync_token=user.config_sync_token,
            created_at=user.created_at,
            modified_at=user.modified_at,
        )

    async def create(self):
        assert self.username is not None, "Username is required."
        assert await User.is_username_available(self.username), (
            "Username is not available."
        )
        assert self.password is not None, "Password is required."
        assert User.check_password_integrity(self.password), "Password is too weak."

        return await User.create(
            username=self.username,
            password=User.encrypt_password(self.password),
            config_sync_token=User.create_config_sync_token(),
        )

    async def update(self, user: User):
        params = self.model_dump(
            exclude=[
                "id",
                "username",
                "config_sync_token",
                "created_at",
                "modified_at",
            ],
            exclude_unset=True,
        )
        if "password" in params:
            assert User.check_password_integrity(params["password"]), (
                "Password is too weak."
            )
            params["password"] = User.encrypt_password(params["password"])
        await user.update_from_dict(params)
        user.modified_at = datetime.now()
        await user.save()
        return user

    def model_dump_insensitive(self):
        return self.model_dump(exclude=["password", "config_sync_token"])


class ConfigSyncTokenModel(BaseModel):
    config_sync_token: str


@router.get("/user/", response_model=UserModel)
async def get_current_user(user: User = Depends(require_user())):
    return UserModel.from_orm(user).model_dump_insensitive()


@router.get("/user/config_sync_token/", response_model=ConfigSyncTokenModel)
async def get_config_sync_token(user: User = Depends(require_user("jwt"))):
    return ConfigSyncTokenModel(config_sync_token=user.config_sync_token)


@router.get("/user/config_sync_token/refresh/", response_model=bool)
async def refresh_config_sync_token(user: User = Depends(require_user("jwt"))):
    await user.refresh_config_sync_token()
    return ConfigSyncTokenModel(config_sync_token=user.config_sync_token)


@router.post("/users/", response_model=UserModel)
async def create_user(data: UserModel):
    try:
        user = await data.create()
    except AssertionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return UserModel.from_orm(user).model_dump_insensitive()


@router.patch("/users/", response_model=UserModel)
async def update_user(data: UserModel, user: User = Depends(require_user("jwt"))):
    try:
        user = await data.update(user)
    except AssertionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return UserModel.from_orm(user).model_dump_insensitive()
