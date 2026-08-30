from aiogram import Router

from .common import router as common_router
from .connection import router as connection_router
from .parser import router as parser_router

router = Router()

router.include_routers(common_router, connection_router, parser_router)
