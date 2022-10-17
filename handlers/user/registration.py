from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP, WYearTelegramCalendar
from filters import IsUser
from handlers.user.utils import set_info_in_table, check_phone, check_fio

from keyboards.default.markups import *
from loader import dp, bot
from states import RegistrationState
from texts_bot.texts import *
from utils.db.get_set_info import get_ways
from utils.google_sheets.get_set_info_sheets import get_table


class MyStyleCalendar(WYearTelegramCalendar):
    # previous and next buttons style. they are emoji now!
    prev_button = "⬅️"
    next_button = "➡️"
    # you do not want empty cells when month and year are being selected
    empty_month_button = "✖️"
    empty_year_button = "✖️"


@dp.message_handler(IsUser(), commands=registration, state='*')
async def process_registration(message: Message, state: FSMContext):
    await state.finish()
    await RegistrationState.date.set()

    calendar, step = MyStyleCalendar(locale='ru', min_date=datetime.date(datetime.today())).build()
    #result, key, step = DetailedTelegramCalendar(locale='ru').process(query)
    if LSTEP[step] == 'year':
        step_ = 'год'
    elif LSTEP[step] == 'month':
        step_ = 'месяц'
    else:
        step_ = 'день'
    await message.answer(f"Выберите {step_} поездки", reply_markup=calendar)


trip_cb = CallbackData('somearg', 'way_id', 'action')


@dp.callback_query_handler(IsUser(), DetailedTelegramCalendar.func(), state=RegistrationState.date)
async def cal(query: CallbackQuery, state: FSMContext):
    result, key, step = MyStyleCalendar(locale='ru', min_date=datetime.date(datetime.today())).process(query.data)
    if not result and key:
        if LSTEP[step] == 'year':
            step_ = 'год'
        elif LSTEP[step] == 'month':
            step_ = 'месяц'
        else:
            step_ = 'день'
        await query.message.edit_text(f"Выберите {step_} поездки", reply_markup=key)
    elif result:
        async with state.proxy() as data:
            data['date'] = result
            data['number'] = 1
            args = data
        print(result)
        await RegistrationState.trip.set()
        ways = get_ways()
        markup = InlineKeyboardMarkup()
        for i in ways:
            markup.add(InlineKeyboardButton(f'{i[1]} {i[2]}', callback_data=trip_cb.new(way_id=i[0], action='choice_trip')))
        markup.add(InlineKeyboardButton(cancel_message, callback_data=trip_cb.new(way_id=0, action='cancel')))
        await query.message.edit_text(choice_text(args, 1) + choice_trip, reply_markup=markup)


count_cb = CallbackData('somearg', 'count', 'action')


@dp.callback_query_handler(IsUser(), trip_cb.filter(action='choice_trip'), state=RegistrationState.trip)
async def process_choice_trip(query: CallbackQuery, state: FSMContext, callback_data: dict):
    async with state.proxy() as data:
        data['way_id'] = callback_data['way_id']
        print('way_id', data['way_id'])
        args = data
    markup = InlineKeyboardMarkup()
    for i in range(5):
        markup.add(InlineKeyboardButton(f'{i+1}', callback_data=count_cb.new(count=i+1, action='choice_count')))
    markup.add(InlineKeyboardButton(choice_count_need_more, callback_data=count_cb.new(count=10, action='choice_count_need_more')))
    markup.add(InlineKeyboardButton(cancel_message, callback_data=count_cb.new(count=0, action='cancel')))
    await RegistrationState.count.set()
    await query.message.edit_text(choice_text(args, 2) + choice_count, reply_markup=markup)


@dp.callback_query_handler(IsUser(), trip_cb.filter(action='cancel'), state=RegistrationState.trip)
async def process_choice_trip_cancel(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()
    await query.message.edit_text('Отменено')


@dp.callback_query_handler(IsUser(), count_cb.filter(action='choice_count'), state=RegistrationState.count)
async def process_choice_count(query: CallbackQuery, state: FSMContext, callback_data: dict):
    async with state.proxy() as data:
        count = data['count'] = int(callback_data['count'])
        print('count', data['count'], count)
        number = data['number']
        args = data
    await RegistrationState.phone.set()
    await query.message.delete()
    if count > 1:
        await query.message.answer(choice_text(args, 3) + enter_phone2.replace('{number}', get_emoji_number(number)), reply_markup=cancel_markup())
    else:
        await query.message.answer(choice_text(args, 3) + enter_phone, reply_markup=cancel_markup())


@dp.callback_query_handler(IsUser(), count_cb.filter(action='cancel'), state=RegistrationState.count)
async def process_choice_count_cancel(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.finish()
    await query.message.edit_text('Отменено')


@dp.callback_query_handler(IsUser(), count_cb.filter(action='choice_count_need_more'), state=RegistrationState.count)
async def process_choice_count_need_more(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await RegistrationState.count_need_more.set()
    async with state.proxy() as data:
        args = data
    await query.message.delete()
    await query.message.answer(choice_text(args, 2) + choice_count_need_more_text, reply_markup=cancel_markup())


@dp.message_handler(IsUser(), lambda message: message.text not in [cancel_message], state=RegistrationState.count_need_more)
async def process_count_need_more(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['count'] = int(message.text)
            print('count', data['count'])
            data['number'] = 1
    except:
        await message.answer(count_error, reply_markup=cancel_markup())


@dp.message_handler(IsUser(), text=cancel_message, state=RegistrationState.count_need_more)
async def process_count_need_more_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


'''Phone'''


@dp.message_handler(IsUser(), lambda message: message.text not in [cancel_message], state=RegistrationState.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = check_phone(message.text)
    print(phone)
    if phone != 0:
        async with state.proxy() as data:
            number = data['number']
            try:
                data['phones'][number] = phone
            except:
                data['phones'] = {number: phone}
            count = data['count']
            args = data
        await RegistrationState.name.set()
        if count > 1:
            await message.answer(choice_text(args, 3) + enter_fio2.replace('{number}', get_emoji_number(number)))
        else:
            await message.answer(choice_text(args, 3) + enter_fio)
    else:
        await message.answer(phone_error_text)


@dp.message_handler(IsUser(), text=cancel_message, state=RegistrationState.phone)
async def process_phone_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsUser(), lambda message: message.text not in [cancel_message], state=RegistrationState.name)
async def process_name(message: Message, state: FSMContext):
    if check_fio(message.text):
        async with state.proxy() as data:
            number = data['number']
            try:
                data['names'][number] = message.text
            except:
                data['names'] = {number: message.text}
            phones = data['phones']
            count = data['count']
            way_id = data['way_id']
            date = data['date']
            args = data
        if count > number >= 1:
            async with state.proxy() as data:
                number = data['number'] = data['number'] + 1
            await RegistrationState.phone.set()
            await message.answer(choice_text(args, 3) + enter_phone2.replace('{number}', get_emoji_number(number)))
        else:
            await RegistrationState.confirm.set()
            s = check
            s += choice_text(args, 4)
            await message.answer(s, reply_markup=check_markup())
    else:
        await message.answer(fio_error_text)


@dp.message_handler(IsUser(), text=cancel_message, state=RegistrationState.name)
async def process_name_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsUser(), text=confirm_message, state=RegistrationState.confirm)
async def process_confirm(message: Message, state: FSMContext):
    async with state.proxy() as data:
        number = data['number']
        phones = data['phones']
        count = data['count']
        way_id = data['way_id']
        date = data['date']
        print(data)
        args = data
    await state.finish()
    s = check
    s += choice_text(args, 4)
    set_info_in_table(args)
    await message.answer('Сохранено\n\n' + s, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsUser(), text=cancel_message, state=RegistrationState.confirm)
async def process_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


