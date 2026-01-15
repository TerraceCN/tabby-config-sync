# -*- coding: utf-8 -*-

from fastapi import APIRouter

from . import v1, token

router = APIRouter()
router.include_router(v1.router, prefix="/1")
router.include_router(token.router)
