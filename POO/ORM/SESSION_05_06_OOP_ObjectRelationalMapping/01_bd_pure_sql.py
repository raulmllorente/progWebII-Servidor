# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:26:05 2020

# SQL de SQLite - https://alvinalexander.com/android/sqlite-create-table-insert-syntax-examples
# DB Browser for SQLite - https://sqlitebrowser.org/dl/
# Sqlite dentro de Python - https://docs.python.org/2/library/sqlite3.html

@author: manoel.alonso
"""


# BASIC SQL FROM WITHIN PYTHON / SQL BÁSICO DESDE DENTRO DE PYTHON
import sqlite3

conn = sqlite3.connect('./database.db')
c = conn.cursor()


# CREATE TABLE
c.execute("""
  CREATE TABLE 
      coffees (
              id INTEGER PRIMARY KEY,
              coffee_name TEXT NOT NULL,
              price REAL NOT NULL
              );""")
conn.commit()


# INSERT TABLE
c.execute("""
     INSERT INTO 
        coffees 
     VALUES 
        (null, 'Colombian', 7.99);
""")


conn.commit()

for fila in c.execute("SELECT * FROM coffees"):
    print("id=",fila[0])
    print("Nombre=",fila[1])
    print("Precio=",fila[2])

# INSERT TABLE - MULTIPLE LINES / MULTIPLES LINEAS
c.execute("""INSERT INTO coffees VALUES 
          (null, 'French_Roast', 8.99);""")
c.execute("""INSERT INTO coffees VALUES 
          (null, 'Espresso', 9.99);""")
c.execute("""INSERT INTO coffees VALUES 
          (null, 'Colombian_Decaf', 8.99);""")
c.execute("""INSERT INTO coffees VALUES 
          (null, 'French_Roast_Decaf', 9.99);""")
conn.commit()

for fila in c.execute("SELECT * FROM coffees"):
    print("id=",fila[0])
    print("Nombre=",fila[1])
    print("Precio=",fila[2])


#UPDATE - MULTIPLE LINES / MULTIPLES LINEAS
c.execute("""UPDATE coffees SET price = 6.99 WHERE id=5;""")
c.execute("""UPDATE coffees SET price = 10.99 WHERE id=4;""")
c.execute("""UPDATE coffees SET price = 69.99 WHERE id=3;""")
conn.commit()

for fila in c.execute("SELECT * FROM coffees"):
    print("id=",fila[0])
    print("Nombre=",fila[1])
    print("Precio=",fila[2])

#DELETE - DELETING A LINE / BORRANDO UNA LINEA
c.execute("""DELETE FROM coffees WHERE id=3""")
conn.commit()

#CLOSING SESSION
conn.close()
