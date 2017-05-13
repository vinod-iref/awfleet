# Create required Database & Tables
import sqlite3

conn = sqlite3.connect('fleet.db')

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS spotinstance")
c.execute("CREATE TABLE spotinstance "
          "  ( "
          "     id      TEXT PRIMARY KEY NOT NULL, "
          "     price   REAL NOT NULL, "
          "     service TEXT NOT NULL, "
          "     datelie INT NOT NULL, "
          "     is_up   INT NOT NULL "
          "  )")

c.execute("DROP TABLE IF EXISTS ondemand")
c.execute("CREATE TABLE ondemand "
          "  ( "
          "     id      TEXT PRIMARY KEY NOT NULL, "
          "     price   REAL NOT NULL, "
          "     service TEXT NOT NULL, "
          "     datelie INT NOT NULL, "
          "     is_up   INT NOT NULL "
          "  )")

conn.commit()

conn.close()