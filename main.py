# -*- coding: utf-8 -*-
import sqlite3

class Menu():
    def __init__(self, choice="0"):
        print("Телефонный справочник:")
        self.choice = choice

    def init_menu(self):
        self.choice = input("""Чтобы выбрать действие введите цифру:\n
                        1 - Добавить абонента;
                        2 - Удалить абонента по id;
                        3 - Редактировать абонента по id;
                        4 - Вывести список абонентов;
                        5 - поиск абонентов по имени и фамилии;
                        6 - выход.
                        """)

class PersonProcessing():
    def __init__(self):
        connect = sqlite3.connect("phoneBook.db")
        cursor = connect.cursor()
        print("отработали")
        self.connect = connect
        self.cursor = cursor


        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Persons
                           (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            name VARCHAR(20), surname VARCHAR(20), phone VARCHAR(20))
                            """)


    def AddPerson(self):
        print("Добавление абонента")
        name = input("Введите имя: ")
        surname = input("Введите фамилию: ")
        phone = input("Введите телефон: ")
        data = (name, surname, phone)
        self.cursor.execute("INSERT INTO Persons (name, surname, phone) VALUES (?, ?, ?)", data)
        self.connect.commit()
        input("Данные добавлены, нажмите Enter чтобы продолжить")
        print()

    def DeletePerson(self):
        print("Удаление абонента")
        id = int(input("введите id удаляемого абонента:"))
        self.cursor.execute("SELECT * FROM Persons WHERE id = %d" % id)
        temp_list = self.cursor.fetchall()
        if len(temp_list) > 0:
            self.cursor.execute("DELETE FROM Persons WHERE id = %d" % id)
            self.connect.commit()
            print("абонент", temp_list, "удален")
        else:
            input("такого id не существует, нажмите Enter чтобы продолжить")


    def EditPerson(self):
        print("редактирование абонента")
        id = ""
        while id != "q":
            id = input("введите id редактируемого абонента:")
            if id != "q":
                try:
                    id = int(id)
                    break
                except ValueError:
                    print("Введите корректный id \n"
                          "для выхода из этого меню введите q")

        self.cursor.execute("SELECT * FROM Persons WHERE id = ?", (id,))
        temp_list = self.cursor.fetchall()
        if len(temp_list) > 0:
            print("Изменяемые данные:", "\n",
                  "1.", "name:", temp_list[0][1], "\n",
                  "2.", "surname:", temp_list[0][2], "\n",
                  "3.", "phone:", temp_list[0][3])

            choice = input("Введите цифровое обозначение поля \n"
                           "которое хотите редактировать")
            print("если хотите выйти из меню редактирования введите q")

            while choice != "q":
                if choice == "1":
                    print("Редактируем поле \"name\"")
                    new_name = input("Введите новое имя записи: ")
                    if new_name == "q":
                        break
                    self.cursor.execute("""UPDATE Persons SET name = ?
                                           WHERE id = ?""", (new_name, id,))
                    self.connect.commit()
                    break
                    
                elif choice == "2":
                    print("Редактируем поле \"surname\"")
                    new_surname = input("Введите новую фамилию записи: ")
                    if new_surname == "q":
                        break
                    self.cursor.execute("""UPDATE Persons SET surname = ?
                                           WHERE id = ?""", (new_surname, id,))
                    self.connect.commit()
                    break

                elif choice == "3":
                    print("Редактируем поле \"phone\"")
                    new_phone = input("Введите новый телефон записи: ")
                    if new_phone == "q":
                        break
                    self.cursor.execute("""UPDATE Persons SET phone = ?
                                           WHERE id = ?""", (new_phone, id,))
                    self.connect.commit()
                    break

                elif choice == "q":
                    break

                else:
                    print("Такого поля нет, введите правильную цифру")
                    break

        else:
            input("такого id не существует, нажмите Enter чтобы продолжить")


    def ListOfAbonents(self):
        self.cursor.execute("SELECT id, name, surname, phone FROM Persons ORDER BY id")
        result_list = self.cursor.fetchall()
        if len(result_list) == 0:
            print("Список абонентов пуст")
            input("нажмите Enter чтобы продолжить")

        else:
            print("%-15s%-30s%-30s%-30s" % ("id", "name", "surname", "phone"))
            print()

            for cortej in result_list:

                print("%-15d%-30s%-30s%-30s" % (cortej[0], cortej[1], cortej[2], cortej[3]))

            print()
            input("нажмите Enter чтобы продолжить")
        print()

    def FindByName(self):
        print("ищем по имени или фамилии")
        choice = ""
        while choice != "q":

            choice = input("Выберите цифру 1 или 2 по какому полю будем искать:\n"
                           "1. поиск по имени;\n"
                           "2. поиск по фамилии")

            if choice == "1":

                search_name = input("Введите часть имени сначала или имя целиком для поиска")

                if search_name == "":
                    print("вы ввели пустой поисковой запрос")
                    choice = input("для выхода из поиска нажмите q\n"
                                   "для продолжения нажмите Enter")
                else:

                    self.cursor.execute("SELECT * FROM Persons WHERE name LIKE ?", (search_name + '%',))
                    result_list = self.cursor.fetchall()

                    if len(result_list) > 0:
                        print("вот что удалось найти:")
                        print(result_list)
                        input("для продолжения нажмите Enter")
                        break

                    else:
                        print("по запросу %s ничего не найдено" % search_name)
                        choice = input("для выхода из поиска нажмите q\n"
                              "для продолжения нажмите Enter")

            elif choice == "2":

                search_surname = input("Введите часть фамилии сначала или фамилию целиком для поиска")

                if search_surname == "":

                    print("вы ввели пустой поисковой запрос")
                    choice = input("для выхода из поиска нажмите q\n"
                                   "для продолжения нажмите Enter")
                else:

                    self.cursor.execute("SELECT * FROM Persons WHERE surname LIKE ?", (search_surname + '%',))
                    result_list = self.cursor.fetchall()

                    if len(result_list) > 0:
                        print("вот что удалось найти:")
                        print(result_list)
                        input("для продолжения нажмите Enter")
                        break

                    else:
                        print("по запросу %s ничего не найдено" % search_surname)
                        choice = input("для выхода из поиска нажмите q\n"
                                       "для продолжения нажмите Enter")





m = Menu()

p = PersonProcessing()

while m.choice != "6":
    m.init_menu()

    if m.choice == "1":
        p.AddPerson()
    elif m.choice == "2":
        p.DeletePerson()
    elif m.choice == "3":
        p.EditPerson()
    elif m.choice == "4":
        p.ListOfAbonents()
    elif m.choice == "5":
        p.FindByName()
    elif m.choice == "6":

        print("Вы вышли из программы.")

    else:
        print("Введите корректный запрос")



