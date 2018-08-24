# -*- coding: utf-8 -*-
#скрипт для тестов

import sqlite3

connect = sqlite3.connect("phoneBook.db")
cursor = connect.cursor()

try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS Persons
                               (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                name VARCHAR(20), surname VARCHAR(20), phone VARCHAR(20))
                                """)
except sqlite3.OperationalError:
    print("таблица уже существует")

cursor.execute("""INSERT INTO Persons (name, surname, phone)
                  VALUES ('Алекс', '', '+375296854589')
                """)
data = ('jora', 'fokin', '+375296542589')
cursor.execute("INSERT INTO Persons (name, surname, phone) VALUES ('jora', 'fokin', '123456')")
name = 'Ura'
surname = 'Urin'
phone = '123456'
cursor.execute("INSERT INTO Persons (name, surname, phone) VALUES (?, ?, ?)" , data)

connect.commit()
connect.close()