import asyncio
import datetime
import logging
from config import TOKEN
from aiogram import Bot, types , Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
CHAT_ID_STONILEND = 1120233842
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def create_inline_keyboard():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Доступ к файлам с лекций направление - ИГРЫ",
                                url="https://drive.google.com/drive/folders/16Nt4bLyv8vylFV1a1OuGaS6xSYtc8U-h")
    btn2 = InlineKeyboardButton("Доступ к файлам с лекций направление - БОТЫ",
                                url="https://drive.google.com/open?id=1Rwspj-mkkXWNhZXHXCcKRn8U8BKYIIE2&usp=drive_fs")

    markup.add(btn1, btn2)
    return markup

# @dp.message_handler(commands=["start"])
# async def echo_message(message: types.Message):
#     await message.reply(f"111")
#     await send_keyboard_periodicaly()

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    await send_keyboard_periodicaly()


async def send_keyboard_periodicaly():
    while True:
        now = datetime.datetime.now()
        print(now)
        if now.hour == 18 and now.minute == 35:
            markup = create_inline_keyboard()
            await bot.send_message(chat_id=CHAT_ID_STONILEND, text="получилось, алиллуя", reply_markup=markup)
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(10)




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_keyboard_periodicaly())
    executor.start_polling(dp, skip_updates=True)
import asyncio
import datetime
import logging
from config import TOKEN
from aiogram import Bot, types , Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, Inline