import telebot
import requests
from config import bot_token, api_url, whitelist

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("Сокращение ссылок")
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Сокращение ссылок")
def menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    shorten_button = telebot.types.InlineKeyboardButton("Сократить ссылку", callback_data="shorten")
    stats_button = telebot.types.InlineKeyboardButton("Статистика ссылки", callback_data="stats")
    markup.add(shorten_button, stats_button)
    bot.send_message(
        message.chat.id,
        "Выберите действие:\n1. Сократить ссылку\n2. Посмотреть статистику (доступно для избранных пользователей)",
        reply_markup=markup,
    )

@bot.callback_query_handler(func=lambda call: call.data == "shorten")
def ask_for_url(call):
    bot.send_message(call.message.chat.id, "Отправьте ссылку, которую нужно сократить.")
    bot.register_next_step_handler(call.message, handle_shorten_url)

def handle_shorten_url(message):
    original_url = message.text
    try:
        response = requests.post(f'{api_url}/shorten', json={"original_url": original_url})
        if response.status_code == 200:
            short_url = response.json().get("short_url")
            bot.send_message(message.chat.id, f"Сокращённая ссылка: {short_url}")
        else:
            bot.send_message(message.chat.id, "Ошибка при сокращении ссылки. Попробуйте снова.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "stats")
def ask_for_stats(call):
    if call.message.chat.id not in whitelist:
        bot.send_message(call.message.chat.id, "У вас нет доступа к статистике.")
        return

    bot.send_message(call.message.chat.id, "Введите короткую ссылку для получения статистики.")
    bot.register_next_step_handler(call.message, handle_stats_request)

def handle_stats_request(message):
    short_url = message.text
    # Извлечение short_id из ссылки
    if short_url.startswith("http"):
        short_id = short_url.rsplit('/', 1)[-1]  
        print(short_url, short_id)
    else:
        bot.send_message(message.chat.id, "Неверный формат ссылки. Попробуйте снова.")
        return

    try:
        response = requests.get(f"{api_url}/stats/{short_id}")
        print(response.text)
        if response.status_code == 200:
            stats = response.json()
            bot.send_message(
                message.chat.id,
                f"Статистика ссылки:\nОригинальная ссылка: {stats['original_url']}\n"
                f"Короткий ID: {stats['short_id']}\nКоличество переходов: {stats['clicks']}",
            )
        else:
            bot.send_message(message.chat.id, "Ссылка не найдена. Проверьте её и попробуйте снова.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


bot.polling()
