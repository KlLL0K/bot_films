import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, BotCommand, BotCommandScopeDefault
from aiogram.utils import executor
from main import TOKEN
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def set_default_commands(bot: bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('command_default1', 'стандартная команда 1'),
            BotCommand('command_default2', 'стандартная команда 2'),
            BotCommand('command_default2', 'стандартная команда 2'),
        ],
        scope=BotCommandScopeDefault(),
    )


@dp.message_handler(commands='command_default1')
async def user_start(message: types.Message):
    await message.answer(f"Бот запущен")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
