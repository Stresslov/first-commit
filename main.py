import telebot
from telebot import types
import os
import os.path

TOKEN = os.getenv('TOKEN')  # Используем переменную окружения
bot = telebot.TeleBot(TOKEN)

# Сохраняем выбранное задание для пользователя
user_task = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Задание 1-5"),
        types.KeyboardButton("Задание 6"),
        types.KeyboardButton("Задание 7"),
        types.KeyboardButton("Задание 8"),
        types.KeyboardButton("Задание 9"),
        types.KeyboardButton("Задание 10"),
        types.KeyboardButton("Задание 11"),
        types.KeyboardButton("Задание 12"),
        types.KeyboardButton("Задание 13"),
        types.KeyboardButton("Задание 14"),
        types.KeyboardButton("Задание 15"),
        types.KeyboardButton("Задание 16"),
        types.KeyboardButton("Задание 17"),
        types.KeyboardButton("Задание 18"),
        types.KeyboardButton("Задание 19")
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите номер задания:", reply_markup=markup)


# Обработка выбора задания
@bot.message_handler(func=lambda message: message.text.startswith("Задание"))
def choose_type(message):
    task_number = message.text.replace("Задание ", "").strip()
    user_task[message.chat.id] = task_number

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Теория", "Домашнее задание", "Назад")

    bot.send_message(message.chat.id, f"Задание {task_number}. Что хотите посмотреть?", reply_markup=markup)


# Обработка выбора теории или домашнего задания
@bot.message_handler(func=lambda message: message.text in ["Теория", "Домашнее задание", "Назад"])
def send_file(message):
    if message.text == "Назад":
        start(message)
        return

    chat_id = message.chat.id

    task_number = user_task.get(chat_id)
    if not task_number:
        bot.send_message(chat_id, "Пожалуйста, сначала выберите задание.")
        return

    folder = "theory" if message.text == "Теория" else "homework"
    if message.text == "Теория":
        filename = f"Информация {task_number} задание.pdf"
    else:
        filename = f"Домашняя работа {task_number} задание.pdf"

    file_path = os.path.join('files', folder, filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
    else:
        bot.send_message(chat_id, "Файл не найден.")

bot.remove_webhook()
bot.infinity_polling()
