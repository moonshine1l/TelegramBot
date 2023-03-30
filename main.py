import random

import requests
import telebot
import logging
import pyjokes
from googletrans import Translator

from telebot import types

API_TOKEN = '5907573151:AAE3qQcrIdV1Al52EOEYQ4QFcVMQ9tG5phY'

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.INFO)

storage = dict()

translator = Translator()


def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)


def set_data_storage(user_id, key, value):
    storage[user_id][key] = value


def get_data_storage(user_id):
    return storage[user_id]


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id,
                     "Привет) \nЯ - бот, который попытается поднять тебе настроение!\nДля того, чтобы узнать список игр напишите команду /help ")


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id,
                     "/numbers - Угадай число \n/rockPaperScissors - Камень, ножницы, бумага \n/cat - я отправлю тебе котика!")


@bot.message_handler(commands=['cat'])
def command_joke(message):
    stickers = ['CAACAgIAAxkBAAEIZA9kJh__l6fJR0D5PyLUpNR_roQtXAAC-hYAAn1r2Ut65pmScEboGC8E', 'CAACAgIAAxkBAAEIZBFkJiAHUxP0Q-doWXp_2gzWXKrsgwACYBsAApueiUjjNxm8QnKxFS8E', 'CAACAgIAAxkBAAEIZA1kJh_0Tz6-Mx_1EVyctTFAL8-3HwACnRQAAvoa2EsPDH0ubFMNKC8E', 'CAACAgIAAxkBAAEIZBNkJiBsr-ykXg8XNg7Ku7HsHewcYQACrSUAAkNruUnV0eYl-TGYoS8E', 'CAACAgIAAxkBAAEIZBVkJiB_SXcQ4CIhR62b52QkI3jbMgACtBUAAtIFyEvEgZTnl4Z7ay8E', 'CAACAgIAAxkBAAEIZBdkJiCOBIVv1_FXz55LT1nj0GtxmQACXxYAAgq6yUsjtyMt_mlHPi8E', 'CAACAgQAAxkBAAEIZBlkJiCoQZ8fivg_y_wc2qwYfMoLCgACOgADzjkIDWhSWwg2l986LwQ', 'CAACAgIAAxkBAAEIZBtkJiFU8XSS1YLCFIQk_YvsSEwgUwACwBYAAue6yEl3RpwBVx61_y8E', 'CAACAgIAAxkBAAEIZB1kJiFnjbM6SP7TvlNvCs2DA91D9wACnRUAAv0jQEhsZsXBxjMR1C8E', 'CAACAgIAAxkBAAEIZB9kJiF04NiNBBY6QT44TrHsAs_KIgAC2BIAAhS7OUi0ifTH5oLybS8E', 'CAACAgIAAxkBAAEIZCFkJiGJDkP-5lW5VO3cLbju2bxa7wAC6RcAApPEQUgKY9An4pR4RC8E', 'CAACAgIAAxkBAAEIZCNkJiGWgy2DWjhOemzXYD3UYp1LDgACFhMAAou-QEiilDSZ9FgpUC8E']
    bot.send_sticker(message.chat.id, random.choice(stickers))


@bot.message_handler(commands=['numbers'])
def digitgames(message):
    init_storage(message.chat.id)

    attempt = 5
    set_data_storage(message.chat.id, "attempt", attempt)

    bot.send_message(message.chat.id, f'Игра "угадай число"!\nКоличество попыток: {attempt}')

    random_digit = random.randint(1, 10)
    print(random_digit)

    set_data_storage(message.chat.id, "random_digit", random_digit)
    print(get_data_storage(message.chat.id))

    bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, process_digit_step)


def process_digit_step(message):
    user_digit = message.text

    if not user_digit.isdigit():
        msg = bot.reply_to(message, 'Вы ввели не цифры, введите пожалуйста цифры')
        bot.register_next_step_handler(msg, process_digit_step)
        return

    attempt = get_data_storage(message.chat.id)["attempt"]
    random_digit = get_data_storage(message.chat.id)["random_digit"]

    if int(user_digit) == random_digit:
        bot.send_message(message.chat.id, f'Ура! Ты угадал число! Это была цифра: {random_digit}')
        init_storage(message.chat.id)
        return
    elif attempt > 1:
        attempt -= 1
        set_data_storage(message.chat.id, "attempt", attempt)
        bot.send_message(message.chat.id, f'Неверно, осталось попыток: {attempt}')
        bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_message(message.chat.id, 'Вы проиграли!')
        init_storage(message.chat.id)
        return


@bot.message_handler(commands=['rockPaperScissors'])
def game_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Камень🤜')
    btn2 = types.KeyboardButton('Ножницы✌️')
    btn3 = types.KeyboardButton('Бумага✋')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Камень🤜, ножницы✌️, бумага✋, раз, два, три! Выберите жест:',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def game(message):
    choice = random.choice(['Камень🤜', 'Ножницы✌️', 'Бумага✋'])
    if message.text == choice:
        bot.send_message(message.chat.id, 'Боевая ничья!  Для начала новой игры пишите /rockPaperScissors')
        return
    else:
        if message.text == 'Камень🤜':
            if choice == 'Ножницы✌️':
                bot.send_message(message.chat.id,
                                 'Поздравляю с победой! У меня была {}.  Для начала новой игры пишите /rockPaperScissors'.format(
                                     choice))
            else:
                bot.send_message(message.chat.id,
                                 'Извините, но Вы проиграли 😢. У меня был(и/a) {}.  Для начала новой игры пишите /rockPaperScissors'.format(
                                     choice))

        elif message.text == 'Ножницы✌️':
            if choice == 'Бумага✋':
                bot.send_message(message.chat.id,
                                 'Поздравляю с победой! У меня была {}. Для начала новой игры пишите /rockPaperScissors'.format(
                                     choice))
            else:
                bot.send_message(message.chat.id,
                                 'Извините, но Вы проиграли 😢. У меня был(и/a) {}.  Для начала новой игры пишите /rockPaperScissors'.format(
                                     choice))
        elif message.text == 'Бумага✋':
            if choice == 'Камень🤜':
                bot.send_message(message.chat.id,
                                 'Поздравляю с победой! У меня была {}.  Для начала новой игры пишите /rockPaperScissors'.format(
                                     choice))
            else:
                bot.send_message(message.chat.id,
                                 'Извините, но Вы проиграли 😢. У меня был(и/a) {}. Для начала новой игры пишите /rockPaperScissors'.format(
                                     choice))
        return


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling()
