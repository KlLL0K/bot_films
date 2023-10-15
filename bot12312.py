import logging
import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, types


API_TOKEN = '2029153739:AAGJdqJ0eW-Qs03xwYBXhWzBY90L1AS6gE0'


proxy_url = 'http://proxy.server:3128'

connector = aiohttp.TCPConnector(proxy_url=proxy_url)
aiohttp_session = aiohttp.ClientSession(connector=connector)
bot = Bot(token=API_TOKEN, client_session=aiohttp_session)


dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
   await message.answer('Вы ввели команду /start')
   print('hello')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start_polling(skip_updates=True))