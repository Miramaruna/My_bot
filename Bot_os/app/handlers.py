
import sqlite3, random, time, asyncio

from aiogram import F, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import ChatMemberUpdatedFilter

from aiogram import types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ContentType, ChatMemberUpdated
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ChatMemberStatus

from app.keyboard import *
from app.BD import *
from bot import *

router = Router()
fm_t = False
chat_id = None
admin = 5626265763

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

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
        await message.reply(f"Вы были зарегистрированы под именем {message.from_user.first_name}")
    else:
        await message.reply("Аккаунт существует😉")
    await message.reply("Успешно выполнено!😄")

@router.message(Command("help"))
async def help(message: Message):
    await message.reply("Привет помочь?\nКоманда старта📍 - /start\nИнформация🤔 - /info \nЕсли нужна помощь обращяйся по это команде😄 - /help\nПрописные команды ниже\nПрофиль🧩\n geeks🕵\n register💻\n копать💰\n /transfer📲\n Ферма🔫\n Инвентарь📁\n /shop🏪\n/kazino🎰\nдать 'число'\n удалить(сообщение)\n trading📈\n/start_game(крестики нолики)\nАрмия🪖\nВсе команды можно посмотреть введя команду '/commands'", reply_markup=keyboard_start) 

@router.message(Command("commands"))
async def commands(message: Message):
    await message.answer("/start\n/info\n/help\ngeeks\nregister\n/play\n/профиль\nкопать\nФерма\n/transfer\nИнвентарь\n/shop\n/kazino\n/ban\ndelete\n/ban_admin\n/передача\nusers\nкалькулятор\nArmy\nсражаться\nдать\nудалить\n/start_game\n/mailing\nadmin\n/add_admin\nstop")

@router.message(Command("info"))
async def info(message: Message):
    await message.reply("Привет!✋\nЭто информация о моем боте\nЯзык бота - python\nБД - Sqlite3\nБиблиотека - aiogram3\nVersion == 2.2.2💫", reply_markup=keyboard_info) 

@router.message(F.text == "geeks")
async def info(message: Message):
    await message.answer('Научился я этому в учебном месте GEEKS это хорошое место для изучения программирования а также других сфер \nКак дизайн программирования для телефона и т.д\n/start', reply_markup=keyboard_start) 

async def get_user_data(user_id):

    cursor.execute("SELECT name, wins, cash FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        return {'name': result[0], 'wins': result[1], 'cash': result[2]}
    return None

@router.message(F.text == "профиль")
async def info_profile(message : Message):
    user_id = message.from_user.id

    user_info = await get_user_data(user_id)

    if user_info:
        name = user_info['name']
        wins = user_info['wins']
        cash = user_info['cash']
    
    cursor.execute(F"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    a = cursor.fetchone()
    admin_id = a[0]

    if message.chat.type == 'private':
        await message.reply(f"Имя - {name},\nid - {message.from_user.id},\nКоличество побед - {wins},\nДеньги💵 - {cash},\nНаличие админки🤗 - {admin_id}")
    else:
        member = await message.chat.get_member(user_id)
        if member.status == ChatMemberStatus.MEMBER:
            role = "Обычный согрупник"
        elif member.status == ChatMemberStatus.ADMINISTRATOR:
            role = "Администратор"
        elif user_id == admin:
            role = 'Создатель бота'
        else:
            role = "Неизвестная роль"

        await message.reply(f"Имя - {name},\nid - {message.from_user.id},\nКоличество побед - {wins},\nДеньги💵 - {cash},\nНаличие админки🤗 - {admin_id},\nРоль в группе - {role}👥")

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
    await message.reply("Введите ID пользователя чтоб удалить его😨\nотмена - отмена")
    await state.set_state(Delete.id) 

    @router.message(Delete.id)
    async def delete_accept(message: Message, state: FSMContext):
            cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
            a = cursor.fetchone()
            admink = a[0]
            cursor.execute(f"SELECT user_id FROM users WHERE user_id = {message.text}")
            user = cursor.fetchone()
            connection.commit()
            try:
                if message.text != 'отмена':
                    if admink != []:
                        if user != []:
                            if int(message.text) != admin:
                                cursor.execute("DELETE FROM users WHERE user_id = ?", (message.text,))
                                connection.commit()
                                await message.reply("Удаление прошло успешно!😢")
                                await bot.send_message(admin, f"Пользователь - {message.text} удален админом - {admink}!❗️")
                                await state.clear()
                            else:
                                await message.answer("ТЫ слишком глупп удалить владельца бота😂")
                                await bot.send_message(admin, f"На вас пытались покушится пользователь с ID - {admink}🤦‍♂️")
                                await state.clear()
                        else:
                            await message.answer("Такого пользователя нету!🤦‍♂️")
                    else:
                        await message.reply("Недастаточно прав 😂")
                        await state.clear()
                else:
                    await message.answer("Отмена✅")
                    await state.clear()
            except BaseException as e:
                await message.reply("Error")
                print(e)

@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID фота: {message.photo[-1].file_id}")

@router.message(F.text == 'копать')
async def kopat(message: Message):
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
        p = cursor.fetchone()
        if p != None:
            await message.reply(f"Вы заработали: 500💵")
            cursor.execute("UPDATE users SET cash = cash + ? WHERE user_id = ?", (500, message.from_user.id))
            connection.commit()
        else:
            await message.answer("Зарегистрируйтесь чтоб можно было зарабатывать игровуй валюту!🙂")

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

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

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

################################################################################################################################################################
################################################################################################################################################################

@router.message(F.text.startswith('дать'))
async def give_currency(message: Message):
    if not message.reply_to_message:
        await message.reply("Вы должны ответить на сообщение пользователя, чтобы передать валюту.")
        return

    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Вы должны указать сумму. Пример: дать 100")
            return
        
        amount = int(parts[1])

        if amount <= 0:
            await message.reply("Сумма должна быть положительной.")
            return

    except ValueError:
        await message.reply("Некорректная сумма. Пример: дать 100")
        return

    from_user_id = message.from_user.id
    to_user_id = message.reply_to_message.from_user.id


    cursor.execute(F"SELECT cash FROM users WHERE user_id = {message.from_user.id}")
    c = cursor.fetchone()
    cash = c[0]
    if cash < amount:
        await message.reply("У вас недостаточно средств.")
        return


    cursor.execute(F"UPDATE users SET cash = cash - {-amount} WHERE user_id = {from_user_id}")
    cursor.execute(F"UPDATE users SET cash = cash + {amount} WHERE user_id = {to_user_id}")

    await message.reply(f"Вы передали {amount} игровой валюты пользователю {message.reply_to_message.from_user.full_name}.")
    await message.bot.send_message(
        to_user_id, f"Вам было передано {amount} игровой валюты от {message.from_user.full_name}."
    )
    connection.commit()

@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def on_bot_added_to_group(message: Message, event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        chat_id = event.chat.id
        await bot.send_message(chat_id, "Привет! Я бот. Спасибо за добавление в группу!")

@router.message(F.text == 'удалить')
async def delete_message_on_command(message: Message):
    member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.ADMINISTRATOR:
        if message.reply_to_message:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
            except Exception as e:
                await message.reply(f"Не удалось удалить сообщение: {e}")
        else:
            await message.reply("Вы должны ответить на сообщение, чтобы удалить его.")
    else:
        await message.answer('Стань админом сперва😒')

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

@router.message(F.text.in_({'Армия','армия','Army'}))
async def army(message: Message):
    cursor.execute(F"SELECT user_id FROM army WHERE user_id = {message.from_user.id}")
    u = cursor.fetchone()
    connection.commit
    if u == None:
        cursor.execute("INSERT INTO army(user_id, soldiers, cars, tanks) VALUES(?, ?, ?, ?)", (message.from_user.id, 10, 2, 1))
        connection.commit()
        await message.answer("Армия создана!🪖")
    else:
        cursor.execute(f"SELECT soldiers FROM army WHERE user_id = {message.from_user.id}")
        s = cursor.fetchone()
        soldiers = s[0]
        cursor.execute(f"SELECT cars FROM army WHERE user_id = {message.from_user.id}")
        c = cursor.fetchone()
        cars = c[0]
        cursor.execute(f"SELECT tanks FROM army WHERE user_id = {message.from_user.id}")
        t = cursor.fetchone()
        tanks = t[0]
        connection.commit()
        balls = soldiers + (cars * 5) + (tanks * 20)
        need = (cars * 3) + (tanks *4)
        if soldiers <= need:
            await message.answer(f"Не хватка Солдат!{soldiers - need}", reply_markup=armmy_kb)
        else:
            await message.answer(f"--Армия--\nСолдаты - {soldiers - need}🪖\nМашины - {cars}🛻\nТанки - {tanks}💥\nБаллы - {balls}", reply_markup=armmy_kb)

@router.callback_query(F.data == 'sol')
async def add_soldiers(callback: CallbackQuery):
    acc = await army_accept(callback.from_user.id, 100)
    if acc == True:
        await add_army_slodiers(callback.from_user.id, 100, 10)
        await callback.message.answer("10 Солдат успешно прибыли в вашу армию!🪖")
    else:
        await callback.message.answer("Не достаточно денег📉")

async def army_accept(id, price):
    cursor.execute(f"SELECT cash FROM users WHERE user_id = {id}")
    c = cursor.fetchone()
    cash = c[0]
    if cash >= price:
        return True
    else: 
        return False
    
async def add_army_slodiers(id, price, number):
    cursor.execute("UPDATE army SET soldiers = soldiers + ? WHERE user_id = ?", (number, id))
    cursor.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", (price, id))
    connection.commit()

@router.callback_query(F.data == 'car')
async def add_сars(callback: CallbackQuery):
    acc = await army_accept(callback.from_user.id, 1000)
    if acc == True:
        await add_army_cars(callback.from_user.id, 1000, 5)
        await callback.message.answer("5 Машин успешно прибыли в вашу армию!🪖")
    else:
        await callback.message.answer("Не достаточно денег📉")

async def add_army_cars(id, price, number):
    cursor.execute("UPDATE army SET cars = cars + ? WHERE user_id = ?", (number, id))
    cursor.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", (price, id))
    connection.commit()

@router.callback_query(F.data == 'tan')
async def add_tanks(callback: CallbackQuery):
    acc = await army_accept(callback.from_user.id, 3000)
    if acc == True:
        await add_army_tanks(callback.from_user.id, 3000, 1)
        await callback.message.answer("1 Танк успешно прибыли в вашу армию!🪖")
    else:
        await callback.message.answer("Не достаточно денег📉")

async def add_army_tanks(id, price, number):
    cursor.execute("UPDATE army SET tanks = tanks + ? WHERE user_id = ?", (number, id))
    cursor.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", (price, id))
    connection.commit()

def get_army(user_id):
    cursor.execute('SELECT soldiers, cars, tanks FROM army WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return {'soldiers': result[0], 'cars': result[1], 'tanks': result[2]} if result else None

def calculate_army_strength(army):
    soldiers = army['soldiers']
    cars = army['cars']
    tanks = army['tanks']
    
    needed_soldiers_for_cars = cars * 3
    needed_soldiers_for_tanks = tanks * 4
    total_needed_soldiers = needed_soldiers_for_cars + needed_soldiers_for_tanks
    
    if soldiers < total_needed_soldiers:
        return None 
    
    remaining_soldiers = soldiers - total_needed_soldiers
    strength = remaining_soldiers + (cars * 5) + (tanks * 20)
    return strength

@router.message(F.text == 'cражаться')
async def battle(message: Message):
    if not message.reply_to_message:
        await message.answer("Сражение возможно только если вы ответите на сообщение соперника.")
        return
    
    user_1_id = message.from_user.id
    user_2_id = message.reply_to_message.from_user.id
    
    army_1 = get_army(user_1_id)
    army_2 = get_army(user_2_id)
    
    if not army_1 or not army_2:
        await message.answer("Не удалось найти армии одного из пользователей.")
        return
    
    strength_1 = calculate_army_strength(army_1)
    strength_2 = calculate_army_strength(army_2)
    
    if strength_1 is None:
        await message.answer(f"У пользователя {message.from_user.username} недостаточно солдат для управления машинами и танками.")
        return
    
    if strength_2 is None:
        await message.answer(f"У пользователя {message.reply_to_message.from_user.username} недостаточно солдат для управления машинами и танками.")
        return
    
    if strength_1 > strength_2:
        result_message = f"Победитель: {message.from_user.username}!\nСила армии: {strength_1} баллов против {strength_2}."
    elif strength_1 < strength_2:
        result_message = f"Победитель: {message.reply_to_message.from_user.username}!\nСила армии: {strength_2} баллов против {strength_1}."
    else:
        result_message = f"Ничья! Обе армии имеют одинаковую силу: {strength_1} баллов."
    
    await message.answer(result_message)

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

@router.message(F.text == "admin")
async def adminka(message: Message):
    await message.answer("Админка:🤠", reply_markup=admin_kb)

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
        cursor.execute(f"SELECT user_id FROM admin WHERE user_id = {message.text}")
        a = cursor.fetchone()
        adma = a[0]
        if adma != None:
            cursor.execute(f"DELETE FROM admin WHERE user_id = {message.text}")
            connection.commit()
            await bot.send_message(message.text, f"Вы были удалены админом {message.from_user.first_name}")
            await message.reply("Удаление прошло успешно!✅")
            await state.clear()
        else:
            await message.answer("Такого админа нет🙅‍♂️")

@router.message(Command("help_admin"))
async def help_admin(message: Message):
    cursor.execute(F"SELECT user_id FROM admin WHERE user_id = {message.from_user.id}")
    a = cursor.fetchone()
    connection.commit()
    if a != None:
        await message.answer("Вот команды для админов:\n/delete - Для удаление скамеров🤡 и плохих людей❗️\nban - команда для создателя бойтесь ее💀")
    else:
        await message.answer('Сперва админом стань😐')

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

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

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
            stavka = stavka * random.randint(1.1, 2)
            await message.answer(f"Вы выйграли - {stavka}!🤑")
            cursor.execute(f"UPDATE users SET cash = cahs + ? WHERE user_id = ?", (stavka, message.from_user.id))
            connection.commit()
            await state.clear()
        else:
            await message.answer(f"Вы проиграли!😭, ваша ставка - {stavka}")
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

games = {}

def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def check_victory(board, symbol):
    for row in board:
        if row.count(symbol) == 3:
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)].count(symbol) == 3:
            return True
    if [board[i][i] for i in range(3)].count(symbol) == 3 or [board[i][2 - i] for i in range(3)].count(symbol) == 3:
        return True
    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def display_board(board):
    return "\n".join([" | ".join(row) for row in board])

def generate_keyboard(board):
    builder = InlineKeyboardBuilder()
    for i in range(3):
        buttons = []
        for j in range(3):
            if board[i][j] == " ":
                buttons.append(InlineKeyboardButton(text="⬜", callback_data=f"move_{i},{j}"))
            else:
                buttons.append(InlineKeyboardButton(text=board[i][j], callback_data=f"taken_{i},{j}"))
        builder.row(*buttons)
    return builder.as_markup()

def bot_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)

@router.message(Command("start_game"))
async def start_game(message: Message):
    games[message.chat.id] = create_board()
    await message.answer(f"Игра началась! Вы играете крестиками (X).\nВаш ход:\n{display_board(games[message.chat.id])}", reply_markup=generate_keyboard(games[message.chat.id]))

@router.callback_query()
async def handle_move(call: CallbackQuery):
    if not (call.data.startswith("move_") or call.data.startswith("taken_")):
        return

    game = games.get(call.message.chat.id)

    if not game:
        await call.message.answer("Игра не найдена.")
        return

    if call.data.startswith("taken"):
        await call.answer("Эта клетка уже занята!")
        return

    if call.data.startswith("move"):
        i, j = map(int, call.data.split("_")[1].split(","))
        if game[i][j] != " ":
            await call.answer("Эта клетка уже занята!")
            return

        game[i][j] = "X"

        if check_victory(game, "X"):
            await call.message.edit_text(f"Поздравляем! Вы победили!\n{display_board(game)}")
            games.pop(call.message.chat.id)
            return

        if check_draw(game):
            await call.message.edit_text(f"Ничья!\n{display_board(game)}")
            games.pop(call.message.chat.id)
            return

        bot_i, bot_j = bot_move(game)
        game[bot_i][bot_j] = "O"

        if check_victory(game, "O"):
            await call.message.edit_text(f"Бот победил!\n{display_board(game)}")
            games.pop(call.message.chat.id)
            return

        if check_draw(game):
            await call.message.edit_text(f"Ничья!\n{display_board(game)}")
            games.pop(call.message.chat.id)
            return

        await call.message.edit_text(f"Ваш ход:\n{display_board(game)}", reply_markup=generate_keyboard(game))

class Trading(StatesGroup):
    n = State()

@router.message(F.text == "Trading")
async def trading(message: Message, state:FSMContext):
    await message.answer("Введите куда пойдет рынок\nВниз📉\nНавверх📈")
    await state.set_state(Trading.n)

@router.message(Trading.n)
async def trade(message: Message, state:FSMContext):
    choice = random.choice(['Вниз', 'Навверх'])
    try:
        if message.text == choice:
            win = random.randint(1000, 10000)
            await message.answer(f"Вы угадали ваша прибыль - {win}💰")
            await state.clear()
        else:
            lose = random.randint(1000, 10000)
            await message.answer(f"Вы не угадали вы потеряли - {lose}🥲")
            await state.clear()
    except BaseException as e:
        await message.answer(f"Ошибка: {e}")

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

################################################################################
# ################################################################################
# ################################################################################
# ################################################################################################################################################################
