import logging
import time
from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from main import TOKEN
from aiogram.dispatcher.filters import Text

API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
user_data = {}


def get_keyboard():
    buttons = [types.InlineKeyboardButton(text='+1',callback_data='num_decr'),
               types.InlineKeyboardButton(text='-1',callback_data='num_incr'),
               types.InlineKeyboardButton(text='подтвердить', callback_data='num_finish')
               ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def update_num_message(message: types.Message, new_value: int):
    await message.edit_text(f"укажите число: {new_value}", reply_markup=get_keyboard())


@dp.message_handler(commands='numbers')
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer('укажите число: 0',reply_markup=get_keyboard())


@dp.callback_query_handler(Text(startswith='num_'))
async def callback_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split('_')[1]
    if action == 'incr':
        user_data[call.from_user.id] = user_value - 1
        await update_num_message(call.message, user_value - 1)
    elif action == 'decr':
        user_data[call.from_user.id] = user_value + 1
        await update_num_message(call.message, user_value + 1)
    elif action == 'finish':
        await call.message.delete_reply_markup()
        await call.message.edit_text(f'итого: {user_value}')
    await call.answer()







# @dp.callback_query_handler(text='random_value')
# async def send_random(call: types.CallbackQuery):
#     await call.message.answer(str(randint(1, 100)))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)