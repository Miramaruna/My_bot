from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# buttons

button_start = [
    [KeyboardButton(text='/play'), KeyboardButton(text='/info')],
    [KeyboardButton(text='/help'), KeyboardButton(text='register')],
    [KeyboardButton(text='Профиль'), KeyboardButton(text='users')]
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

# help_admin = [
    # [InlineKeyboardButton(text='delete', callback_data='delete')]
# ]

# help_admin_keyboard = InlineKeyboardMarkup(inline_keyboard=help_admin)

help_admin = [
    [KeyboardButton(text='/delete')]
]

keyboard_help_admin = ReplyKeyboardMarkup(keyboard=help_admin, resize_keyboard=True)