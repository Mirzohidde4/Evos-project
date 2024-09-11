import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import (
    Message, CallbackQuery, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup,
    FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
)
from aiogram.filters import CommandStart, Command, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import TOKEN, ADMIN_ID
from buttons import contact, menyu, settings, savat, tasdiqlash, tolov, tasdiq_turi, location
from inline import chatjoin, mahsulotlar
from state import xabar, zakaz
from datetime import datetime
from sqlite import (
    ReadDb, AddUser, AddXabar, AddSavat, DeleteDb, AddBuyurtma, UpdateBuyurtma,
    Taomlarr, Mahsulotlar, Tasdiqlanmagan, Tozalash, UpdateSavat, Zakaz
)


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def smd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user = message.from_user.full_name
    urls = message.from_user.url
    # if await chatjoin(user_id=user_id, user=user, username=urls):

    if any(user[1] == user_id for user in ReadDb('main_users')):
        await message.reply(text=f'{html.bold('EVOS | Доставка')} botiga xush kelibsiz!')
        await message.answer(text=f'🛒 {html.bold('Asosiy Menyu')}')
        await message.answer(
            text='Marhamat buyurtma berishingiz mumkin!',
            reply_markup=menyu
        )
            
    else:    
        await message.answer(text=f'{html.bold('EVOS | Доставка')} botiga xush kelibsiz!')
        await message.answer(
            text='Botdan foydalanish uchun,\navval telefon raqamingizni yuboring.',
            reply_markup=contact
        )
        await state.set_state(zakaz.telefon)


@dp.callback_query(F.data == 'result')        
async def result(call: CallbackQuery):
    await call.message.delete()
    user = call.from_user.full_name
    user_id = call.from_user.id
    username = call.message.from_user.username or 'noma\'lum'
    if await chatjoin(user_id=user_id, user=user, username=username):
        await call.message.answer(
            text=f"""
                🥳Tabriklaymiz!!! Sizga 🎁<b>50% chegirma</b> taqdim etildi.

📑Promokodingiz: EVOS1707890 nusxalab botga yuboring.

/start botni qayta ishga tushuring.
            """,
        )
    else:
        await call.answer(text="Iltimos kanalga obuna bo'ling")    


@dp.message(F.contact, zakaz.telefon)
async def Contact(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = message.from_user.full_name or 'noma\'lum'
    username = message.from_user.username or 'noma\'lum'
    tel = message.contact.phone_number
    try:
        AddUser(user_id, user, username, tel)
        await message.reply(text=f'Telefon raqamingiz qabul qilindi✅')
        await message.answer(text=f'🛒 {html.bold('Asosiy Menyu')}')
        await message.answer(
            text='Marhamat buyurtma berishingiz mumkin!',
            reply_markup=menyu
        )
    except Exception as ex:
        logging.info(f'User qo\'shishda xatolik: {ex}')
    await state.clear()


@dp.message(F.text == '🍴 Menyu')
async def Menyu(message: Message):
    if ReadDb('main_menyu'):
        await message.answer_photo(
            photo='https://avatars.mds.yandex.net/i?id=a84ce466efb37e0b77f3ebb24a5ca2c165f77fda-11380860-images-thumbs&n=13',
            caption='<b>🍔 Mahsulotlarimiz :</b>',
            reply_markup=mahsulotlar.as_markup()
        )
    else:
        await message.answer(
            text='<b>Mahsulot mavjud emas.</b>',
            reply_markup=menyu
        )


@dp.callback_query(F.data.startswith('menu_'))
async def Menyus(call: CallbackQuery):
    categoriya = call.data.split('_')[1]

    if categoriya == 'orqaga':
        await call.message.delete()
        await call.message.answer(
            text=f'🛒 {html.bold("Asosiy Menyu")}',
            reply_markup=menyu
        )

    elif Taomlarr(category=categoriya):
        foods = InlineKeyboardBuilder()
        for food in Taomlarr(category=categoriya):
            foods.add(InlineKeyboardButton(text=food, callback_data=f'taom_{food}'))
        foods.add(InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'taom_orqaga'))    
        foods.adjust(2)
        
        photos = None
        for rasm in ReadDb('main_menyu'):
            if rasm[1] == categoriya:
                photos = rasm[2]
                break
        
        if photos:
            try:
                await call.message.delete() 
                await call.message.answer_photo(
                    photo=FSInputFile(path=f'../{str(photos)}'),
                    reply_markup=foods.as_markup()
                )
            except Exception as e:
                print(f"Rasmni yuborishda xato: {e}")   
        else:
            await call.message.answer(
                text='<b>Tanlang:</b>',
                reply_markup=foods.as_markup()
            ) 

    else:
        await call.answer(
            text='Mahsulot mavjud emas',
            show_alert=True
        )              


@dp.callback_query(F.data.startswith('taom_'))       
async def Taomlar(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    categoriya = call.data.split('_')[1]
    user = call.from_user.full_name
    user_id = call.from_user.id

    if categoriya == 'orqaga':
        await call.message.answer_photo(
            photo='https://avatars.mds.yandex.net/i?id=a84ce466efb37e0b77f3ebb24a5ca2c165f77fda-11380860-images-thumbs&n=13',
            caption='<b>🍔 Mahsulotlarimiz :</b>',
            reply_markup=mahsulotlar.as_markup()
        )

    elif Mahsulotlar(categoriya):
        count = 1
        if Mahsulotlar(categoriya)[2] == None:
            if Mahsulotlar(categoriya)[3] == None:
                await call.message.answer_photo(
                    photo=FSInputFile(path=f'../{Mahsulotlar(categoriya)[1]}'),
                    caption=f'Narxi: {Mahsulotlar(categoriya)[0]} so\'m',
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                            [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                        ]
                    )
                )
            else:
                await call.message.answer_photo(
                    photo=FSInputFile(path=f'../{Mahsulotlar(categoriya)[1]}'),
                    caption=f'{Mahsulotlar(categoriya)[3]}\n\nNarxi: {Mahsulotlar(categoriya)[0]} so\'m',
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                            [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                        ]
                    )
                )

            await state.update_data(
                {
                    'user': user,
                    'user_id': user_id,
                    'name': categoriya,
                    'count': count,
                    'price': Mahsulotlar(categoriya)[0],
                    'photo': Mahsulotlar(categoriya)[1]
                }
            )        
        
        else:
            if Mahsulotlar(categoriya)[3] == None:
                await call.message.answer_photo(
                    photo=FSInputFile(path=f'../{Mahsulotlar(categoriya)[1]}'),
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=f'Katta {Mahsulotlar(categoriya)[0]} so\'m', callback_data='double_big'), 
                            InlineKeyboardButton(text=f'Kichik {Mahsulotlar(categoriya)[2]} so\'m', callback_data='double_mini')],
                            [InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'double_orqaga')]
                        ]
                    )    
                )
            else:
                await call.message.answer_photo(
                    photo=FSInputFile(path=f'../{Mahsulotlar(categoriya)[1]}'),
                    caption=f'{Mahsulotlar(categoriya)[3]}',
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text=f'Katta {Mahsulotlar(categoriya)[0]} so\'m', callback_data='double_big'), 
                            InlineKeyboardButton(text=f'Kichik {Mahsulotlar(categoriya)[2]} so\'m', callback_data='double_mini')],
                            [InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'double_orqaga')]
                        ]
                    )    
                )
            await state.update_data(
                {
                    'user': user,
                    'user_id': user_id,
                    'name': categoriya,
                    'count': count,
                    'big_price': Mahsulotlar(categoriya)[0],
                    'mini_price': Mahsulotlar(categoriya)[2],
                    'photo': Mahsulotlar(categoriya)[1]
                }
            )    

    else:
        await call.answer(
            text='<b>Taom mavjud emas.</b>',
            show_alert=True
        )


@dp.callback_query(F.data.startswith('double_'))
async def Double(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    action = call.data.split('_')[1]
    data1 = await state.get_data()
    count = data1.get('count')
    big_price = data1.get('big_price')
    mini_price = data1.get('mini_price')
    photo = data1.get('photo')

    if action == 'orqaga':
        pass

    elif action == 'big':
        await call.message.answer_photo(
            photo=FSInputFile(path=f'../{photo}'),
            caption=f'Narxi: {big_price} so\'m',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                    [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                ]
            )
        )
        await state.update_data(
            {
                'count': count,
                'price': big_price,
                'photo': photo
            }
        )     

    elif action == 'mini':
        await call.message.answer_photo(
            photo=FSInputFile(path=f'../{photo}'),
            caption=f'Narxi: {mini_price} so\'m',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                    [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                ]
            )
        )
        await state.update_data(
            {
                'count': count,
                'price': mini_price,
                'photo': photo
            }
        )     


@dp.callback_query(F.data.startswith('mahsulot_'))
async def Amal(call: CallbackQuery, state: FSMContext):
    action = call.data.split('_')[1]
    data = await state.get_data()
    user = data.get('user')
    user_id = data.get('user_id')
    name = data.get('name')
    count = data.get('count')
    price = data.get('price')
    photo = data.get('photo')

    if action == 'orqaga':
        id_menu = None
        for food in ReadDb('main_food'):
            if food[1] == name:
                id_menu = food[3]
        photos = None
        for rasm in ReadDb('main_menyu'):
            if rasm[0] == id_menu:
                photos = rasm[2]
                break
        
        foods = InlineKeyboardBuilder()
        for food in ReadDb('main_food'):
            if food[3] == id_menu:
                foods.add(InlineKeyboardButton(text=food[1], callback_data=f'taom_{food[1]}'))
        foods.add(InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'taom_orqaga'))    
        foods.adjust(2)
        
        if photos:
            try:
                await call.message.delete() 
                await call.message.answer_photo(
                    photo=FSInputFile(path=f'../{str(photos)}'),
                    reply_markup=foods.as_markup()
                )
            except Exception as e:
                print(f"Rasmni yuborishda xato: {e}")
        else:
            await call.message.answer(
                text='<b>Tanlang:</b>',
                reply_markup=foods.as_markup()
            )        

    elif action == 'qo\'shish':
        total = count * price
        if ReadDb('main_savat'):
            for user_savat in ReadDb('main_savat'):
                if (user_savat[2] == user_id) and (user_savat[3] == name):
                    cnt = user_savat[4] + count
                    tl_price = user_savat[6] + total
                    try:
                        UpdateSavat(cnt, tl_price, user_id, name)
                        await call.message.answer(
                            text=f'{html.bold(f'📥Savat yangilandi.\n+{count}:')} {name}',
                            reply_markup=savat
                        )
                    except Exception as e:
                        logging.info(f'Savatni yangilashda xatolik: {e}')
                    break                
            else:    
                try:
                    AddSavat(user=user, user_id=user_id, name=name, count=count, price=price, total_price=total)
                    await call.message.answer(
                        text=f'{html.bold(f'📥Savatga qo\'shildi.\n+{count}:')} {name}',
                        reply_markup=savat
                    )
                except Exception as e:
                    logging.info(f'Savatga qo\'shishda xatolik: {e}') 
        
        else:    
            try:
                AddSavat(user=user, user_id=user_id, name=name, count=count, price=price, total_price=total)
                await call.message.answer(
                    text=f'{html.bold(f'📥Savatga qo\'shildi.\n+{count}:')} {name}',
                    reply_markup=savat
                )
            except Exception as e:
                logging.info(f'Savatga qo\'shishda xatolik: {e}') 

    elif action == 'soni':
        await call.answer(
            text=f'{count} ta'
        )        

    elif action == 'minus':
        if count >= 2:
            count -= 1
            if call.message.text:
                await bot.edit_message_text(
                    text = call.message.text,
                    chat_id = call.message.chat.id,
                    message_id = call.message.message_id,
                    reply_markup = InlineKeyboardMarkup(
                        inline_keyboard = [
                            [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                            [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                        ]
                    )
                )

            elif call.message.photo:
                await bot.edit_message_media(
                    media = InputMediaPhoto(
                        media = call.message.photo[-1].file_id,
                        caption = call.message.caption or ''
                    ),
                    chat_id = call.message.chat.id,
                    message_id = call.message.message_id,
                    reply_markup = InlineKeyboardMarkup(
                        inline_keyboard = [
                            [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                            [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                        ]
                    )
                )
            await call.answer(text='mahsulot -1')

            await state.update_data(
                {
                    'user': user,
                    'user_id': user_id,
                    'name': name,
                    'count': count,
                    'price': price,
                    'photo': photo
                }    
            )
        else:
            await call.answer(text='kamaytira olmaysiz')


    elif action == 'plus':
        count += 1
        if call.message.text:
            await bot.edit_message_text(
                text = call.message.text,
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                reply_markup = InlineKeyboardMarkup(
                    inline_keyboard = [
                        [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                        [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                    ]
                )
            )

        elif call.message.photo:
            await bot.edit_message_media(
                media = InputMediaPhoto(
                    media = call.message.photo[-1].file_id,
                    caption = call.message.caption or ''
                ),
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                reply_markup = InlineKeyboardMarkup(
                    inline_keyboard = [
                        [InlineKeyboardButton(text='-', callback_data='mahsulot_minus'), InlineKeyboardButton(text=f'{count}', callback_data='mahsulot_soni'), InlineKeyboardButton(text='+', callback_data='mahsulot_plus')],
                        [InlineKeyboardButton(text='📥 Savatga qo\'shish', callback_data='mahsulot_qo\'shish'), InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'mahsulot_orqaga')]
                    ]
                )
            )

        await call.answer(text='mahsulot +1')   
        await state.update_data(
            {
                'user': user,
                'user_id': user_id,
                'name': name,
                'count': count,
                'price': price,
                'photo': photo
            }    
        )    


@dp.message(F.text == '📥 Savat')    
async def Savat(message: Message):
    user_id = message.from_user.id
    urls = message.from_user.url
    name = message.from_user.full_name

    if ReadDb('main_savat'):
        prices = []
        response = str('<b>🛒 Sizning savatingiz:</b>')
        number = 0
        for user in ReadDb('main_savat'):
            if user[2] == user_id:
                number += 1
                response += str(f'\n\n<b>{number}.</b>\n<b>🍽 Nomi:</b> {user[3]}\n<b>💶 Narxi:</b> {user[5]:.2f} so\'m\n<b>▫️ Soni:</b> {user[4]} ta\n<b>💸 Umumiy narx:</b> {user[6]:.2f} so\'m')   
                prices.append(user[6])
        total_prices = sum(prices)

        if any(user[2] == user_id for user in ReadDb('main_savat')):
            await message.answer(
                text=f"<b>🤵🏻 Hurmatli</b> <a href='{urls}'>{name}</a>\n{response}\n\n\n<b>💰 Umumiy haridingiz narxi:</b> {total_prices:.2f} so\'m\n<b>❓ Buyurtmani tasdiqlaysizmi?</b>",
                reply_markup=tasdiqlash
            )    
        else:
            await message.answer(
                text='🛒 Savatingiz bo\'sh 🗑',
                reply_markup=menyu
            )    
    
    else:
        await message.answer(
            text='🛒 Savatingiz bo\'sh 🗑',
            reply_markup=menyu
        )          


@dp.message(F.text == '✅ Tasdiqlash')
async def Tasdiqlash(message: Message, state: FSMContext):
    await message.answer(
        text='💶 <b>| To\'lov turini tanlang:</b>',
        reply_markup=tolov
    )
    await state.set_state(zakaz.tolov)


@dp.message(zakaz.tolov)
async def NaqdPul(message: Message, state: FSMContext):
    if message.text == '💵 Naqd':
        await message.reply(text='<b>T\'olov turi | naqd pul orqali </b>')
        await message.answer(
            text='<b>Buyurtmani tasdiqlaysizmi?</b>',
            reply_markup=tasdiq_turi
            )
        await state.update_data({'turi': 'naqd'})
        await state.set_state(zakaz.tasdiq)    
    
    elif message.text == '💳 Karta':
        await message.reply(text='<b>T\'olov turi | karta orqali </b>')
        await message.answer(
            text='<b>Buyurtmani tasdiqlaysizmi?</b>',
            reply_markup=tasdiq_turi
            )
        await state.update_data({'turi': 'karta'})
        await state.set_state(zakaz.tasdiq)    

    elif message:
        await message.reply(
            text='💶 <b>| Iltimos to\'lov turini tanlang:</b>',
            reply_markup=tolov
        )    
        await state.set_state(zakaz.tolov)


@dp.message(zakaz.tasdiq)
async def Haa(message: Message, state: FSMContext):
    if message.text == '✅ Ha':
        await message.answer(
            text='📍 <b>Botga joylashuv ma\'lumotingizni yuboring.</b>',
            reply_markup=location
        )
        await state.set_state(zakaz.joylashuv)

    elif message.text == '❌ Yo\'q':
        await message.answer(
            text=f'🛒 {html.bold("Asosiy Menyu")}',
            reply_markup=menyu
        )
        await state.clear()

    else:
        await message.reply(
            text='<b>Buyurtmani tasdiqlaysizmi?</b>',
            reply_markup=tasdiq_turi
        )    
        await state.set_state(zakaz.tasdiq)  


@dp.message(zakaz.joylashuv)
async def Joylashuv(message: Message, state: FSMContext):
    user_id = message.from_user.id
    urls = message.from_user.url
    name = message.from_user.full_name
    
    phone = None
    for user in ReadDb('main_users'):
        if user[1] == user_id:
            phone = user[3]
    if phone:
        if phone.startswith('+'):
            tel = phone
        else:
            tel = f'+{phone}'    
    else:
        tel = None

    if message.location:
        data = await state.get_data()
        tur = data.get('turi')

        if ReadDb('main_savat'):
            prices = []
            number = 0
            response = str('<b>📦 Yangi buyurtma:</b>')

            if tur == 'naqd':
                loading = await message.answer(text='<b>Buyurtmangiz qabul qilinmoqda...</b>')
                await asyncio.sleep(2)
                for user in ReadDb('main_savat'):
                    if user[2] == user_id:
                        try:
                            formatted_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            AddBuyurtma(user=user[1], user_id=user[2], name=user[3], count=user[4], price=user[5], total_price=user[6], created=formatted_now, turi=tur, status='ko\'rib chiqilmoqda...')
                        except Exception as e:
                            logging.info(f'Buyurtma qo\'shishda xatolik: {e}')

                        try:
                            DeleteDb('main_savat', 'user_id', user_id)
                        except Exception as ex:
                            logging.info(f'Savatni ochirishda xatolik: {ex}')

                        number += 1
                        response += str(f'\n\n<b>{number}.</b>\n<b>🍽 Nomi:</b> {user[3]}\n<b>💶 Narxi:</b> {user[5]:.2f} so\'m\n<b>▫️ Soni:</b> {user[4]} ta\n<b>💸 Umumiy narx:</b> {user[6]:.2f} so\'m')   
                        prices.append(user[6])
                total_prices = sum(prices) 

                try:
                    await bot.send_location(
                        chat_id=ADMIN_ID,
                        latitude=message.location.latitude,
                        longitude=message.location.longitude
                    )
                    await bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f'{response}\n\n🙍 <b>Buyurtma egasi: </b><a href="{urls}">{name}</a>\n<b>📲 Telefon raqami: </b>{tel}\n💵<b> Umumiy narx:</b> {total_prices:.2f} so\'m\n<b>💳 To\'lov turi:</b> {tur}\n<b></b>',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text='✅ Qabul qilish', callback_data=f'admin_qabul_{user_id}_{tur}'), InlineKeyboardButton(text='❌ Bekor qilish', callback_data=f'admin_bekor_{user_id}_{tur}')]
                            ]
                        )
                    )
                except Exception as e:
                    logging.info(f'Adminga xabar yuborishda xatolik: {e}')    

                await loading.delete()
                await message.answer(
                    text='<b>🔜 Tez orada sizga xabar beramiz.</b>',
                    reply_markup=ReplyKeyboardRemove()
                )
                await state.clear()

            elif tur == 'karta':
                tl_prices = []
                for user in ReadDb('main_savat'):
                    if user[2] == user_id:
                        tl_prices.append(user[6])
                tl_price = sum(tl_prices)

                await message.answer(
                    text='🚛 <b>Buyurtma to\'lovni amalga oshirganingizdan keyin yo\'lga chiqadi.</b>',
                    reply_markup=ReplyKeyboardRemove()
                )
                await message.answer(
                    text=f'💳 <b>Buyurtma narxi:</b> {tl_price:.2f} so\'m',
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text='💳 To\'lov qilish', callback_data='tolov_qilish')]
                        ]
                    )
                )    
                await state.update_data({'location': message.location})

    else:    
        await message.answer(
            text='📍 <b>Iltimos joylashuvni yuborish tugmasini bosing!</b>',
            reply_markup=location
        )
        await state.set_state(zakaz.joylashuv)


@dp.callback_query(F.data.startswith('admin_'))
async def Inform(call: CallbackQuery, state: FSMContext):
    action = call.data.split('_')[1]
    user_idd = call.data.split('_')[2]
    turi = call.data.split('_')[3]
    user_id = int(user_idd)
    date = None
    prices = []
    response = str('\n\n🍱 <b>Sizning buyurtmangiz:</b>')
    for user in ReadDb('main_buyurtmalar'):
        if user[3] == user_id:
            date = user[1]
            response += str(f'\n       <b>{user[4]}</b> - {user[5]} ta')   
            prices.append(user[7])
    total_prices = sum(prices)
    date_now = str(date).split()[0]
    time_now = str(date).split()[1]

    if action == 'qabul':
        await call.message.edit_text(
            text=f"{call.message.text}\n\n✅ <b>Buyurtma jo\'natildi</b>.",
        )    
        
        try:
            UpdateBuyurtma(user_id=user_id, created=date, status='qabul qilingan ✅')
        except Exception as e:
            logging.info(f'Buyurtma yangilashda xatolik: {e}')
        
        await bot.send_message(
            chat_id=user_id,
            text='📝 <b>Buyurtmangiz qabul qilindi</b>☑️'
        )

        await bot.send_message(
            chat_id=user_id,
            text=f"{response}\n<b>💵 Umumiy narx:</b> {total_prices:.2f} so\'m\n📌 <b>Buyurtma berilgan sana:</b> {date_now} ({time_now})\n💳 <b>To'lov turi: </b>{turi}\n\n📦 <b>Buyurtmangiz holati:</b> aktiv\n🚛 <b>Buyurtma 15-20 daqiqa ichida oldingizda bo\'ladi ✅</b>",
            reply_markup=menyu
        )
        # await asyncio.sleep(5)
        # await answer.delete() 

    elif action == 'bekor':
        try:
            UpdateBuyurtma(user_id=user_id, created=date, status='bekor qilingan ❌')
        except Exception as e:
            logging.info(f'Buyurtma yangilashda xatolik: {e}')
        
        await call.message.edit_text(
            text=f"{call.message.text}\n\n❌ <b>Buyurtma bekor qilindi</b>.",
        )  

        await bot.send_message(
            chat_id=user_id,
            text='📝 <b>Ayrim sabablarga ko\'ra, buyurtmangiz bekor qilindi</b>🚫'
        )


@dp.callback_query(F.data == 'tolov_qilish')
async def Card(call: CallbackQuery, state: FSMContext):
    if ReadDb('main_karta'):
        card = ''
        a = 0
        for i in str(ReadDb('main_karta')[0][3]):
            a += 1
            card += str(i)
            card += ' ' if a % 4 == 0 else ''
        await call.message.answer_photo(
            photo=FSInputFile(path=f'../{ReadDb('main_karta')[0][1]}'),
            caption=f'💳 <b>Karta raqami:</b> {card}\n👤 <b>Karta egasi:</b> {ReadDb('main_karta')[0][2]}\n\n<b>📲 To\'lovni amalga oshirib to\'lov qilganingiz haqidagi chek yoki screenshotni jo\'nating.</b>',
            reply_markup=ReplyKeyboardRemove()    
        )
    else:
        await call.message.answer(
            text='💳 <b>Karta mavjud emas</b>',
            reply_markup=ReplyKeyboardRemove()
        )

    await state.set_state(zakaz.screenshot)


@dp.message(zakaz.screenshot)
async def Screen(message: Message, state: FSMContext):
    user_id = message.from_user.id
    urls = message.from_user.url
    name = message.from_user.full_name
    data = await state.get_data()
    locatsiya = data.get('location')
    tur = data.get('turi')

    phone = None
    for user in ReadDb('main_users'):
        if user[1] == user_id:
            phone = user[3]
    if phone:
        if phone.startswith('+'):
            tel = phone
        else:
            tel = f'+{phone}'    
    else:
        tel = None

    if ReadDb('main_savat'):
        prices = []
        number = 0
        response = str('<b>📦 Yangi buyurtma:</b>')
        for user in ReadDb('main_savat'):
            if user[2] == user_id:
                try:
                    formatted_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    AddBuyurtma(user=user[1], user_id=user[2], name=user[3], count=user[4], price=user[5], total_price=user[6], created=formatted_now, turi=tur, status='ko\'rib chiqilmoqda...')
                except Exception as e:
                    logging.info(f'Buyurtma qo\'shishda xatolik: {e}')
                try:
                    DeleteDb('main_savat', 'user_id', user_id)
                except Exception as ex:
                    logging.info(f'Savatni ochirishda xatolik: {ex}')    

                number += 1
                response += str(f'\n\n<b>{number}.</b>\n<b>🍽 Nomi:</b> {user[3]}\n<b>💶 Narxi:</b> {user[5]:.2f} so\'m\n<b>▫️ Soni:</b> {user[4]} ta\n<b>💸 Umumiy narx:</b> {user[6]:.2f} so\'m')   
                prices.append(user[6])
        total_prices = sum(prices)    

        if message.photo:
            loading = await message.answer(text='<b>Buyurtmangiz qabul qilinmoqda...</b>')
            await asyncio.sleep(2)
            try:
                await bot.send_location(
                    chat_id=ADMIN_ID,
                    latitude=locatsiya.latitude,
                    longitude=locatsiya.longitude
                )
                await bot.send_photo(
                    chat_id=ADMIN_ID,
                    photo=message.photo[-1].file_id,
                    caption='📷 <b>To\'lov screeenshoti</b>'
                )
                await bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f'{response}\n\n🙍 <b>Buyurtma egasi: </b><a href="{urls}">{name}</a>\n<b>📲 Telefon raqami: </b>{tel}\n💵<b> Umumiy narx:</b> {total_prices:.2f} so\'m\n<b>💳 To\'lov turi:</b> karta\n<b></b>',
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text='✅ Qabul qilish', callback_data=f'admin_qabul_{user_id}_karta'), InlineKeyboardButton(text='❌ Bekor qilish', callback_data=f'admin_bekor_{user_id}_karta')]
                        ]
                    )
                )
            except Exception as e:
                logging.info(f'Adminga xabar yuborishda xatolik: {e}')    

            await loading.delete()
            await message.answer(
                text='<b>🔜 Tez orada sizga xabar beramiz.</b>',
                reply_markup=ReplyKeyboardRemove()
            )    

        elif message.document:
            if message.document.mime_type in ("application/pdf", "image/jpeg", "image/png"):
                loading = await message.answer(text='<b>Buyurtmangiz qabul qilinmoqda...</b>')
                await asyncio.sleep(2)
                try:
                    await bot.send_location(
                        chat_id=ADMIN_ID,
                        latitude=locatsiya.latitude,
                        longitude=locatsiya.longitude
                    )
                    await bot.send_document(
                        chat_id=ADMIN_ID,
                        document=f"{message.document.file_id}",
                        caption='📁 <b>To\'lov ma\'lumoti</b>'
                    )
                    await bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f'{response}\n\n🙍 <b>Buyurtma egasi: </b><a href="{urls}">{name}</a>\n<b>📲 Telefon raqami: </b>{tel}\n💵<b> Umumiy narx:</b> {total_prices:.2f} so\'m\n<b>💳 To\'lov turi:</b> karta\n<b></b>',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text='✅ Qabul qilish', callback_data=f'admin_qabul_{user_id}_karta'), InlineKeyboardButton(text='❌ Bekor qilish', callback_data=f'admin_bekor_{user_id}_karta')]
                            ]
                        )
                    )
                except Exception as e:
                    logging.info(f'Adminga xabar yuborishda xatolik: {e}')    

                await loading.delete()
                await message.answer(
                    text='<b>🔜 Tez orada sizga xabar beramiz.</b>',
                    reply_markup=ReplyKeyboardRemove()
                )

            else:
                await message.reply("📲 <b>To\'lovni amalga oshirib to\'lov qilganingiz haqidagi chek yoki screenshotni jo\'nating.</b>")
        else:
            await message.reply(text='📲 <b>To\'lovni amalga oshirib to\'lov qilganingiz haqidagi chek yoki screenshotni jo\'nating.</b>')


@dp.message(F.text == '📋 Mening buyurtmalarim')
async def Buyurtmalar(message: Message):
    user_id = message.from_user.id
    unconfirmed_orders = Tasdiqlanmagan(user_id)
    
    if unconfirmed_orders[0]:
        await message.answer(
            text=f'''
                📥 <b>Savatingizda tasdiqlanmagan {unconfirmed_orders[0]} ta buyurtma mavjud!</b>⚠️
(Iltimos avval buyurtmani tasdiqlang )
            ''',
            reply_markup=menyu
        )
        return

    orders = ReadDb('main_buyurtmalar')
    
    if any(user[3] == user_id for user in orders):
        prices = []
        response = '\n\n🍱 <b>Sizning buyurtmangiz:</b>'
        current_data = ''
        current_tur = ''
        current_status = ''

        for user in orders:
            if user[3] == user_id:
                if user[1] != current_data:
                    if current_data:
                        total_prices = sum(prices)
                        date_now = current_data.split()[0]
                        time_now = current_data.split()[1]
                        dt = datetime.strptime(date_now, "%Y-%m-%d")
                        date = dt.strftime("%d-%m-%Y")
                        try:
                            await message.answer(
                                text=f"{response}\n<b>💵 Umumiy narx:</b> {total_prices:.2f} so\'m\n📌 <b>Buyurtma berilgan sana:</b> {date} ({time_now})\n💳 <b>To'lov turi: </b>{current_tur}\n\n📦 <b>Buyurtmangiz holati:</b> {current_status}",
                                reply_markup=menyu
                            )
                        except Exception as e:
                            logging.info(f'Xabar yuborishda xatolik: {e}')
                    
                    # Reset for the new data
                    response = '\n\n🍱 <b>Sizning buyurtmangiz:</b>'
                    prices = []
                    current_data = user[1]
                    
                response += f'\n       <b>{user[4]}</b> - {user[5]} ta'
                prices.append(user[7])
                current_tur = user[8]
                current_status = user[9]
        
        # Don't forget to handle the last batch
        if current_data:
            total_prices = sum(prices)
            date_now = current_data.split()[0]
            time_now = current_data.split()[1]
            dt = datetime.strptime(date_now, "%Y-%m-%d")
            date = dt.strftime("%d-%m-%Y")
            try:
                await message.answer(
                    text=f"{response}\n<b>💵 Umumiy narx:</b> {total_prices:.2f} so\'m\n📌 <b>Buyurtma berilgan sana:</b> {date} ({time_now})\n💳 <b>To'lov turi: </b>{current_tur}\n\n📦 <b>Buyurtmangiz holati:</b> {current_status}",
                    reply_markup=menyu
                )
            except Exception as e:
                logging.info(f'Xabar yuborishda xatolik: {e}')
    else:
        await message.answer(
            text='<b>🚫 Siz buyurtma qilmagansiz!</b>',
            reply_markup=menyu
        )



@dp.message(F.text == '❌ Bekor qilish')
async def BekorQilish(message: Message):
    user_id = message.from_user.id
    table = False
    if ReadDb('main_savat'):
        for user in ReadDb('main_savat'):
            if user[2] == user_id:
                try:
                    DeleteDb('main_savat', 'user_id', user_id)
                    table = True
                except Exception as ex:
                    logging.info(f'Savatni ochirishda xatolik: {ex}')
    else:
        logging.info('savat tozalanmadi!')

    if table:
        await message.answer(
            text='⛔️ <b>Savatingiz tozalandi.</b>',
            reply_markup=menyu
        )
    else:
        await message.answer(
            text='⚠️ <b>Savatingiz tozalanmadi!</b>'
        )  


@dp.message(F.text == '🗑 Ma\'lumotlarni tozalash')
async def ClearInfo(message: Message):
    user_id = message.from_user.id

    vaxtincha = await message.answer(text='<b>Ma\'lumotlaringiz tozalanmoqda...</b>')
    Tozalash('main_savat', 'user_id', user_id)
    Tozalash('main_xabarlar', 'author_id', user_id)
    Tozalash('main_users', 'user_id', user_id)

    await asyncio.sleep(1)
    await vaxtincha.delete()
    await message.answer(text='🗑 <b>Ma\'lumotlaringiz tozalandi.</b>')
    await message.answer(
        text='/start ni bosib botni qayta ishga tushuring.',
        reply_markup=ReplyKeyboardRemove()
        )


@dp.message(F.text == '📨 Xabar yuborish')
async def Xabar(message: Message, state: FSMContext):
    await message.answer(
        text='Xabaringizni yozing:',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(xabar.text)


@dp.message(F.text, xabar.text)
async def XabarYuborish(message: Message, state: FSMContext):
    user = message.from_user.full_name
    username = message.from_user.username or 'noma\'lum'
    user_id = message.from_user.id
    text = message.text
    try:
        AddXabar(user, user_id, username, text)
        await message.answer(text='<b>Xabaringiz yuborildi</b>')
        await message.answer(
            text='Tez orada sizga aloqaga chiqishadi.',
            reply_markup=menyu
        )
        await state.clear()
    except Exception as ex:
        logging.info(f'Xabar yuborishda xatolik: {ex}')


@dp.message(F.text == '🔙 Orqaga qaytish')
async def Back(message: Message):
    await message.answer(
        text=f'🛒 {html.bold("Asosiy Menyu")}',
        reply_markup=menyu
    )
    

@dp.message(F.text == '⚙️ Sozlamalar')
async def Sozlamalar(message: Message):
    await message.answer(
        text='📋 | <b>Sozlamalar bo\'limiga hush kelibsiz</b>',
        reply_markup=settings
    )


@dp.message(F.text == '📞 Aloqa')
async def Aloqa(message: Message):
    await message.answer_photo(
        photo='https://www.sostav.ru/app/public/images/news/2017/11/13/compressed/Depositphotos_10302425_m-2015.jpg',
        caption='''
          <b>Kontaktlar</b>
<b>Call-центр</b>

+998 71-203-12-12
+998 71-203-55-55
<b>Yetkazib berish telefon raqamlar:</b>

Toshkent: +998 71-203-12-12
Namangan: +998 78-147-12-12
Farg`ona: +998 73-249-12-12
Qo`qon: +998 73-542-78-78
Andijon: +998 74-224-12-12
Samarqand: +998 78-129-16-16
Qarshi: +998 78-129-17-17
      ''',
      reply_markup=menyu
    )


@dp.message(F.text == 'ℹ️ Biz haqimizda')
async def About(message: Message):
    await message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=0eb780f68c29968eeea710708454450427dcba93-12715110-images-thumbs&n=13',
        caption='''
                <b>Kompaniyamizning birinchi filiali 2006 yilda ochilgan bo’lib, shu kungacha muvaffaqiyatli faoliyat yuritib kelmoqdaligini bilarmidingiz?</b> 
15 yil davomida kompaniya avtobus bekatidagi kichik ovqatlanish joyidan zamonaviy, kengaytirilgan tarmoqqa aylandi, u bugungi kunda O‘zbekiston bo‘ylab 60 dan ortiq restoranlarni, o‘zining eng tezkor yetkazib berish xizmatini, zamonaviy IT-infratuzilmasini va 2000 dan ortiq xodimlarni o‘z ichiga oladi.
        ''',
        reply_markup=menyu
    )


@dp.message(Command('info'))
async def About(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=0eb780f68c29968eeea710708454450427dcba93-12715110-images-thumbs&n=13',
        caption='''
                <b>Kompaniyamizning birinchi filiali 2006 yilda ochilgan bo’lib, shu kungacha muvaffaqiyatli faoliyat yuritib kelmoqdaligini bilarmidingiz?</b> 
15 yil davomida kompaniya avtobus bekatidagi kichik ovqatlanish joyidan zamonaviy, kengaytirilgan tarmoqqa aylandi, u bugungi kunda O‘zbekiston bo‘ylab 60 dan ortiq restoranlarni, o‘zining eng tezkor yetkazib berish xizmatini, zamonaviy IT-infratuzilmasini va 2000 dan ortiq xodimlarni o‘z ichiga oladi.
        ''',
        reply_markup=menyu
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")   
