#import flask
import json
import time
#import telebot
from telebot import apihelper
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY={
    'proxy_url': 'socks5://alterlife.me:1818',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'nutelebot',
        'password': 'h8#jU2mQ',
    }
}
TOKEN = '1087000896:AAH7nwyqoV3ESLy6ygxz-GmCwgQylv3ypjI'
bot = telegram.Bot(token=TOKEN)

updater = Updater(token='1087000896:AAH7nwyqoV3ESLy6ygxz-GmCwgQylv3ypjI', use_context=True, request_kwargs=PROXY)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_webhook(listen='0.0.0.0',
                      port=5000,
                      url_path=TOKEN)
                      #key='private.key',
                      #cert='cert.pem',
                      #webhook_url='https://example.com:8443/TOKEN')
updater.bot.set_webhook("https://82d26449.ngrok.io/" + TOKEN)
updater.idle()
#app = flask.Flask(__name__)

#WEBHOOK_HOST = 'https://d822656f.ngrok.io/'
#WEBHOOK_URL_BASE = "%s" % (WEBHOOK_HOST)
#WEBHOOK_URL_PATH = "/%s" % (TOKEN)

#furl = WEBHOOK_URL_BASE+WEBHOOK_URL_PATH
#print(furl)
#print(WEBHOOK_URL_PATH)

# proxies = {
#     'https': 'http://81.210.32.100:8080'
#  #   'https': 'https://89.22.102.52',
# }

# apihelper.proxy = proxies
# bot = telebot.TeleBot(TOKEN)
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Привет!")
#
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     bot.reply_to(message, "Бот парсит HH и выдает по заданым ключевым словам и региону информацию о вакасиях.\n Кол-во вакансий, средняя ЗП, и топ 10 необходимых навыков")
#
# # Handle all other text messages
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     bot.reply_to(message, message.text)
#
# @app.route('/')
# def index():
#     return '<h1>Бот парсер v1</>'
#
# # Process webhook calls
# @app.route('/1087000896:AAH7nwyqoV3ESLy6ygxz-GmCwgQylv3ypjI', methods=['POST'])
# def webhook():
#     bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
#     return "!", 200
#
# updater.start_webhook(listen='127.0.0.1', port=5000, url_path='TOKEN1')
# updater.bot.set_webhook(webhook_url='https://example.com/TOKEN1',
#                         certificate=open('cert.pem', 'rb'))
#
#
# if __name__ == '__main__':
#      app.run()