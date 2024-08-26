from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from keyboards import *
import crud_functions

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

crud_functions.initiate_db()


# crud_functions.populate_db()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def started(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup=start_menu)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Мы поможем тебе!')


@dp.message_handler(text='Рассчитать')
async def started(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = 10 * int(data.get('weight')) + 6.25 * int(data.get('growth')) - 5 * int(data.get('age')) + 5
    await message.answer(f'Ваша норма калорий: {res}')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = crud_functions.get_all_products()
    for product in products:
        title, description, price = product
        await message.answer(f'Название: {title} | Описание: {description} | Цена: {price}')
        img_path = f'photos/{products.index(product) + 1}.png'
        with open(img_path, 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=product_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state: FSMContext):
    username = message.text
    if crud_functions.is_included(username):
        await message.answer("Пользователь уже существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state: FSMContext):
    age = message.text
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')

    crud_functions.add_user(username, email, age)
    await message.answer("Вы успешно зарегистрированы!")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
