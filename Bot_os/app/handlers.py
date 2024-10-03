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

class Calculator(StatesGroup):
    num2 = State()
    num = State()
    snak = State()

@router.message(F.text.in_({'Калькулятор', 'калькулятор'}))
async def calculate(message: Message, state: FSMContext):
    await message.answer("Введите первое число:")
    await state.set_state(Calculator.num)
    await message.delete()

@router.message(Calculator.num)
async def num1(message: Message, state: FSMContext):
    global num
    num = int(message.text)
    await message.answer("Введите второе число:")
    await state.set_state(Calculator.num2)

@router.message(Calculator.num2)
async def snaki(message: Message, state: FSMContext):
    global num, num2
    num2 = int(message.text)
    await message.answer("Введите знак:")
    await state.set_state(Calculator.snak)

@router.message(Calculator.snak)
async def vych(message: Message, state: FSMContext):
    global num, num2
    snak = message.text
    if snak == '-':
        otvet = num - num2
        await message.answer(f"Ответ - {otvet}")
        await state.clear()
    if snak == '+':
        otvet = num + num2
        await message.answer(f"Ответ - {otvet}")
        await state.clear()
    if snak == '*':
        otvet = num * num2
        await message.answer(f"Ответ - {otvet}")
        await state.clear()
    if snak == '/':
        otvet = num / num2
        await message.answer(f"Ответ - {otvet}")
        await state.clear()

@router.message(F.text == "register")
async def start_bot(message: Message):
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
    users = cursor.fetchall()
    if users == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",(message.from_user.id, message.from_user.first_name, 0, 500, None, None, None))
        connection.commit()
        await message.reply("Регистрация прошла успешно прошла успешно!👌")
        await message.reply(f"Вы были зарегистрированы под именем {message.from_user.id}")
    else:
        await message.reply("Аккаунт существует😉")
    await message.reply("Успешно выполнено!😄")

@router.message(Command("help"))
async def help(message: Message):
    await message.reply("Привет помочь?\nКоманда старта📍 - /start\nИнформация🤔 - /info \nЕсли нужна помощь обращяйся по это команде😄 - /help\nПрописные команды ниже\nПрофиль🧩\n geeks🕵\n register💻\n копать💰\n /transfer📲\n Ферма🔫\n Инвентарь📁\n /shop🏪\n/kazino🎰", reply_markup=keyboard_start) 

@router.message(Command("commands"))
async def commands(message: Message):
    await message.answer("/start\n/info\n/help\ngeeks\nregister\n/play\n/профиль\nкопать\nФерма\n/transfer\nИнвентарь\n/shop\n/kazino\n/ban\n/delete\n/ban_admin\n/transfer\n/передача\nusers\nкалькулятор")

@router.message(Command("info"))
async def info(message: Message):
    await message.reply("Привет!✋\nЭто информация о моем боте\nМой бот обычные слова воспринимает как эхо тоесть он не будет повторять слова\nА будет писать значение по умолчанию как (pon)\nНа этом у меня все!🤓\nУдачи!\n/start \nVersion == 2.2.0💫", reply_markup=keyboard_info) 

@router.message(F.text == "geeks")
async def info(message: Message):
    await message.answer('Научился я этому в учебном месте GEEKS это хорошое место для изучения программирования а также других сфер \nКак дизайн программирования для телефона и т.д\n/start', reply_markup=keyboard_start) 

@router.message(F.text == "профиль")
async def info_profile(message : Message):
    cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    u = cursor.fetchone()
    cursor.execute(f"SELECT wins FROM users WHERE user_id = {message.from_user.id}")
    w = cursor.fetchone()
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {message.from_user.id}")
    m = cursor.fetchone()
    connection.commit()
    wins = w[0]
    money = m[0]
    if u is None:
        user_id = None
    else:
        user_id = u[0]
    await message.reply(f"Имя - {message.from_user.first_name},\nid - {message.from_user.id},\nКоличество побед - {wins},\nДеньги💵 - {money},\nНаличие админки🤗 - {user_id}") 

@router.message(F.text == "users")
async def users(message: Message):
    cursor.execute(f"SELECT name, user_id, cash FROM users")
    useri = cursor.fetchall()
    connection.commit()
    if useri:
        response = "список всех пользователей:\n"
        for user_id, name, cash in useri:
            users = useri
            response += f"id - {user_id}, name - {name}, cash-{cash}\n"
    await message.reply(f"{response}")

class Delete(StatesGroup):
    id = State()

@router.message(Command("delete"))
async def delete(message: Message, state: FSMContext):
    await message.reply("Введите ID пользователя чтоб удалить его😨")
    await state.set_state(Delete.id) 

    @router.message(Delete.id)
    async def delete_accept(message: Message, state: FSMContext):
            cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
            admin = cursor.fetchall()
            connection.commit()
            try:
                if admin != []:
                    cursor.execute("DELETE FROM users WHERE user_id = ?", (message.text,))
                    connection.commit()
                    await message.reply("Удаление прошло успешно!😢")
                    await message.reply("/start")
                    await state.clear()
                else:
                    await message.reply("Недастаточно прав 😂")
                    await message.reply("/start")
                    await state.clear()
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

        await bot.send_message(receiver_id, f'Вам наслено {amount}')

        connection.commit()
        await message.reply("Перевод выполнен успешно")

    except Exception as e:
        connection.rollback()
        await message.reply(f"Ошибка: {e}")

@router.message(Command('передача'))
async def transfer_pol(message: Message):
    if message.from_user.id == admin:
        try:
            args = message.text.split()
            if len(args) < 3:
                raise ValueError("Неверный формат команды. Используйте: /transfer <id получателя> <сумма> Пример /передача id пользователя 100")

            receiver_id = int(args[1])
            amount = float(args[2])

            cursor.execute("SELECT cash FROM users WHERE user_id = ?", (message.from_user.id,))
            sender_cash = cursor.fetchone()
            s = sender_cash[0]

            if sender_cash is None:
                raise ValueError("Пользователь-отправитель не найден")

            cursor.execute("UPDATE users SET cash = cash + ? WHERE user_id = ?", (amount, receiver_id))

            await bot.send_message(receiver_id, f'Вам наслено {amount}')

            connection.commit()
            await message.reply("Перевод выполнен успешно")
            print(f"Пользователь с ID {message.from_user.id} использовал чит!")

        except Exception as e:
            connection.rollback()
            await message.reply(f"Ошибка: {e}")
            print(e)

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
        s = cursor.fetchone()
        cursor.execute(F"SELECT lvl FROM farm WHERE user_id = {message.from_user.id}")
        l = cursor.fetchone()
        connection.commit()
        size = s[0]
        lvl = l[0]
        await message.reply(f"--Ферма--\nЛюди - {size}\nlvl - {lvl}", reply_markup=arm_kb)

@router.callback_query(F.data == 'add')
async def add(callback: CallbackQuery):
    await callback.answer("Выполнение")
    acc = await accept(callback.from_user.id)
    if acc == True:
        await callback.message.answer("50 Людей добавлено в ферму✅")
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
    if result > 500:
        acc = True
    else:
        acc = False
    return acc

@router.message(F.text.in_({'Инвентарь', 'инвентарь', 'bydtynfhm'}))
async def inven(message: Message):
    cursor.execute(f"SELECT phone FROM users WHERE user_id = {message.from_user.id}")
    p = cursor.fetchone()
    phone = p[0]
    cursor.execute(f"SELECT car FROM users WHERE user_id = {message.from_user.id}")
    c = cursor.fetchone()
    car = c[0]
    cursor.execute(f"SELECT house FROM users WHERE user_id = {message.from_user.id}")
    h = cursor.fetchone()
    house = h[0]
    connection.commit()
    await message.answer(f"Инвентарь:\nМашина🚗 - {car}\nТелефон📱 - {phone}\nДом🏠 - {house}")

@router.message(Command('shop'))
async def shop(message: Message):
    await message.answer(f"Добро пожаловать в магазин🏪", reply_markup=shop_kb)

@router.message(F.text == 'Машины')
async def car(message: Message):
    await message.answer('Какую марку желаете купить?🪇', reply_markup=car_kb)

class Car(StatesGroup):
    num = State()

@router.message(F.text == 'BMW')
async def car(message: Message, state: FSMContext):
    await message.reply("BMW BMW M5 (G30) - 104K. 1\nBMW 7 Series (G11) - 87K. 2\nBMW iX (I20) - 84K. 3\nBMW X7 (G07) - 75K. 4\nBMW M4 (G82) - 73K. 5\nBMW M3 (G80) - 73K. 6\nBMW 6 Series Gran Turismo (G32) - 65K. 7\nBMW X6 (G06) - 65K. 8\nBMW M2 (G87) - 62K. 9\nBMW X5 (G05) - 61K. 10\nBMW i4 (G26) - 55K. 11\nBMW 5 Series (G30) - 54K. 12\nBMW X4 (G02) - 52K. 13\nBMW Z4 (G29) - 49K. 14\nBMW X3 (G01) - 45K. 15\nBMW X2 (F39) - 44K. 16\nBMW 4 Series Coupe (G22) - 46K. 17\nBMW 3 Series (G20) - 42K. 18\nBMW X1 (U11) - 42K. 19\nBMW 2 Series Coupe (G42) - 40K. 20\n\nЧтоб купить напишите нужное число после цены\nотмена - отмена")
    await state.set_state(Car.num)

    @router.message(Car.num, F.content_type == ContentType.TEXT)
    async def buy_car(message: Message, state: FSMContext):
        if message.text != 'отмена':
            acc = await accept_car(message.text, message.from_user.id)
            if acc == True:
                cursor.execute(f"SELECT name FROM car WHERE id = {message.text}")
                n = cursor.fetchone()
                name = n[0]
                await get_car(message.text, message.from_user.id)
                await message.answer(f"Машина {name} успешно куплена!🚘")
                await state.clear()
            else:
                await message.answer('Не достаточно денег📉')
                await state.clear()
        else:
                await message.answer("Отмена!✅")
                await state.clear()

@router.message(F.text == 'Mercedes')
async def car(message: Message, state: FSMContext):
    await message.answer("Mercedes-AMG One - 2.7M.21\nMercedes-AMG GT Black Series - 325K.22\nMercedes-AMG G 63 4x4² - 250K.23\nMercedes-Maybach S 680 4MATIC - 230K.24\nMercedes-AMG S 63 E PERFORMANCE - 180K.25\nMercedes-Maybach GLS 600 4MATIC - 170K.26\nMercedes-Benz S-Class S 580 4MATIC - 120K.27\nMercedes-Benz GLE Coupe AMG 53 - 120K.28\nMercedes-Benz G-Class G 550 - 110K.29\nMercedes-AMG E 63 S 4MATIC+ - 107K.30\nMercedes-Benz EQS 580 4MATIC - 105K.31\nMercedes-Benz GLS 450 4MATIC - 100K.32\nMercedes-AMG CLS 53 4MATIC+ - 95K.33\nMercedes-Benz GLE 450 4MATIC - 76K.34\nMercedes-Benz E-Class E 450 4MATIC - 70K.35\nMercedes-Benz GLC 300 4MATIC - 55K.36\nnMercedes-AMG CLA 45 4MATIC+ - 55K.37\nMercedes-Benz C-Class C 300 - 45K.38\nMercedes-Benz A-Class A 220 - 35K.39\nMercedes-Benz GLA 250 - 40K.40\nЧтоб купить напишите нужное число после цены\n!!!!Цены в долларх!!!\n1доллар - 1000\nотмена - отмена")
    await state.set_state(Car.num)

    @router.message(Car.num, F.content_type == ContentType.TEXT)
    async def buy_car(message: Message, state: FSMContext):
        if message.text != 'отмена':
            acc = await accept_car(message.text, message.from_user.id)
            if acc == True:
                cursor.execute(f"SELECT name FROM car WHERE id = {message.text}")
                n = cursor.fetchone()
                name = n[0]
                await get_car(message.text, message.from_user.id)
                await message.answer(f"Машина {name} успешно куплена!🚘")
                await state.clear()
            else:
                await message.answer('Не достаточно денег📉')
                await state.clear()
        else:
                await message.answer("Отмена!✅")
                await state.clear()

async def get_car(idi, idi2):
    cursor.execute(f"SELECT name FROM car WHERE id = {idi}")
    n = cursor.fetchone()
    name = n[0]
    cursor.execute(f"SELECT price FROM car WHERE id = {idi}")
    p = cursor.fetchone()
    price = p[0]
    cursor.execute(f"UPDATE users SET car = ? WHERE user_id = ?", (name, idi2))
    cursor.execute(f'UPDATE users SET cash = cash - ? WHERE user_id = ?', (price, idi2))
    connection.commit()

async def accept_car(idi, idi2):
    cursor.execute(f"SELECT price FROM car WHERE id = {idi}")
    p = cursor.fetchone()
    price = p[0]
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {idi2}")
    c = cursor.fetchone()
    cash = c[0]
    connection.commit()
    if cash >= price:
        acc = True
    else:
        acc = False
    return acc

class Phone(StatesGroup):
    num = State()

@router.message(F.text == "Телефоны")
async def phone(message: Message, state:FSMContext):
    await message.reply("Телефоны:\niPhone 15 Pro Max - 40k.1\nSamsung Galaxy S24 Ultra - 40k.2\nGoogle Pixel 8 Pro - 39k.3\nHuawei Mate 60 Pro - 38k.4\nSony Xperia 1 V - 38k.6\nOnePlus 12 Pro - 37k.7\nXiaomi 14 Pro - 37k.8/nOppo Find X6 Pro - 37k.9\nVivo X100 Pro - 36k.10\nAsus ROG Phone 7 Ultimate - 36k.11\nMotorola Edge 40 Pro - 35k.12\nRealme GT5 Pro - 35k.13\nHonor Magic 6 Pro - 34k.14\\nZTE Axon 50 Ultra - 34k.15\nNubia Red Magic 8 Pro - 34k.16\niPhone 15 - 33k.17\nSamsung Galaxy S24 - 33k.18\nGoogle Pixel 8 - 33k.19\nXiaomi 14 - 32k.20\nOnePlus 12 - 32k.21\nЧтоб купить напишите нужное число после цены\nотмена - отмена")
    await state.set_state(Phone.num)

@router.message(Phone.num)
async def buy_phone(message: Message, state:FSMContext):
        if message.text != 'отмена':
            accepted = await accept_phone(message.text, message.from_user.id)
            if accepted == True:
                cursor.execute(f"SELECT name_phone FROM phone WHERE id = {message.text}")
                n = cursor.fetchone()
                name = n[0]
                await get_phone(message.text, message.from_user.id)
                await message.answer(f"Телефон {name}, успешно куплен!📱")
                await state.clear()
            elif accepted == False:
                await message.answer('Не достаточно денег📉')
                await state.clear()
        else:
                await message.answer("Отмена!✅")
                await state.clear()

async def get_phone(idi, idi2):
    cursor.execute(f"SELECT name_phone FROM phone WHERE id = {idi}")
    n = cursor.fetchone()
    name = n[0]
    cursor.execute(f"SELECT price FROM phone WHERE id = {idi}")
    p = cursor.fetchone()
    price = p[0]
    cursor.execute(f"UPDATE users SET phone = ? WHERE user_id = ?", (name, idi2))
    cursor.execute(f'UPDATE users SET cash = cash - ? WHERE user_id = ?', (price, idi2))
    connection.commit()

async def accept_phone(idi, idi2):
    cursor.execute(f"SELECT price FROM phone WHERE id = {idi}")
    p = cursor.fetchone()
    price = p[0]
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {idi2}")
    c = cursor.fetchone()
    cash = c[0]
    if cash > price:
        acc = True
    else:
        acc = False
    return acc

class House(StatesGroup):
    num = State()

@router.message(F.text == 'Дома')
async def house(message: Message, state: FSMContext):
    await message.answer("Вилла - 5M. 1\nПоместье - 10M. 2\nКоттедж - 1M. 3\nДуплекс - 600K. 4\nТаунхаус - 800K. 5\nЧастный дом - 700K. 6\nШале - 1.5M. 7\nКвартира в многоквартирном доме - 500K. 8\nЛофт - 700K. 9\nСтудия - 300K. 10\nМодульный дом - 400K. 11\nКонтейнер - 150K. 12\nБунгало - 600K. 13\nПентхаус - 3M. 14\nКабинка - 100K. 15\nБарак - 50K. 16\nКоробка - 30K. 17\nЧтоб купить напишите нужное число после цены\nотмена - отмена")
    await state.set_state(House.num)

@router.message(House.num)
async def house_buy(message: Message, state: FSMContext):
    if message.text != 'отмена':
        accepted = await accept_house(message.text, message.from_user.id)
        if accepted == True:
            cursor.execute(f"SELECT name FROM house WHERE id = {message.text}")
            n = cursor.fetchone()
            name = n[0]
            await get_house(message.text, message.from_user.id)
            await message.answer(f"Дом {name}, успешно куплен!🏠")
            await state.clear()
        elif accepted == False:
            await message.answer('Не достаточно денег📉')
            await state.clear()
    else:
        await message.answer("Отмена!✅")
        await state.clear()

async def get_house(idi, idi2):
    cursor.execute(f"SELECT name FROM house WHERE id = {idi}")
    n = cursor.fetchone()
    name = n[0]
    cursor.execute(f"SELECT price FROM house WHERE id = {idi}")
    p = cursor.fetchone()
    price = p[0]
    cursor.execute(f"UPDATE users SET house = ? WHERE user_id = ?", (name, idi2))
    cursor.execute(f'UPDATE users SET cash = cash - ? WHERE user_id = ?', (price, idi2))
    connection.commit()

async def accept_house(idi, idi2):
    cursor.execute(f"SELECT price FROM house WHERE id = {idi}")
    p = cursor.fetchone()
    price = p[0]
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {idi2}")
    c = cursor.fetchone()
    cash = c[0]
    if cash > price:
        acc = True
    else:
        acc = False
    return acc

class Ban(StatesGroup):
    id = State()

@router.message(Command('ban'))
async def ban(message: Message, state: FSMContext):
    if message.from_user.id == admin:
        await message.answer("Напишите айди🪪:")
        await state.set_state(Ban.id)
    else:
        await message.reply('Ты не владелец!❌')

    @router.message(Ban.id)
    async def ban_id(message: Message, state: FSMContext):
        await bot.ban_chat_member(message.text, message.text, time.ctime)
        await state.clear()

@router.message(Command('ban_admin'))
async def ban_admin(message: Message, state:FSMContext):
    if message.from_user.id == admin:
        await message.answer("Введите ID админа для удаления🪪:")
        await state.set_state(Ban.id)
    else:
        await message.reply("У вас не доступа!❌")

    @router.message(Ban.id)
    async def ban_admin_True(message: Message, state: FSMContext):
        cursor.execute(f"DELETE FROM admin WHERE user_id = {message.text}")
        connection.commit()
        await message.reply("Удаление прошло успешно!✅")
        await state.clear()

class Kazino(StatesGroup):
    stavka = State()

@router.message(Command('kazino'))
async def kazino(message: Message, state: FSMContext):
    await message.answer("Введите свою ставу💵:")
    await state.set_state(Kazino.stavka)

@router.message(Kazino.stavka)
async def winorlos(message: Message, state:FSMContext):
    stavka = int(message.text)
    vygrysh = 3
    ran = random.randint(1,3)
    acc = accept_kazino(stavka, message.from_user.id)
    if acc == True:
        if ran == vygrysh:
            stavka = stavka * 2
            await message.answer(f"Вы выйграли - {stavka}!🤑")
            cursor.execute(f"UPDATE users SET cash = cahs + ? WHERE user_id = ?", (stavka, message.from_user.id))
            connection.commit()
            await state.clear()
        else:
            await message.answer("Вы проиграли!😭")
            cursor.execute(f"UPDATE users SET cash = cash - ? WHERE user_id = ?", (stavka, message.from_user.id))
            connection.commit()
            await state.clear()
    else:
        await message.answer("Не достаточно денег📉")

async def accept_kazino(stavka, idi2):
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {idi2}")
    c = cursor.fetchone()
    cash = c[0]
    if cash >= stavka:
        acc = True
    else: 
        acc = False

@router.message(Command("play"))
async def play_bot(message: Message):
    await message.reply("Привет✋ я загадал число от 1 до 3 отгадай число!🤔")
    keyboard = ReplyKeyboardBuilder()
    for i in range(1,4):
        keyboard.add(KeyboardButton(text=f'{i}'))
    await message.answer("Выберите число: ", reply_markup=keyboard.as_markup(resize_keyboard=True))   

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