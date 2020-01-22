from flask import Flask
from flask import request
import requests
import json
import telebot

app = Flask(__name__)
TOKEN = '1087000896:AAH7nwyqoV3ESLy6ygxz-GmCwgQylv3ypjI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Бот парсит HH и выдает по заданым ключевым словам и региону информацию о вакасиях.\n Кол-во вакансий, средняя ЗП, и топ 10 необходимых навыков")

@app.route('/')
def index():
    return '<h1>Бот парсер v1</>'

if __name__ == '__main__':
    app.run()