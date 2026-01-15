# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from settings import settings


def create_jwt(payload: dict[str, Any], expires_minutes: int | None = None) -> str:
    """Create a jwt token."""

    now = datetime.now(timezone.utc)
    if expires_minutes is None:
        expires_minutes = settings.jwt.expire_minutes
    exp = now + timedelta(minutes=expires_minutes)

    to_encode = payload.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    to_encode.update({"iat": int(now.timestamp()), "exp": int(exp.timestamp())})

    return jwt.encode(
        to_encode,
        settings.jwt.secret,
        algorithm=settings.jwt.algorithm,
    )


def parse_jwt(token: str) -> dict[str, Any]:
    """Parse a jwt token."""

    return jwt.decode(
        token,
        settings.jwt.secret,
        algorithms=[settings.jwt.algorithm],
    )
