import telebot
import re  # Импортируем модуль для работы с регулярными выражениями
from config import token  # Импорт токена

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:  # Проверка на то, что эта команда была вызвана в ответ на сообщение
        chat_id = message.chat.id  # Сохранение id чата
        # Сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        # Проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)  # Пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

# проверка на ссылку в тексте
@bot.message_handler(func=lambda message: True)
def check_for_links(message):
    if re.search(r'https?://S+', message.text):  
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        
        # пользователь не админ или создатель
        if user_status != 'administrator' and user_status != 'creator':
            bot.ban_chat_member(chat_id, user_id)  # Баним пользователя
            bot.send_message(chat_id, f"Пользователь @{message.from_user.username} был забанен за отправку ссылки.")
        else:
            bot.send_message(chat_id, "Администраторы не могут быть забанены.")

bot.infinity_polling(none_stop=True)
