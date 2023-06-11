import sqlite3
import time
import requests
from bot_settings import db_name, url_status_status_statement

"""подключение базы данных"""
db_connect = sqlite3.connect(db_name, check_same_thread=False)
db_cursor = db_connect.cursor()

#генерация таблицы Статус заявки (использовать если нужно сгенгерировать таблицу)
def create_status_table():
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS numb_status_statement(
                id INTEGER PRIMARY KEY,
                statement_number TEXT,
                statement_status TEXT
                );
        """)

    db_connect.commit()

#генерация таблицы Контакты НТП (использовать если нужно сгенгерировать таблицу)
def create_NTP_table():
    db_connect.execute(
    """
    CREATE TABLE IF NOT EXISTS contact_NTP(
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                phones TEXT,
                mail TEXT 
                );
    """)
    db_connect.commit()

#генерация таблицы Обратной связи (использовать если нужно сгенгерировать таблицу)
def create_feed_back_table():
    db_connect.execute(
    """
    CREATE TABLE IF NOT EXISTS feed_back(
                id INTEGER PRIMARY KEY,
                date TEXT,
                username TEXT,
                feed_back TEXT
                );
    """)
    
#добавления информации в базу данных Статус заявки
def post_statement(number, status): 
    values = [(None, number, status)] 
    db_cursor.executemany('insert into numb_status_statement values (?, ?, ?)', values)
    
    db_connect.commit()

#добавление информации в базу данных NTP Контакты
def post_NTP_contscts(full_name,phone_number, email):
    values = [(None, full_name, phone_number, email)]
    db_cursor.executemany('insert into contact_NTP values (?, ?, ?, ?)', values)
    
    db_connect.commit()

#добавление информации в базу данных ФидБек
def post_feed_back(date_message, username, feed_back):
    
    #конвертация времени
    date_message = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(date_message))
    
    values = [(None, date_message, username, feed_back)]
    db_cursor.executemany('insert into feed_back values (?, ?, ?, ?)', values)
    db_connect.commit()

#Получение информации по заявке
def get_status_statement(number):
    
    url = url_status_status_statement + str(number)
    status = requests.get(url)
    
    print(f"{type(status)=}, {status=}, {status=}")
    
    status = None
    
    if status == None:
        status = "Номер заявки не найден \n Проверьте на наличие ошибки и попробуйте снова"
    return status

#Получение информации по заявке с локальной базы данных
def get_local_dbstatus_statement(number):
    status = db_cursor.execute('SELECT statement_status FROM numb_status_statement WHERE statement_number ==? ', (f'{number}',)).fetchone()
    if status == None:
        status = "Номер заявки не найден \n Проверьте на наличие ошибки и попробуйте снова"
    return status

#Получение всех контактов
def get_contact_NTP():
    
    all_contacts = db_cursor.execute("SELECT * from contact_NTP").fetchall()
    answer = text_converter(all_contacts=all_contacts)
    return answer

"""Структура контакта
    (0)id
    (1)ФиО
    (2)Номер телефона
    (3)Почта
"""
#Форматирование текста
def text_converter(all_contacts):
    
    answer = ""
    quantity_contacts = len(all_contacts)
    
    for index in range(quantity_contacts):
        contact = all_contacts[index-1]
        full_name = contact[1]
        phone_number = contact[2]
        email_adress = contact[3]
        сurrent_contact = f"{full_name}\n{phone_number}\n{email_adress}\n\n"
        answer = answer + сurrent_contact
        
    return answer