# sqlite3

import sqlite3, random, time, asyncio

# aiogram

from aiogram import F, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram import types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ContentType
from aiogram.exceptions import TelegramBadRequest

from app.keyboard import *
from app.BD import *
from bot import *

router = Router()
fm_t = False
chat_id = None
admin = 5626265763

@router.message(Command("start"))
async def start_bot(message: Message):
    await message.reply(f"Привет {message.from_user.first_name}!\nЭто бот мируни🧑‍💻\nТут все команды этого бота📁\nИграть🤠 - /play\nПерезапуск бота💊 - /start\nПомощь😭 - /help\nИнформация🤔 - /info,\nРегистрация😀 - registr,\nПользователи👨 - users,\nКоманды для админов - /help_admin", reply_markup=keyboard_start)
    await message.delete()

@router.message(Command("fake"))
async def fake(message: Message):
    players = [
        564646546, 'Bot', 4, 1000000
    ]
    cursor.execute("INSERT INTO users(user_id, name, wins, cash) VALUES(?, ?, ?, ?)", (players))
    connection.commit()

@router.message(F.text == "register")
async def start_bot(message: Message):
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
    users = cursor.fetchall()
    if users == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",(message.from_user.id, message.from_user.first_name, 0, 500))
        connection.commit()
        await message.reply("Регистрация прошла успешно прошла успешно!👌")
        await message.reply(f"Вы были зарегистрированы под именем {message.from_user.id}")
    else:
        await message.reply("Аккаунт существует😉")
    await message.reply("Успешно выполнено!😄")

@router.message(Command("help"))
async def help(message: Message):
    await message.reply("Привет помочь?\nКоманда старта📍 - /start\nИнформация🤔 - /info \nЕсли нужна помощь обращяйся по это команде😄 - /help\nПрописные команды ниже\nПрофиль🧩, geeks🕵, register💻, копать💰, /transfer📲, Ферма🔫", reply_markup=keyboard_start)

@router.message(Command("help_admin"))
async def help_admin(message: Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    admin = cursor.fetchall()
    if admin == []:
        await message.reply("Сперва админом стань!🤓")
        await message.delete()  
    elif admin != []:
        await message.reply("Вот все команды!😄", reply_markup=help_admin_keyboard)
        await message.delete()  

@router.message(Command("info"))
async def info(message: Message):
    await message.reply("Привет!✋\nЭто информация о моем боте\nМой бот обычные слова воспринимает как эхо тоесть он не будет повторять слова\nА будет писать значение по умолчанию как (pon)\nНа этом у меня все!🤓\nУдачи!\n/start \nVersion == 2.1.9💫", reply_markup=keyboard_info)
    await message.delete()  

@router.message(F.text == "geeks")
async def info(message: Message):
    await message.answer('Научился я этому в учебном месте GEEKS это хорошое место для изучения программирования а также других сфер \nКак дизайн программирования для телефона и т.д\n/start', reply_markup=keyboard_start)
    await message.delete()  

@router.message(F.text == "профиль")
async def info_profile(message : Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    user_id = cursor.fetchall()
    cursor.execute(f"SELECT wins FROM users WHERE user_id = {message.from_user.id}")
    wins = cursor.fetchall()
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {message.from_user.id}")
    money = cursor.fetchall()
    connection.commit()
    await message.reply(f"Имя - {message.from_user.first_name},\nid - {message.from_user.id},\nКоличество побед - {wins},\nДеньги💵 - {money},\nНаличие админки - {user_id}")
    await message.delete()  

@router.message(F.text == "users")
async def users(message: Message):
    cursor.execute(f"SELECT name, id FROM users")
    useri = cursor.fetchall()
    connection.commit()
    if useri:
        response = "список всех пользователей:\n"
        for user_id, users in useri:
            users = useri
            response += f"{user_id}. {users}\n"
    await message.reply(f"{response}")

@router.callback_query(F.data == 'delete')
async def delete_help(callback: CallbackQuery):
    await callback.answer("delete")
    await callback.message.edit_text("Просто нажми на это -> /delete")

@router.message(Command("delete"))
async def delete(message: Message, state: FSMContext):
    await message.reply("Введите ID пользователя чтоб удалить его")
    await message.delete()  

    @router.message(F.text)
    async def delete_accept(message: Message):
            cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
            admin = cursor.fetchall()
            connection.commit()
            try:
                if admin != []:
                    cursor.execute("DELETE FROM users WHERE user_id = ?", (message.text,))
                    connection.commit()
                    await message.reply("Удаление прошло успешно!😢")
                    await message.reply("/start")
                else:
                    await message.reply("Недастаточно прав 😂")
                    await message.reply("/start")
            except BaseException as e:
                await message.reply("Error")
                print(e)
                await message.reply("/start")

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID фота: {message.photo[-1].file_id}")

@router.message(F.text == 'копать')
async def kopat(message: Message):
        await message.reply(f"Вы заработали: 500💵")
        cursor.execute("UPDATE users SET cash = cash + ? WHERE user_id = ?", (500, message.from_user.id))
        connection.commit()

@router.message(Command('transfer'))
async def transfer_pol(message: Message):

    try:
        args = message.text.split()
        if len(args) < 3:
            raise ValueError("Неверный формат команды. Используйте: /transfer <id получателя> <сумма> Пример /transfer id пользователя 100")

        receiver_id = int(args[1])
        amount = float(args[2])

        cursor.execute("SELECT cash FROM users WHERE user_id = ?", (message.from_user.id,))
        sender_cash = cursor.fetchone()

        if sender_cash is None:
            raise ValueError("Пользователь-отправитель не найден")
        
        if sender_cash[0] < amount:
            raise ValueError("Недостаточно средств для перевода")

        cursor.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", (amount, message.from_user.id))
        cursor.execute("UPDATE users SET cash = cash + ? WHERE user_id = ?", (amount, receiver_id))

        connection.commit()
        await message.reply("Перевод выполнен успешно")

    except Exception as e:
        connection.rollback()
        await message.reply(f"Ошибка: {e}")

##Ферму с людьми поменять

@router.message(F.text.in_({"Ферма", "athvf", "ферма"}))
async def farm(message: Message):
    cursor.execute(f"SELECT user_id FROM farm WHERE user_id = {message.from_user.id}")
    us = cursor.fetchall()
    connection.commit()
    if us == []:
        await message.reply("Ферма создана⚔️")
        await create_farm(message.from_user.id)
    else:
        cursor.execute(f"SELECT size FROM farm WHERE user_id = {message.from_user.id}")
        size = cursor.fetchone()
        cursor.execute(F"SELECT lvl FROM farm WHERE user_id = {message.from_user.id}")
        lvl = cursor.fetchone()
        connection.commit()
        await message.reply(f"--Ферма--\nЛюди - {size}\nlvl - {lvl}", reply_markup=arm_kb)

@router.callback_query(F.data == 'add')
async def add(callback: CallbackQuery):
    await callback.answer("Выполнение")
    acc = await accept(callback.from_user.id)
    if acc == True:
        await callback.message.answer("100 Людей добавлено в ферму🟩")
        await add_people_farm(callback.from_user.id)
    else:
        await callback.message.answer("Не достаточно денег📉")

async def add_people_farm(idi):
        cursor.execute("UPDATE farm SET size = size + ? WHERE user_id = ?", (50, idi))
        cursor.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", (500, idi))
        connection.commit()

async def accept(idi):
    cursor.execute(F"SELECT cash FROM users WHERE user_id = {idi}")
    cash = cursor.fetchone()
    result = cash[0]
    connection.commit()
    if result > 0:
        acc = True
    else:
        acc = False
    return acc

@router.message(Command("play"))
async def play_bot(message: Message):
    await message.reply("Привет✋ я загадал число от 1 до 3 отгадай число!🤔")
    keyboard = ReplyKeyboardBuilder()
    for i in range(1,4):
        keyboard.add(KeyboardButton(text=f'{i}'))
    await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))
    await message.delete()    

    @router.message(F.text.in_(['1', '2', '3']))
    async def odin(message: Message):
        user_guess = int(message.text)
        correct_number = random.randint(1, 3)
        if user_guess == correct_number:
                cursor.execute('UPDATE users SET wins = wins + ? WHERE user_id = ?', (1, message.from_user.id))
                connection.commit()
                await message.answer_photo(photo="https://pic.vjshi.com/2023-04-20/e57c2237d4bf4f64928b0d20a8c33d53/online/puzzle.jpg?x-oss-process=style/w1440_h2880")
                await message.answer("Ты выйграл!😄\n/start")
        else:
            await message.answer_photo(photo="https://i.pinimg.com/600x315/60/a7/1f/60a71f48617c70eca2f990f374d1e848.jpg")
            await message.answer("Ты проиграл!😢\n/start")