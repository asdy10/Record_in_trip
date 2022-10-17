from utils.db.get_set_info import get_way_by_id
from utils.google_sheets.get_set_info_sheets import get_table, update_table, clear_table


def set_info_in_table(args):
    number = args['number']
    phones = args['phones']
    names = args['names']
    count = args['count']
    way_id = args['way_id']
    way_id, way, price = get_way_by_id(way_id)
    y, m, d = str(args['date']).split('-')
    date = f'{d}.{m}.{y}'

    list_name = 'Уфа-Мск' if way.split('-')[0] == 'Уфа' else 'Мск-Уфа'
    ranges = f'{list_name}!B1:F10000'
    table = get_table(ranges)
    for i in table:
        print(i)
    pos_insert = 0
    pos_insert3 = 999999
    for i in table:
        if i:
            if date in i[0]:
                pos_date_name = table.index(i)
                try:
                    pos_insert = table.index([], pos_date_name, len(table))
                except:
                    pos_insert = len(table)
                try:
                    pos_insert2 = table.index([' '] * 5, pos_date_name, len(table))
                except:
                    pos_insert2 = len(table)
                for i in range(pos_date_name + 1, len(table)):
                    try:
                        if '2022' in table[i][0] or '2023' in table[i][0]:
                            pos_insert3 = i
                            break
                    except:
                        pass

                pos_insert = min(pos_insert, pos_insert2, pos_insert3)
                break

    if pos_insert != 0:
        # print(pos_insert)
        for i in names:
            table.insert(pos_insert, [names[i], phones[i], 'TelegBot', way, price])
        # print(table[pos_insert + 2])
        try:
            next_project = table[pos_insert + count + 1][0]
            table[pos_insert + count] = [' '] * 5
            table[pos_insert + count + 1] = [next_project] + [' '] * 4
        except Exception as e:
            print(e)

    else:
        table.insert(1, [])
        for i in names:
            table.insert(1, [names[i], phones[i], 'TelegBot', way, price])
        table.insert(1, [f'{date}'])
    color_numbers = []
    for i in range(len(table)):
        print(table[i])
        if '2022' in table[i][0] or '2023' in table[i][0]:
            color_numbers.append(i)
    #update_table([[['']]*5]*1000, ranges)
    clear_table(ranges)
    update_table(table, ranges)
    #ranges = 'Действие!B2:F10000'


def check_phone(phone):
    phone = phone.replace('+', '')
    if len(phone) == 11:
        if phone[0] not in ['7', '8']:
            return 0
        else:
            phone = phone[1:]
            phone = '8' + phone
            try:
                return int(phone)
            except:
                return 0

    elif len(phone) == 10:
        try:
            phone = '8' + phone
            return int(phone)
        except:
            return 0
    else:
        return 0


def check_fio(fio):
    try:
        _, _, _ = fio.split(' ')
        return True
    except:
        return False
