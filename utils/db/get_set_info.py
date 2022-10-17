import json

from loader import db

"""users"""


async def is_user_exist(cid):
    if db.fetchone(f'SELECT * FROM users WHERE cid="{cid}"'):
        return True
    else:
        return False


def create_user(cid, user_name):
    db.query(f'INSERT INTO users (cid, user_name) VALUES ("{cid}", "{user_name}")')


def get_user(cid):
    return db.fetchone(f'SELECT * FROM users WHERE cid={cid}')


def get_all_users():
    return db.fetchall(f'SELECT * FROM users')


def create_way(way, price):
    try:
        db.query('DELETE FROM ways WHERE way=?', (way))
    except:
        pass
    try:
        way_id = get_ways()[-1][0] + 1
    except:
        way_id = 1
    db.query('INSERT INTO ways VALUES (?, ?, ?)', (way_id, way, price))


def get_ways():
    return db.fetchall('SELECT * FROM ways')


def get_way_by_id(wid):
    try:
        return db.fetchone('SELECT * FROM ways WHERE way_id=?', (wid,))
    except Exception as e:
        print(e)