import asyncio
import logging
import io
import datetime
import re

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.utils.exceptions import BadRequest

from main import TOKEN
from aiogram.dispatcher.filters import Command
from filters import IsGroup, IsPrivate, AdminFilter

API_TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('set_photo', 'Установить фото в группе'),
        types.BotCommand('set_title', 'Установить название группы'),
        types.BotCommand('set_description', 'Установить описание группы'),
        types.BotCommand('ro', 'Режим Read Only'),
        types.BotCommand('unro', 'Отключить RO'),
        types.BotCommand('ban', 'Забанить пользователя'),
        types.BotCommand('unban', 'Разбанить пользователя'),
    ])


# @dp.message_handler()
# async def del_m(message: types.Message):
#     await bot.delete_message(message.chat.id, message.message_id)
@dp.message_handler(IsGroup(), Command('set_photo', prefixes='!/'), AdminFilter())
async def set_new_photo(message: types.Message):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_file = types.InputFile(path_or_bytesio=photo)
    await message.chat.set_photo(photo=input_file)


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def banned_member(message: types.Message):
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f'{message.left_chat_member.get_mention(as_html=True)} вышел из чата')
    elif message.from_user.id == (await bot.me).id:
        return
    else:
        await message.reply(
            f'{message.left_chat_member.full_name} был удален из чата пользователем {message.from_user.get_mention(as_html=True)}')


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def banned_member(message: types.Message):
    await message.reply(
        f'{message.left_chat_member.full_name}  был удален из чата пользователем {message.from_user.full_name}')


@dp.message_handler(IsGroup(), Command('set_title', prefixes='!/'), AdminFilter())
async def set_new_title(message: types.Message):
    source_message = message.reply_to_message
    title = source_message.text
    await message.chat.set_title(title=title)


@dp.message_handler(IsGroup(), Command('set_description', prefixes='!/'), AdminFilter())
async def set_new_description(message: types.Message):
    source_message = message.reply_to_message
    description = source_message.text
    await message.chat.set_description(description=description)


@dp.message_handler(IsGroup(), Command('ban', prefixes='!/'), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)
    await message.reply(f'Пользователь {member.full_name} был забанен')


@dp.message_handler(IsGroup(), Command('ban', prefixes='!/'), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)
    await message.reply(f'Пользователь {member.full_name} был забанен')


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    await message.reply(f'Привет {message.new_chat_members[0].full_name}')


@dp.message_handler(IsGroup(), Command('unban', prefixes='!/'), AdminFilter())
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.unban(user_id=member_id)
    await message.reply(f'Пользователь {member.full_name} был разбанен')
    service_message = await message.reply('Сообщение удалится через 5 секунд')
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()




@dp.message_handler(IsGroup(), Command('unro', prefixes='!/'), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    User_Allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_pin_messages=False,
        can_invite_users=True,
        can_change_info=False,
        can_add_web_page_previews=True,
    )
    await message.chat.restrict(user_id=member_id, permissions=User_Allowed, until_date=0)
    await message.reply(f'Пользователь {member.full_name} был разбанен')
    service_message = await message.reply('Сообщение удалится через 5 секунд')
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), Command('ro', prefixes='!/'), AdminFilter())
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    command_parse = re.compile(r'(!ro|/ro) ?(\d+)? ?([a-zA-Z ])+?')
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5
    else:
        time = int(time)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
    ReadOnlyPermission = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_pin_messages=False,
        can_invite_users=True,
        can_change_info=False,
        can_add_web_page_previews=False,
    )
    try:
        await bot.restrict_chat_member(chat_id, user_id=member_id, permissions=ReadOnlyPermission,
                                       until_date=until_date)
        await message.answer(
            f'Пользователю {member.get_mention(as_html=True)} запрещено писать на {time} минут по причине {comment}')
    except BadRequest:
        await message.answer('Пользователь является администратором')
        service_message = await message.reply('Сообщение удалится через 5 секунд')
        await asyncio.sleep(5)
        await message.delete()
        await service_message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
