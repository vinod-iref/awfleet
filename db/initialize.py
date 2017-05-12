# Create required Database & Tables
import squite3

conn = sqlite3.connect('fleet.db')

c = conn.cursor()

c.execute("CREATE TABLE spotprice(id INT PRIMARY KEY NOT NULL,size TEXT NOT NULL, price INT NOT NULL, dateline INT NOT NULL)")

c.execute("CREATE INDEX timestamp ON spotprice (dateline);")

conn.commit()

conn.close()