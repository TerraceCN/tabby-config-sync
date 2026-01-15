# -*- coding: utf-8 -*-

from fastapi import APIRouter

from . import configs, users

router = APIRouter()
router.include_router(configs.router)
router.include_router(users.router)
