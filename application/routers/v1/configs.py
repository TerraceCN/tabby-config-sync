# -*- coding: utf-8 -*-

from datetime import datetime

from fastapi import APIRouter, Depends, Response, HTTPException, status
from pydantic import BaseModel

from application.models import Config, User
from application.auth import require_user

router = APIRouter(tags=["configs"])


class ConfigModel(BaseModel):
    id: int | None = None
    name: str | None = None
    content: str | None = "{}"
    last_used_with_version: str | None = None
    created_at: datetime | None = None
    modified_at: datetime | None = None

    @classmethod
    def from_orm(cls, record: Config):
        return cls(
            id=record.id,
            name=record.name,
            content=record.content,
            last_used_with_version=record.last_used_with_version,
            created_at=record.created_at,
            modified_at=record.modified_at,
        )

    async def create(self, user: User):
        return await Config.create(
            user=user,
            name=self.name,
            content=self.content,
            last_used_with_version=self.last_used_with_version,
        )

    async def update(self, config: Config):
        params = self.model_dump(
            exclude=["id", "created_at", "modified_at"],
            exclude_unset=True,
        )
        await config.update_from_dict(params)
        config.modified_at = datetime.now()
        await config.save()
        return config


@router.get("/configs", response_model=list[ConfigModel])
async def get_configs(user: User = Depends(require_user())):
    configs: list[Config] = await user.configs.all()
    return [
        ConfigModel.from_orm(config).model_dump(exclude=["content"])
        for config in configs
    ]


@router.get("/configs/{config_id}", response_model=ConfigModel)
async def get_config(config_id: int, user: User = Depends(require_user())):
    config: Config | None = await Config.get_or_none(id=config_id, user=user)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Config not found"
        )
    return ConfigModel.from_orm(config)


@router.post("/configs", response_model=ConfigModel)
async def create_config(data: ConfigModel, user: User = Depends(require_user())):
    config = await data.create(user)
    return ConfigModel.from_orm(config)


@router.patch("/configs/{config_id}", response_model=ConfigModel)
async def update_config(
    config_id: int, data: ConfigModel, user: User = Depends(require_user())
):
    config: Config | None = await Config.get_or_none(id=config_id, user=user)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Config not found"
        )
    config = await data.update(config)
    return ConfigModel.from_orm(config)


@router.delete("/configs/{config_id}")
async def delete_config(config_id: int, user: User = Depends(require_user())):
    config: Config | None = await Config.get_or_none(id=config_id, user=user)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Config not found"
        )
    await config.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
