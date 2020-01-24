import flask
import json
import time
import telebot
from telebot import apihelper


app = flask.Flask(__name__)
TOKEN = '1087000896:AAH7nwyqoV3ESLy6ygxz-GmCwgQylv3ypjI'
WEBHOOK_HOST = 'https://nubot.autosh.ru'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

bot = telebot.TeleBot(TOKEN)
apihelper.proxy = {'https': 'socks5://nutelebot:h8#jU2mQ@alterlife.me:1818'}

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Бот парсит HH и выдает по заданым ключевым словам и региону информацию о вакасиях.\n Кол-во вакансий, средняя ЗП, и топ 10 необходимых навыков")

# Handle all other text messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

@app.route('/')
def index():
    return '<h1>Бот парсер v1</>'

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

if __name__ == '__main__':
    app.run()