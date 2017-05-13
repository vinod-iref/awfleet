import sqlite3
import time

class DB():
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def instance_up(self, table, _id, price, service):
        dateline = int(time.time())
        self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?)".format(table), (_id, price, service, dateline,1))
        self.conn.commit()

    def get_instances(self, table):
        return [value for value in self.cursor.execute("SELECT * FROM {} WHERE is_up=?".format(table), (1,))]

    def instance_down(self, table, _id):
        self.cursor.execute("UPDATE {} SET is_up=?".format(table), (0,))
        self.conn.commit()

