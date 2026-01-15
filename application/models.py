# -*- coding: utf-8 -*-

from secrets import token_hex

from tortoise import fields
from tortoise.models import Model


class Config(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User",
        related_name="configs",
        on_delete=fields.CASCADE,
    )
    name = fields.CharField(max_length=255)
    content = fields.TextField(default="{}")
    last_used_with_version = fields.CharField(max_length=32, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(null=True)


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    config_sync_token = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(null=True)

    configs: fields.ReverseRelation[Config]

    @classmethod
    async def is_username_available(cls, username: str) -> bool:
        """Check if the username is available."""

        return not await cls.filter(username=username).first()

    @staticmethod
    def check_password_integrity(password: str):
        """Check if the password is valid."""

        return len(password) >= 8

    @staticmethod
    def encrypt_password(password: str):
        """Encrypt the password."""

        return password

    def check_password(self, password: str) -> bool:
        """Check if the password is correct."""

        return self.password == self.encrypt_password(password)

    @staticmethod
    def create_config_sync_token() -> str:
        """Create a config sync token."""

        return token_hex(16)

    async def refresh_config_sync_token(self):
        """Refresh the config sync token."""

        self.config_sync_token = self.create_config_sync_token()
        await self.save()
