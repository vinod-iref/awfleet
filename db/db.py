import sqlite3
import time

class SPOT_PRICE():
	def __init__(self, db_name):
		self.conn = sqlite3.connect(db_name)
		self.cursor = self.conn.cursor()
		self.table_name = "spotprice"
		self.sizes = ['m4.large']

	def insert(price,size=None,dateline=None):
		if dateline == None:
			dateline =  int(time.time())

		if size in self.sizes:
			self.cursor.execute("INSERT INTO %s VALUES ")
		else:
			return None

	def delete():
		pass

	def update():
		pass
		