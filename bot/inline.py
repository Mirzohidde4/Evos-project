import logging
from config import CHANEL_ID, TOKEN
from aiogram import Bot, html
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from sqlite import ReadDb

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def chatjoin(user_id: int, user: str, username: str) -> bool:
    btn = InlineKeyboardBuilder()
    is_subscribed = True

    count = 1
    for ch in CHANEL_ID:
        try:
            user_status = await bot.get_chat_member(f"@{ch}", user_id)
        except Exception as e:
            logging.error(f"Error checking user status in channel {ch}: {e}")
            continue

        if user_status.status not in ["creator", "administrator", "member"]:
            btn.add(
                InlineKeyboardButton(text=f'➕ Obuna bo\'lish {count}', url=f"https://t.me/{ch}")
            )
            is_subscribed = False
        count += 1    

    btn.add(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="result"))
    btn.adjust(1)

    if not is_subscribed:
        await bot.send_message(
            chat_id=user_id, 
            text=f'''
                 <b>Assalom alaykum, {html.link(value=user, link=username)}! 
🟢EVOS'ning rasmiy hamkor kanallariga a'zo bo'lishingiz orqali 🔖(50% chegirma) ni qo'lga kiriting.</b>

(⚠️Hamkor kanallarimizga obuna bo'lmasdan botdan foydalana olmaysiz.)
            ''', 
            reply_markup=btn.as_markup()
        )
        return False
    return True


mahsulotlar = InlineKeyboardBuilder()
for categoriya in ReadDb('main_menyu'):
    soni = 0
    if ReadDb('main_food'):
        for son in ReadDb('main_food'):
            if son[3] == categoriya[0]:
                soni += 1
    mahsulotlar.add(InlineKeyboardButton(text=f'{categoriya[1]} ({soni})', callback_data=f'menu_{categoriya[1]}'))
mahsulotlar.add(InlineKeyboardButton(text='🔙 Orqaga', callback_data='menu_orqaga'))
mahsulotlar.adjust(3)

