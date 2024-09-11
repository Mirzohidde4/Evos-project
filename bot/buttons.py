from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlite import ReadDb


contact = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='📲 Telefon raqamni yuborish', request_contact=True)]
  ],
  resize_keyboard=True, one_time_keyboard=True
)


menyu = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='🍴 Menyu')],
    [KeyboardButton(text='📋 Mening buyurtmalarim')],
    [KeyboardButton(text='📥 Savat'), KeyboardButton(text='📞 Aloqa')],
    [KeyboardButton(text='📨 Xabar yuborish'), KeyboardButton(text='⚙️ Sozlamalar')],
    [KeyboardButton(text='ℹ️ Biz haqimizda')]
  ],
  resize_keyboard=True, one_time_keyboard=True
)


settings = ReplyKeyboardMarkup(
  keyboard=[
    # [KeyboardButton(text='🇺🇿 Tilni o\'zgartirish')],
    [KeyboardButton(text='🗑 Ma\'lumotlarni tozalash')],
    [KeyboardButton(text='🔙 Orqaga qaytish')]
  ],
  resize_keyboard=True
)


savat = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='📥 Savat')],
    [KeyboardButton(text='🔙 Orqaga qaytish')]
  ],
  resize_keyboard=True
)


tasdiqlash = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='✅ Tasdiqlash'), KeyboardButton(text='❌ Bekor qilish')],
    [KeyboardButton(text='🔙 Orqaga qaytish')]
  ],
  resize_keyboard=True
)


tolov = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='💵 Naqd'), KeyboardButton(text='💳 Karta')],
  ],
  resize_keyboard=True
)


tasdiq_turi = ReplyKeyboardMarkup(
  keyboard=[
    [KeyboardButton(text='✅ Ha'), KeyboardButton(text='❌ Yo\'q')],
  ],
  resize_keyboard=True
)


location = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📍 Joylashuvni yuborish', request_location=True)]
    ],
    resize_keyboard=True, one_time_keyboard=True
)