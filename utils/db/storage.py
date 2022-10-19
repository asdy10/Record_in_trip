import sqlite3 as lite
import threading

lock = threading.Lock()


class DatabaseManager(object):

    def __init__(self, path):
        self.conn = lite.connect(path, check_same_thread=False)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS users (cid TEXT, user_name TEXT, ref TEXT)')
        self.query('CREATE TABLE IF NOT EXISTS ways (way_id INT PRIMARY KEY, way TEXT, price INT)')

    def query(self, arg, values=None):
        with lock:
            if values == None:
                self.cur.execute(arg)
            else:
                self.cur.execute(arg, values)
            self.conn.commit()

    def fetchone(self, arg, values=None):
        with lock:
            if values == None:
                self.cur.execute(arg)
            else:
                self.cur.execute(arg, values)
            return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        with lock:
            if values == None:
                self.cur.execute(arg)
            else:
                self.cur.execute(arg, values)
            return self.cur.fetchall()

    def __del__(self):
        self.conn.close()


'''

users: cid int, user_name text, balance float, referal int, buyouts int, reviews int, discount int, ref_percent float, ref_bonus float

buyout templates: cid int, idt int, link text, keywords text, count_products int, address text, date_buyouts text

buyouts: cid int, idx int, link text, keywords text, count_products int, cost float,
         address text, date_buyouts text, status text, review bool, bid int, new_price float

reviews: idx int, message text, date_review text, images text

browsers: bid int, phone text, proxy text, user_agent text, payment text, token text, discount float

graph: cid int, idt text, gid text, count int, date text, price float, completed bool

bot_data: discount float, payment text, token text

referals: cid int, idx text, profit text, date text

'''
