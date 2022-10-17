from utils.db.get_set_info import create_way
from utils.google_sheets.get_set_info_sheets import get_table, paint_table

if __name__ == '__main__':
    ranges = f'Уфа-Мск!B3:B3'
    paint_table(1661131174, 1)