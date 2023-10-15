import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardRemove
from aiogram.utils import executor
from keyboards import kb1, kb3, kb4, kb5, inlinekb1
from main import TOKEN
API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.reply('Привет', reply_markup=kb5)


@dp.message_handler(commands=['rm'])
async def rm(message: types.Message):
    await message.reply('убираем клавиатуру', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['in'])
async def inl(message: types.Message):
    await message.reply('инлайн', reply_markup=inlinekb1)


@dp.callback_query_handler(text="button1")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'нажата кнопка')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
