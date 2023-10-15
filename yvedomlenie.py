import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

from main import TOKEN
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

cb = CallbackData('post', 'id', 'action')
button = types.InlineKeyboardButton(
    text='like',
    callback_data=cb.new(id=5, action='like'))

keyboard = types.InlineKeyboardMarkup().add(button)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.message):
    await message.answer("нажми на кнопку",reply_markup=keyboard)


@dp.callback_query_handler(cb.filter())
async def callback(call: types.CallbackQuery, callback_data: dict):
    post_id = callback_data['id']
    action = callback_data['action']
    if action == 'like':
        await call.message.edit_text('ты лайкнул пост'.format(post_id))
        await call.answer(text='ты лайкнул что хотел',show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)