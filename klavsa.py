from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_inline_keyboard():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("Доступ к файлам с лекций направление - ИГРЫ", url="https://drive.google.com/drive/folders/16Nt4bLyv8vylFV1a1OuGaS6xSYtc8U-h")
    btn2 = InlineKeyboardButton("Доступ к файлам с лекций направление - БОТЫ", url="https://drive.google.com/open?id=1Rwspj-mkkXWNhZXHXCcKRn8U8BKYIIE2&usp=drive_fs")
    markup.add(btn1)
    markup.add(btn2)


    return markup