import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from keyboards import kb1, kb3, kb4
from main import TOKEN
API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class Keyboard_Main(ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True, one_time_keyboard=True)
        self.add(KeyboardButton('Напитки'))
        self.add(KeyboardButton('Закуски'))

class KeyboardDrink(ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True, one_time_keyboard=True)
        self.insert(KeyboardButton('Сок'))
        self.insert(KeyboardButton("Газировка"))
        self.add(KeyboardButton('Назад'))

class KeyboardSnack(ReplyKeyboardMarkup):
    def __init__(self):
        super().__init__(resize_keyboard=True, one_time_keyboard=True)
        self.insert(KeyboardButton('Чипсы'))
        self.insert(KeyboardButton('Бургер'))
        self.add(KeyboardButton("Назад"))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.username
    await message.answer(f' Приветствую {user_name}! \nВыбери нужное',
                         reply_markup=Keyboard_Main())

@dp.message_handler(text='Напитки')
async def get_drink(message: types.Message):
    await message.answer('Выбери напиток', reply_markup=KeyboardDrink())


@dp.message_handler(text="Закуски")
async def get_drink(message: types.Message):
    await message.answer('Выбери закуску', reply_markup=KeyboardSnack())


@dp.message_handler(text='Назад')
async def get_drink(message: types.Message):
    await message.answer('Вы вышли в главное меню', reply_markup=Keyboard_Main())


@dp.message_handler(text='Назад')
async def get_drink(message: types.Message):
    await message.answer('Вы вышли в главное меню', reply_markup=Keyboard_Main())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
