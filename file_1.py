import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils import executor
from main import TOKEN
from main import ADMINS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class IsAdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in ADMINS


dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(commands=['sleep'], user_id=ADMINS)
async def admin_commands_handler(message: types.Message):
    await message.answer('hi admin')


@dp.message_handler(commands=['sleep1'])
async def admin_commands_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Admin panel', callback_data='admin_panel'))
        await message.answer('hi admin, what do you want to do', reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('support', url='https://youtube.com'))
        await message.answer('hi, how can i help you?', reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
