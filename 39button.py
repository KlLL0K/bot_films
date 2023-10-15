import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from keyboards import kb1, kb3, kb4, kb5, ReplyKeyboardRemove, inline_kb1
from config import TOKEN
API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_command_2(message: types.Message):
   await message.reply("Отправляю все возможные кнопки", reply_markup=inline_kb_full)



@dp.message_handler(commands=['rm'])
async def rm(message: types.Message):
    await message.reply('Убираем клаву', reply_markup=ReplyKeyboardRemove())



# кнопка инлайн
@dp.message_handler(commands=['in'])
async def inl_kb(message: types.Message):
    await message.reply('Инлайн', reply_markup=inline_kb1)

#перехват кнопки
@dp.callback_query_handler(text='button1')
async def process_callback_button1(callback_query:types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "нажата кнопка!")



from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('Яндекс', url='https://www.yandex.ru'))



@dp.callback_query_handler(text='1')
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
   code = callback_query.data[-1]
   if code.isdigit():
       code = int(code)
   if code == 2:
       await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
   elif code == 5:
       await bot.answer_callback_query(
           callback_query.id,
           text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов', show_alert=True)
   else:
       await bot.answer_callback_query(callback_query.id)
   await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')











if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)