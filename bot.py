import telebot
import requests  # for work with HTTP
import json
from telebot import types

bot = telebot.TeleBot('7175628286:AAEDNBOaAayGrswbOYnemasT-1WujWSFGA4')
API = 'ea9ba49e45d4950c4eab0069ac547572'

user_state = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я бот, который может говорить погоду!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Температуа воздуха 🌡')
        btn2 = types.KeyboardButton('Погодные условия 🌬')
        btn3 = types.KeyboardButton('Вся информация 📚')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.from_user.id, 'Задайте интересующий вас вопрос ?', reply_markup=markup)

    elif message.text == 'Температуа воздуха 🌡':
        bot.send_message(message.from_user.id, "Напиши мне название города🏙️ в котором хочешь узнать погоду🌤️")
        user_state[message.from_user.id] = 'awaiting_city'

    elif user_state[message.from_user.id] == 'awaiting_city':
        if user_state[message.from_user.id] == 'awaiting_city':
            city = message.text.strip().lower()
            weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
            data = json.loads(weather.text)
            if 'main' in data:
                bot.reply_to(message, f'Cейчас погода: {data["main"]["temp"]} °C')
            else:
                bot.reply_to(message, 'Извините, я не смог найти погоду для этого города. Попробуйте снова.')

            user_state[message.from_user.id] = None

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Температуа воздуха 🌡')
        btn2 = types.KeyboardButton('Погодные условия 🌬')
        btn3 = types.KeyboardButton('Вся информация 📚')
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(message.from_user.id, 'Выберите интересующий вас вопрос:', reply_markup=markup)

        user_state[message.from_user.id] = None

    else:
        bot.send_message(message.from_user.id, "Я не понял, попробуйте ещё раз.")



bot.polling(non_stop=True)

