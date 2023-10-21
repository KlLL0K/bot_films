import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from main import TOKEN

API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
from aiogram.dispatcher.filters import Command, BoundFilter
from filters import IsGroup, IsPrivate


# @dp.message_handler()
# async def del_m(message: types.Message):
#    await bot.delete_message(message.chat.id, message.message_id)


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()


class IsGroup(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )


check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Проверить подписки', callback_data="check_subs")
        ]
    ]
)
channels = [-4031782044]
from typing import Union


@dp.message_handler(Command("channels"))
async def show_channels(message: types.Message):
    for channel in channels:
        channels_format = str()
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f'Канал <a href="{invite_link}">{chat.title}</a>\n\n'
    await message.answer(f'Вам необходимо подписаться на следующие каналы: \n'
                         f'{channels_format}',
                         reply_markup=check_button,
                         disable_web_page_preview=True)


async def check(user_id, channel: Union[int, str]):
    bot = Bot.get_current()
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in channels:
        status = await check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f'Подписка на канал {channel.title} оформлена!'
        else:
            invite_link = await channel.export_invite_link()
            result += (f'Подписка на канал {channel.title} не оформлена!'
                       f'<a href="{invite_link}">Нужно  подписаться.</a>\n\n')
    await call.message.answer(result, disable_web_page_preview=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
