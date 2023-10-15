import logging
import random
import re
import time
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from main import TOKEN
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#функция которая генерит случайное число
def random_num():
    return random.randint(1, 10)

#создание клавиатуры начального меню с кнопками начать и отмена
start_menu = InlineKeyboardMarkup(resize_keyboard=True)
button_start = InlineKeyboardButton('Начать', callback_data='startgame')
button_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
start_menu.add(button_start, button_cancel)

user_data = {} #пустой словарь

@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    await message.answer('Привет, угадай число.\nДля запуска игры нажми начать', reply_markup=start_menu) # вызывается клавиатура


# обработчик кнопки ОТМЕНА
@dp.callback_query_handler(Text(equals='cancel'))
async def end_game_command(call: types.CallbackQuery):
    await call.message.delete() # удаляем текущее сообщение

@dp.callback_query_handler(Text(equals='startgame'))
async def start_game_command(call:types.CallbackQuery):

    user_data[call.from_user.id] = {'secret_number': random_num(), 'attempts':3 }
    await call.message.answer("Я загадал число от 1 до 10\n Попробуй угадай его!\nОтправь мне число в цифрах")
    await bot.answer_callback_query(call.id)
    await call.message.delete()
    print(user_data[call.from_user.id]['secret_number'])

@dp.message_handler(regexp=re.compile(r'^\d+$')) # ^ начало строки, \d-цифры от 0 -9, + - может повторятся только один раз
async def check_numbers(message:types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.reply('для начала нажмите старт')
        return

    user_data[user_id]['attempts'] -=1
    user_number = int(message.text)




    if user_number > user_data[user_id]['secret_number']:
        await message.reply(f"Секретное число меньше. Количество попыток:{user_data[user_id]['attempts']}")

    elif user_number < user_data[user_id]['secret_number']:
        await message.reply(f"Секретное число больше. Количество попыток:{user_data[user_id]['attempts']}")

    else:
        await message.reply('Вы угадали. Хотите еще?', reply_markup=start_menu)
        del user_data[user_id]
        return

    if user_data[user_id]['attempts'] ==0:
        await message.reply(f'Вы проиграли. Число было{user_data[user_id]["secret_number"]}',reply_markup=start_menu)
        del user_data[user_id]
        return
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)