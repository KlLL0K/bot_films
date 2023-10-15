import logging
import time
from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from main import TOKEN
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='random')
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='нажми', callback_data='random_value'))
    await message.answer('нажми на кнопку, чтобы бот отправил случайное число от 1 до 100', reply_markup=keyboard)


# @dp.callback_query_handler(text='random_value')
# async def send_random(call: types.CallbackQuery):
#     await call.message.answer(str(randint(1, 100)))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
