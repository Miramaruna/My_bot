from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# buttons

button_start = [
    [KeyboardButton(text='/play'), KeyboardButton(text='/info')],
    [KeyboardButton(text='/help'), KeyboardButton(text='register')],
    [KeyboardButton(text='Профиль'), KeyboardButton(text='users')],
    [KeyboardButton(text='/help_admin'), KeyboardButton(text="Копать")],
    [KeyboardButton(text='/shop')]
]

button_play = [
    [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3')]
]

button_info = [
    [KeyboardButton(text='geeks')]
]

keyboard_play = ReplyKeyboardMarkup(keyboard=button_play, resize_keyboard=True, one_time_keyboard=True)
keyboard_start = ReplyKeyboardMarkup(keyboard=button_start,resize_keyboard=True)
keyboard_info = ReplyKeyboardMarkup(keyboard=button_info,resize_keyboard=True, one_time_keyboard=True)

army = [
    [InlineKeyboardButton(text='Увеличить кол. Людей', callback_data='add')],
    [InlineKeyboardButton(text='start', callback_data='st')],
    [InlineKeyboardButton(text='stop', callback_data='sp')]
]

arm_kb = InlineKeyboardMarkup(inline_keyboard=army)

shop = [
    [KeyboardButton(text='Телефоны')],
    [KeyboardButton(text='Машины')],
    [KeyboardButton(text='Дома')]
    # [KeyboardButton(text='Дома еще в разработке')]
]
shop_kb = ReplyKeyboardMarkup(keyboard=shop, resize_keyboard=True, one_time_keyboard=True)

car = [
    [KeyboardButton(text='Mercedes')],
    [KeyboardButton(text='BMW')]
]
car_kb = ReplyKeyboardMarkup(keyboard=car, resize_keyboard=True, one_time_keyboard=True)

ar = [
    [InlineKeyboardButton(text='Ad. Soldiers', callback_data='sol')],
    [InlineKeyboardButton(text='Ad. Cars', callback_data='car')],
    [InlineKeyboardButton(text='Ad. Tanks', callback_data='tan')]
]
armmy_kb = InlineKeyboardMarkup(inline_keyboard=ar)

admin = [
    [KeyboardButton(text='stop'), KeyboardButton(text='/передача')],
    [KeyboardButton(text="ban_admin"), KeyboardButton(text="ban_admin")],
    [KeyboardButton(text="delete"), KeyboardButton(text="/mailing")]
]
admin_kb = ReplyKeyboardMarkup(keyboard=admin, resize_keyboard=True, one_time_keyboard=True)