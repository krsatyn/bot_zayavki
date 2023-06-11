# -*- coding: utf-8 -*
import telebot
import sqlite3

from telebot import types

from bot_settings import bot_token, db_name
from database_function import get_status_statement, get_contact_NTP, post_feed_back, get_local_dbstatus_statement
#Ключ слово используется для контроля текущей задачи (задача назначается кнопкой)
KEY_WORD = ""

"""подключение базы данных"""
db_connect = sqlite3.connect(db_name, check_same_thread=False)
cursor = db_connect.cursor()

token = bot_token

bot = telebot.TeleBot(token=token)

#кнопки бота
@bot.message_handler(commands=['start'])
def button(message):
    #шаблон (row_width означает количество кнопок в ряд)
    markup =types.ReplyKeyboardMarkup(row_width=1)
    #кнопки
    button_get_status = types.InlineKeyboardButton("💬Узнать статус заявки💬", callback_data='id_status')
    button_get_NTP_contacts = types.InlineKeyboardButton("⚙️Контакты НТП⚙️", callback_data='id_NTP_contacts')
    button_get_help = types.InlineKeyboardButton("💡Помощь💡", callback_data="id_help")
    button_callback =  types.InlineKeyboardButton("📬Обратная связь📬", callback_data="id_callback")
    #добавление кнопок в шаблон
    markup.add(button_get_status, button_get_NTP_contacts, button_get_help, button_callback)
    bot.send_message(message.chat.id, text="Добрый день!\nЧат бот разработан с целью упростить вам процесс запроса статуса вашей заявки.\nНажмите на кнопку <💬Узнать статус заявки💬>, и введите ваш номер.\nВ ответном сообщении вы получите статус вашей заявки. \nПриятного использования", reply_markup=markup)

#конструкция взаимодействия с ботом
@bot.message_handler(content_types=['text'])
def bot_response(message):
    
    global KEY_WORD 
    #меню возврата
    if message.text == "⬅️Вернуться назад⬅️":
        #шаблон (row_width означает количество кнопок в ряд)
        markup =types.ReplyKeyboardMarkup(row_width=1)
        #кнопки
        button_get_status = types.InlineKeyboardButton("💬Узнать статус заявки💬", callback_data='id_status')
        button_get_NTP_contacts = types.InlineKeyboardButton("⚙️Контакты НТП⚙️", callback_data='id_NTP_contacts')
        button_get_help = types.InlineKeyboardButton("💡Помощь💡", callback_data="id_help")
        button_callback =  types.InlineKeyboardButton("📬Обратная связь📬", callback_data="id_callback")
        #добавление кнопок в шаблон
        markup.add(button_get_status, button_get_NTP_contacts, button_get_help, button_callback)
        bot.send_message(message.chat.id, text="Добрый день!\n\nЧат бот разработан с целью упростить вам процесс запроса статуса вашей заявки.\n\nНажмите на кнопку <💬Узнать статус заявки💬>, и введите ваш номер.\n\nВ ответном сообщении вы получите статус вашей заявки. \n\nПриятного использования", reply_markup=markup)
    
    #получение статуса заявки
    elif message.text == "💬Узнать статус заявки💬":
        KEY_WORD = message.text
        bot.send_message(message.chat.id, text="Введите номер заявки")
        
    #получение ответа от статуса
    elif  KEY_WORD == "💬Узнать статус заявки💬":
        answer = get_status_statement(message.text)
        bot.send_message(message.chat.id, text=f"Статус вашей заявки: \n{answer[0]}")
        KEY_WORD = ""
        
    #Получение контакта НТП
    elif message.text == "⚙️Контакты НТП⚙️":
        bot.send_message(message.chat.id, text=f"Контакты:\n{get_contact_NTP()}")
    
    #вывод функционала Чат Бота
    elif message.text == "💡Помощь💡":
        bot.send_message(message.chat.id, text="Данный Чат бот разработан с целью упростить вам процесс запроса статуса вашей заявки\n\nВ его функционал входит:\n\n1)💬Узнать статус заявки💬\nС помощью этой кнопки вы можете узнать статус вашей заявки\n\n2)⚙️Контакты НТП⚙️\nС помощью данной кнопки вы можете получить <<Здесь определение этого слова>>\n\n3)💡Помощь💡\nЗдесь вы получите всю информацию о нашем боте\n\n4)📬Обратная связь📬\nЗдесь вы сможете написать что вам нравится или не нравится в нашем Боте")
    
    #форма обратной связи
    elif message.text == "📬Обратная связь📬":
        markup =types.ReplyKeyboardMarkup(row_width=1)
        button_acces = types.InlineKeyboardButton("✅Да, я хочу отправить форму обратной связи✅", callback_data="id_acces")
        button_back_menu = types.InlineKeyboardButton("⬅️Вернуться назад⬅️", callback_data="id_dack_menu")
        markup.add(button_acces, button_back_menu)
        
        bot.send_message(message.chat.id, text="Хорошо, для продолжения подтвердите, что вы хотите отправить форму обратной связи\n(Это сделанно, на случай, если вы случайно нажади сюда)", reply_markup=markup)
    
    #Начало записи после соглашения на отправку формы
    elif message.text == "✅Да, я хочу отправить форму обратной связи✅":
        bot.send_message(message.chat.id, text="Следущее ваще сообщение будет отправленно на рассмотрение технической поддержкой")
        KEY_WORD = 'post_answer'
    #запись в бд
    elif KEY_WORD == 'post_answer':
        bot.send_message(message.chat.id, text="Хорошо,  ваше сообщение отправленно и в скором времени рассмотрено\nДЛЯ ВЫХОДА ИХ ФОРМЫ ОБРАТНОЙ СВЯЗИ НАЖМИТЕ НА КНОПКУ <⬅️Вернуться назад⬅️>")
        post_feed_back(date_message=message.date, username=message.from_user.username, feed_back=message.text)
        KEY_WORD=''
        
    #Сообщение при вызове команды которой не существует
    else:
        bot.send_message(message.chat.id, text=f"❗️Выберите команду с панели❗️")
                
bot.polling()