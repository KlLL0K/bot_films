from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import ChatType, chat_member
from main import ADMINS



class IsAdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in ADMINS