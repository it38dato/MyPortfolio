from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
#from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from app import keyboards as kb
from app import database as db
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)
#main = ReplyKeyboardMarkup(resize_keyboard=True)
#main.add('Каталог').add('Корзина').add('Контакты')
#main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
#main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')
#admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
#admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')
#catalog_list = InlineKeyboardMarkup(row_width=2)
#catalog_list.add(InlineKeyboardButton(text='Футболки', url='https://youtube.com/@sudoteach'),
#    InlineKeyboardButton(text='Шорты', url='https://youtube.com/@sudoteach'),
#    InlineKeyboardButton(text='Кроссовки', url='https://youtube.com/@sudoteach'))
async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')
class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer_sticker('CAACAgIAAxkBAAMsZkF9sejjkJMP5H6BQwW-BUeMfncAAosBAAIrXlMLo2G8aSQ0g1A1BA')
    await message.answer(f'{message.from_user.first_name}, Добро пожаловать в магазин кросовок!', reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор!', reply_markup=kb.main_admin)
#@dp.message_handler(content_types=['sticker'])
#async def check_sticker(message: types.Message):
#    await message.answer(message.sticker.file_id)
#    await bot.send_message(message.from_user.id, message.chat.id)
#@dp.message_handler(content_types=['document', 'photo'])
#async def forward_message(message: types.Message):
#    await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)
@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')
@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer('Выберите категорию', reply_markup=kb.catalog_list)
@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста!')
@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него: @mesudoteach')
@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')
@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer('Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю.')
@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()
@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewOrder.next()
@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewOrder.next()
@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await NewOrder.next()
@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')
@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()
@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')
@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 't-shirt':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали футболки')
    elif callback_query.data == 'shorts':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали шорты')
    elif callback_query.data == 'sneakers':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали кроссовки')
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)