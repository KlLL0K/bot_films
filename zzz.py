from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import ChatType
from main import ADMINS


class IsAdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        return member.status in ADMINS


