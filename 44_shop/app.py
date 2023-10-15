from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
import logging
from loader import db
from main import TOKEN, ADMINS

API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_message = 'Пользователь'
admin_message = 'Админ'


class CheckoutState(StatesGroup):
    check_cart = State()
    name = State()
    address = State()
    confirm = State()


class ProductState(StatesGroup):
    title = State()
    body = State()
    image = State()
    price = State()
    confirm = State()


class CategoryState(StatesGroup):
    title = State()


class SosState(StatesGroup):
    question = State()
    submit = State()


class AnswerState(StatesGroup):
    answer = State()
    submit = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
   markup = ReplyKeyboardMarkup(resize_keyboard=True)

   markup.row(user_message, admin_message)

   await message.answer('''Привет! 
 Я бот-магазин по подаже товаров любой категории.

 Чтобы перейти в каталог и выбрать приглянувшиеся товары возпользуйтесь командой /menu.
 Пополнить счет можно через Яндекс.кассу, Сбербанк или Qiwi.
 Возникли вопросы? Не проблема! Команда /sos поможет связаться с админами, которые постараются как можно быстрее откликнуться.
 Заказать похожего бота? Свяжитесь с разработчиком <a href="#">Имя Фамилия</a>
   ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
   cid = message.chat.id
   if cid in ADMINS:
       ADMINS.remove(cid)

   await message.answer('Включен пользовательский режим.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
   cid = message.chat.id
   if cid not in ADMINS:
       ADMINS.append(cid)

   await message.answer('Включен админский режим.', reply_markup=ReplyKeyboardRemove())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
