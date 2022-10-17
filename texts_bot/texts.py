from utils.db.get_set_info import get_way_by_id

choice_date = 'Выберите дату поездки'
choice_trip = 'Выберите направление'
choice_count = 'Выберите желаемое количество мест'
choice_count_need_more_text = 'Введите желаемое количество мест'
choice_count_need_more = 'Нужно больше мест'
count_error = 'Неверное количество, введите еще раз'
enter_phone = 'Введите данные пассажира: +79177777777'
enter_phone2 = 'Введите данные пассажира {number}: +79177777777'
enter_fio = 'Введите данные пассажира: "Фамилия Имя Отчество"'
enter_fio2 = 'Введите данные пассажира {number}: "Фамилия Имя Отчество"'
phone_error_text = 'Некорректный номер, повторите ввод'
fio_error_text = 'Некорректное ФИО, повторите ввод'


def get_emoji_number(number):
    numbers = {'0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
               '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'}
    res = ''
    for i in str(number):
        res += numbers[i]
    return res


check = 'Проверьте данные'


def choice_text(args, step):
    available_args = [i for i in args]
    s = ''
    if 'date' in available_args and step > 0:
        s += f'\nДата: {args["date"]}'
    if 'way_id' in available_args and step > 1:
        s += f'\nНаправление: {get_way_by_id(args["way_id"])[1]}'
    if 'count' in available_args and step > 2:
        s += f'\nПассажиров: {args["count"]}'
        price = get_way_by_id(args["way_id"])[2] * args["count"]
        s += f'\nСтоимость поездки: {price} рублей'
    if 'names' in available_args and 'phones' in available_args and step > 3:
        for i in args['names']:
            s += f'\n\nПассажир {get_emoji_number(i)}:\nФИО: <b>{args["names"][i]}</b>\nНомер телефона: <b>{args["phones"][i]}</b>'
    return s + '\n\n'