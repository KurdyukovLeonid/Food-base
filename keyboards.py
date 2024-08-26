from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb.add(button1, button2)

product_kb = InlineKeyboardMarkup()
for i in range(1, 5):
    product_button = InlineKeyboardButton(text=f'Продукт {i}', callback_data='product_buying')
    product_kb.add(product_button)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)

