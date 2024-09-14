# sqlite3

import sqlite3, random

# aiogram

from aiogram import F, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.keyboard import *
from pnj import *

router = Router()
connection = sqlite3.connect("Mana.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fist_name VARCHAR(30),
    last_name VARCHAR(30),
    age INTEGER DEFAULT NULL,
    is_primium BOOLEAN,
    wins INTEGER
    )
""")
connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    first_name VARCHAR(30)
    )
""")

@router.message(Command("start"))
async def start_bot(message: Message):
    await message.reply(f"Привет {message.from_user.first_name}!\nЭто бот мируни🧑‍💻\nТут все команды этого бота📁\nИграть🤠 - /play\nПерезапуск бота💊 - /start\nПомощь😭 - /help\nИнформация🤔 - /info,\nРегистрация😀 - registr,\nПользователи👨 - users,\nКоманды для админов - /help_admin", reply_markup=keyboard_start)

@router.message(F.text == "register")
async def start_bot(message: Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    users = cursor.fetchall()
    if users == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",(message.from_user.id, message.from_user.first_name, message.from_user.last_name, 12, message.from_user.is_premium, 0))
        connection.commit()
        await message.reply("Регистрация прошла успешно прошла успешно!👌")
    else:
        await message.reply("Аккаунт существует😉")
    await message.reply("Успешно выполнено!😄")

@router.message(Command("add_admin"))
async def add_task(message: Message):
    await message.answer("Введите код проверки:")

    @router.message(F.text)
    async def save_admin(message: Message):
        if message.text == 'bugi':
            cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
            pop = cursor.fetchall()
            connection.commit()
            if pop == []:
                cursor.execute(
                    "INSERT INTO admin (user_id, first_name) VALUES (?, ?)",
                    (message.from_user.id, message.from_user.first_name)
                )
                connection.commit()
                await message.reply("Авторизация прошла успешно!👌")
            else:
                await message.reply("Аккаунт существует😉")
            
        else:
            await message.reply("Код не правильный😡")
        await message.reply("Исполнено!🫡")
        connection.commit()

@router.message(Command("help"))
async def help(message: Message):
    await message.reply("Привет помочь?\nКоманда старта📍 - /start\nИнформация🤔 - /info \nЕсли нужна помощь обращяйся по это команде😄 - /help\nПрописные команды без слеша ниже\nПрофиль🧩, geeks🕵, register💻", reply_markup=keyboard_start)

@router.message(Command("help_admin"))
async def help_admin(message: Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    admin = cursor.fetchall()
    if admin == []:
        await message.reply("Сперва админом стань!🤓")
    elif admin != []:
        await message.reply("Вот все команды!😄", reply_markup=keyboard_help_admin)

@router.message(Command("info"))
async def info(message: Message):
    await message.reply("Привет!✋\nЭто информация о моем боте\nМой бот обычные слова воспринимает как эхо тоесть он не будет повторять слова\nА будет писать значение по умолчанию как (pon)\nНа этом у меня все!🤓\nУдачи!\n/start \nVersion == 2.1.6💫", reply_markup=keyboard_info)

@router.message(F.text == "geeks")
async def info(message: Message):
    await message.answer('Научился я этому в учебном месте GEEKS это хорошое место для изучения программирования а также других сфер \nКак дизайн программирования для телефона и т.д\n/start', reply_markup=keyboard_start)

@router.message(F.text == "Профиль")
async def info_profile(message : Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    user_id = cursor.fetchall()
    connection.commit()
    cursor.execute(f"SELECT wins FROM users WHERE id = {message.from_user.id}")
    wins = cursor.fetchall()
    connection.commit()
    await message.reply(f"Имя - {message.from_user.first_name},\nФамилия - {message.from_user.last_name},\nid - {message.from_user.id},\nКоличество побед - {wins},\nНаличие админки - {user_id}")

# # @router.message(F.text == "users")
# async def users(message: Message):
#     cursor.execute(f"SELECT fist_name, id FROM users")
#     users = cursor.fetchall()
#     if message.from_user.id == admin_id:
#         await bot.send_message(admin_id ,f"список всех пользователей: \n{users}")
#     else:
#         await message.reply("Недастаточно прав 😂")

@router.message(F.text == "users")
async def users(message: Message):
    cursor.execute(f"SELECT fist_name, id FROM users")
    useri = cursor.fetchall()
    connection.commit()
    if useri:
        response = "список всех пользователей:\n"
        for user_id, users in useri:
            users = useri
            response += f"{user_id}. {users}\n"
    await message.reply(f"{response}")

@router.message(Command("delete"))
async def delete(message: Message):
    await message.reply("Введите ID пользователя чтоб удалить его")

    @router.message(F.text)
    async def delete_accept(message: Message):
        cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
        admin = cursor.fetchall()
        try:
            if admin != []:
                cursor.execute(f"DELETE FROM users WHERE id = ?", (message.text))
                await message.reply("Удаление прошло успешно!😢")
            else:
                await message.reply("Недастаточно прав 😂")
        except BaseException as e:
            await message.reply("Error")
            print(e)

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID фота: {message.photo[-1].file_id}")
    
@router.message(Command("play"))
async def play_bot(message: Message):
    await message.reply("Привет✋ я загадал число от 1 до 3 отгадай число!🤔")
    keyboard = ReplyKeyboardBuilder()
    for i in range(1,4):
        keyboard.add(KeyboardButton(text=f'{i}'))
    await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))    

@router.message(F.text == '1')
async def odin(message: Message):
    if 1 == random.randint(1,3):
        cursor.execute(f"SELECT wins FROM users WHERE id = {message.from_user.id}")
        win = cursor.fetchall()
        if win:
            cursor.execute('UPDATE users SET wins = wins + ? WHERE id = ?', (1, message.from_user.id))
            connection.commit()
        await message.reply("Ты выйграл!😄\n/start")
    else:
        await message.reply("Ты проиграл!😢\n/start")
        
@router.message(F.text == '2')
async def dva(message: Message):
    if 2 == random.randint(1,3):
        cursor.execute(f"SELECT wins FROM users WHERE id = {message.from_user.id}")
        win = cursor.fetchall()
        if win:
            cursor.execute('UPDATE users SET wins = wins + ? WHERE id = ?', (1, message.from_user.id))
            connection.commit()
        await message.reply("Ты выйграл!😄\n/start")
    else:
        await message.reply("Ты проиграл!😢\n/start")

@router.message(F.text == '3')
async def tri(message: Message):
    if 3 == random.randint(1,3):
        cursor.execute(f"SELECT wins FROM users WHERE id = {message.from_user.id}")
        win = cursor.fetchall()
        if win:
            cursor.execute('UPDATE users SET wins = wins + ? WHERE id = ?', (1, message.from_user.id))
            connection.commit()
        await message.reply("Ты выйграл!😄\n/start")
    else:
        await message.reply("Ты проиграл!😢\n/start")

# @dp.message(Command('play'))
# async def numbers(message: Message):
#     keyboard = ReplyKeyboardBuilder()
#     for i in range(1,4):
#         keyboard.add(KeyboardButton(text=f'{i}'))
#     keyboard.adjust(2)
#     await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))