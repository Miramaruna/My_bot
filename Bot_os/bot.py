
# sqlite3

import sqlite3

# aiogram

import asyncio, logging, random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# config

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
admin_id = 5626265763

connection = sqlite3.connect("Mana.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fist_name VARCHAR(30),
    last_name VARCHAR(30),
    age INTEGER DEFAULT NULL,
    is_primium BOOLEAN
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    first_name VARCHAR(30)
    )
""")

# buttons

button_start = [
    [KeyboardButton(text='/play'), KeyboardButton(text='/info')],
    [KeyboardButton(text='/help'), KeyboardButton(text='register')],
    [KeyboardButton(text='Профиль')]
]

button_play = [
    [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3')]
]

button_info = [
    [KeyboardButton(text='geeks')]
]

keyboard_play = ReplyKeyboardMarkup(keyboard=button_play, resize_keyboard=True)
keyboard_start = ReplyKeyboardMarkup(keyboard=button_start,resize_keyboard=True)
keyboard_info = ReplyKeyboardMarkup(keyboard=button_info,resize_keyboard=True)

# Version = 2.1.4
# home Replit
# UptimeRobot

# programm

@dp.message(Command("start"))
async def start_bot(message: Message):
    await message.reply(f"Привет {message.from_user.first_name}!\nЭто бот мируни🧑‍💻\nТут все команды этого бота📁\nИграть🤠 - /play\nПерезапуск бота💊 - /start\nПомощь😭 - /help\nИнформация - /info🤔", reply_markup=keyboard_start)

@dp.message(F.text == "register")
async def start_bot(message: Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    users = cursor.fetchall()
    if users == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",(message.from_user.id, message.from_user.first_name, message.from_user.last_name, 12, message.from_user.is_premium))
        connection.commit()
    await message.reply("Успешно выполнено!😄")

@dp.message(Command("add_admin"))
async def add_task(message: Message):
    await message.answer("Введите код проверки:")

    @dp.message(F.text)
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

@dp.message(Command("help"))
async def help(message: Message):
    await message.reply("Привет помочь?\nКоманда старта📍 - /start\nИнформация🤔 - /info \nЕсли нужна помощь обращяйся по это команде😄 - /help\nПрописные команды без слеша ниже\nПрофиль🧩, geeks🕵, register💻", reply_markup=keyboard_start)

@dp.message(Command("info"))
async def info(message: Message):
    await message.reply("Привет!✋\nЭто информация о моем боте\nМой бот обычные слова воспринимает как эхо тоесть он не будет повторять слова\nА будет писать значение по умолчанию как (pon)\nНа этом у меня все!🤓\nУдачи!\n/start \nVersion == 2.1.5💫", reply_markup=keyboard_info)

@dp.message(F.text == "geeks")
async def info(message: Message):
    await message.answer('Научился я этому в учебном месте GEEKS это хорошое место для изучения программирования а также других сфер \nКак дизайн программирования для телефона и т.д\n/start', reply_markup=keyboard_start)

@dp.message(F.text == "Профиль")
async def info_profile(message : Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    user_id = cursor.fetchall()
    await message.reply(f"Имя - {message.from_user.first_name},\nФамилия - {message.from_user.last_name},\nid - {message.from_user.id},\nНаличие админки - {user_id}")

# # @dp.message(F.text == "users")
# async def users(message: Message):
#     cursor.execute(f"SELECT fist_name, id FROM users")
#     users = cursor.fetchall()
#     if message.from_user.id == admin_id:
#         await bot.send_message(admin_id ,f"список всех пользователей: \n{users}")
#     else:
#         await message.reply("Недастаточно прав 😂")

@dp.message(F.text == "users")
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
    
@dp.message(Command("play"))
async def play_bot(message: Message):
    await message.reply("Привет✋ я загадал число от 1 до 3 отгадай число!🤔")
    keyboard = ReplyKeyboardBuilder()
    for i in range(1,4):
        keyboard.add(KeyboardButton(text=f'{i}'))
    await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))    

@dp.message(F.text == '1')
async def odin(message: Message):
    if 1 == random.randint(1,3):
        await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Ты выйграл!😄\n/start", reply_markup=keyboard_play)
    else:
        await message.answer_photo(photo="https://media.makeameme.org/created sorry-you-lose.jpg", caption="Ты проиграл!😢\n/start", reply_markup=keyboard_play)
        
@dp.message(F.text == '2')
async def dva(message: Message):
    if 2 == random.randint(1,3):
        await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Ты выйграл!😄\n/start", reply_markup=keyboard_play)
    else:
        await message.answer_photo(photo="https://media.makeameme.org/created/sorry-you-lose.jpg", caption="Ты проиграл!😢\n/start", reply_markup=keyboard_play)

@dp.message(F.text == '3')
async def tri(message: Message):
    if 3 == random.randint(1,3):
        await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg", caption="Ты выйграл!😄\n/start", reply_markup=keyboard_play)
    else:
        await message.answer_photo(photo="https://media.makeameme.org/created/sorry-you-lose.jpg", caption="Ты проиграл!😢\n/start", reply_markup=keyboard_play)

# @dp.message()
async def echo(message: Message):
    await message.answer("pon")

async def main():
    await dp.start_polling(bot)

# start

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

connection.close()

# @dp.message(Command('play'))
# async def numbers(message: Message):
#     keyboard = ReplyKeyboardBuilder()
#     for i in range(1,4):
#         keyboard.add(KeyboardButton(text=f'{i}'))
#     keyboard.adjust(2)
#     await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))