import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import aiogram.utils.markdown as fmt
from aiogram.utils import exceptions
from loguru import logger
from main import TOKEN
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)

@dp.message_handler(text="Привет")
async def cmd_test1(message: types.Message):
    await message.reply(f'привет <i>{message.from_user.username}</i>')


@dp.message_handler(text="Пока")
async def cmd_test2(message: types.Message):
    await message.reply(f'пока *{message.from_user.username}*')


@dp.message_handler(text='Ping')
async def cmd_test3(message: types.Message):
   await message.answer(
       fmt.text(
           fmt.text(fmt.hunderline("Яблоки"), ", вес 1 кг."),
           fmt.text("Старая цена:", fmt.hstrikethrough(50), "рублей"),
           fmt.text("Новая цена:", fmt.hbold(25), "рублей"),
           sep="\n"
       ), parse_mode="HTML"
   )


@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def cmd_test4(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
    await message.document.download()


@dp.message_handler(content_types="photo")
async def content_type_example(msg:types.Message):
    await msg.answer('лайк')


@dp.errors_handler(exeptio=exceptions.BotBlocked)
async def bot_blocked(update: types.Update, error: exceptions.BotBlocked):
    logger.exception(f"бот блокирован юзером")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)