import json
import time
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import bot_hhparser

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

REGION, PHRASE = range(2)

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('bot_debug.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root_logger.addHandler(handler)

def start(update, context):
    textstart = '''
        Привет, покажу топ навыков и среднюю ЗП для вакансий найденных на hh.ru.\nПоиск осуществляется по заданой ключевой фразе.\nДля получения подробной информации вызывай /help
        '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=textstart)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(update, context):
    texthelp = '''
        Доступыне команды
        /start - Приветствие, краткая информация
        /help - Справка, как использовать бота. Сейчас ты тут :)
        /get_skills - Необходимо отправить команду с указанием критериев поиска, через пробелы написать город и ключевую фразу. Будет произведен поиск вакансий по заданной ключевой фразе в выбранном регионе. Резуьльтат это топ 20 навыков (по суммарному кол-ву упоминаний в вакансиях) а так же средняя ЗП.\n Пример команды: /get_skills москва системный администратор\nЗаметка: город можно писать с использованием любого регистра.
        '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=texthelp)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# def get_skills(update, context):
#     #регион
#     arg1 = context.args[0]
#     #ключевая фраза
#     arg2 = context.args[1]
#     result = arg1 + arg2
#     result_type = str(type(result))
#     context.bot.send_message(chat_id=update.effective_chat.id, text=result)
# get_skills_handler = CommandHandler('get_skills', get_skills, pass_args=True)
# dispatcher.add_handler(get_skills_handler)

def get_skills(update, context):
    update.message.reply_text(
        'Введи город для которого искать вакансии'
        'Отправь /cancel чтобы остановить.\n\n')
    return REGION

def region(update, context):
    user = update.message.from_user
    user_name = user.first_name
    arg1 = update.message.text
    update.message.reply_text(
        'Теперь введи ключевую фразу для поиска вакансий\n'
        'Отправь /cancel чтобы остановить.\n\n')
    return PHRASE

def phrase(update, context):
    user = update.message.from_user
    user_name = user.first_name
    arg2 = update.message.text
    update.message.reply_text(
        'Ищем...')
    #TODO: тут обращаемся к парсеру
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text('Хорошо, до встречи',)
    return ConversationHandler.END

get_skills_handler = ConversationHandler(
        entry_points=[CommandHandler('get_skills', get_skills)],

        states={
            REGION: [MessageHandler(Filters.text, region)],
            PHRASE: [MessageHandler(Filters.text, phrase)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
)
dispatcher.add_handler(get_skills_handler)

def chating(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Просто поболтать к сожалению со мной пока нельзя.')
chating_hundler = MessageHandler(Filters.text, chating)
dispatcher.add_handler(chating_hundler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю такой команды")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.bot.set_webhook("https://81e9ae3c.ngrok.io/" + TOKEN)
updater.start_webhook(listen='0.0.0.0',
                      port=5000,
                      url_path=TOKEN)

