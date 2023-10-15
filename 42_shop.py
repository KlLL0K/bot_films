import logging
import random
import re
import time
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)
from aiogram import Bot, Dispatcher, executor, types
from main import TOKEN

API_TOKEN = TOKEN
from filt import IsAdminFilter

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

available_food_names = ['суши', 'спагетти', "хачапури"]  # state1
available_food_sizes = ['маленькую', "среднюю", "большую"]  # state2


class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()


@dp.message_handler(commands='start')
async def on_start(message: types.Message):
    await message.answer("привет")


async def food_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await message.answer("выберете блюдо", reply_markup=keyboard)
    await OrderFood.waiting_for_food_name.set()


async def food_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_names:
        await message.answer('выбери блюдо используя клавиатуру')
        return
    await state.update_data(chosen_food=message.text.lower())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    await message.answer('теперь выбери размер порции', reply_markup=keyboard)
    await OrderFood.next()


async def food_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_sizes:
        await message.answer('выбери размер порции используя клавиатуру')
        return
    user_data = await state.get_data()
    await message.answer(f"вы заказали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
                         f"Попробуйте теперь заказать напитки: /drinks", reply_markup=ReplyKeyboardRemove())
    await state.finish()


def register_handlers_food(dp: Dispatcher):
    dp.register_message_handler(food_start, commands='food', state='*')
    dp.register_message_handler(food_chosen, state='*')
    dp.register_message_handler(food_chosen, state=OrderFood.waiting_for_food_name)
    dp.register_message_handler(food_size_chosen, state=OrderFood.waiting_for_food_size)


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('выберете, что хотите заказать (/drinks) или блюда (/food).',
                         reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands='cancel', state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(on_start, commands='start', state='*')
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state='*')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
