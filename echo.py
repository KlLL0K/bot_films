import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

TOKEN = '2029153739:AAGJdqJ0eW-Qs03xwYBXhWzBY90L1AS6gE0'

WEBHOOK_HOST = 'https://d6df-95-181-28-151.ngrok-free.app'
WEBHOOK_PATH = '/2VTqDmrcqxRzhumbaf47q2eLPEK_5MhtdCAgkNH3PvRuGxzBF'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


WEBAPP_HOST = 'localhost'
WEBHOOK_PORT = 8000

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutt down')
    await bot.delete_webhook()
    logging.warning('Bye')

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBHOOK_PORT
    )