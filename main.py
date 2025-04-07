import telebot
from telebot import types
import os

TOKEN = '8136889918:AAEjIo54kJ7GCVjvpqWH2mewy1zJnoVHatU'
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(f"Задание {i}") for i in range(1, 6)]  # например, 5 заданий
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите номер задания:", reply_markup=markup)


# Обработка выбора задания
@bot.message_handler(func=lambda message: message.text.startswith("Задание"))
def choose_type(message):
    task_number = message.text.split()[1]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Теория", "Домашнее задание", "Назад")

    bot.send_message(message.chat.id, f"Задание {task_number}. Что хотите посмотреть?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["Теория", "Домашнее задание", "Назад"])
def send_file(message):
    if message.text == "Назад":
        start(message)
        return

    chat_id = message.chat.id
    last_message = bot.send_message(chat_id, "Отправляю файл...")

    # Получение номера задания из предыдущего сообщения
    prev_message = bot.get_chat_history(chat_id, limit=2)[1].text
    task_number = prev_message.split()[1].strip('.')

    if message.text == "Теория":
        filename = f"Информация {task_number} задание.pdf"
        folder = "theory"
    else:
        filename = f"Домашняя работа {task_number} задание.pdf"
        folder = "homework"

    file_path = os.path.join('files', folder, filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
    else:
        bot.send_message(chat_id, "Файл не найден.")

    bot.delete_message(chat_id, last_message.id)


bot.infinity_polling()
