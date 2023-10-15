
from aiogram import Bot, Dispatcher, types
from main import TOKEN
from aiogram.dispatcher import filters, FSMContext
import logging
from aiogram.dispatcher.filters import BoundFilter
from main import ADMINS
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class IsAdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in ADMINS


IMAGE_REGEXP = r'https://.+?.(jpg|jpeg|png)'
dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(IsAdminFilter)
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def start_command(message: types.Message):
    welcome_text = "Привет"
    await message.answer(welcome_text)


@dp.message_handler(commands="set_state")
async def set_state(message: types.Message, state: FSMContext):
    await state.set_state('test_state')


@dp.message_handler(state='example_state')
async def state_example(msg: types.Message, state: FSMContext):
    await msg.answer('ой все')
    await state.finish()


@dp.message_handler(filters.Regexp(IMAGE_REGEXP))
async def regexp_example(msg: types.Message):
    await msg.answer('состояние установлено')
    await msg.answer("это пикча")


@dp.message_handler(hashtags='money')
async def hashteg_example(msg: types.Message):
    await msg.answer("круто")


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
