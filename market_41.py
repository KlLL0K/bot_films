import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, AdminFilter
from aiogram.types import ParseMode, BotCommand, BotCommandScopeDefault, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from main import TOKEN
from filters import IsAdminFilter
API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_menu():
    menu_kb = InlineKeyboardMarkup(roe_width=2)
    pizza_button = InlineKeyboardButton(text="Pizza🍕", callback_data='pizza_cat')
    snack_button = InlineKeyboardButton(text="Snack🍟", callback_data='snacks_cat')
    menu_kb.insert(pizza_button)
    menu_kb.insert(snack_button)
    return menu_kb
# ================================================================


@dp.message_handler(commands='menu')
async def menu_bot(message: types.Message):
    await message.answer("добро пожаловать в компанию дставки",reply_markup=get_menu())


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('menu', "Вывести меню"),
            BotCommand('help', "Помощь"),
            BotCommand('support', "поддержка")
        ],
        scope=BotCommandScopeDefault()
    )


@dp.message_handler(AdminFilter(), CommandStart())
async def admin_start(message: types.Message):
    await message.reply('команнды установленны')
    await set_default_commands(message.bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)