import logging
import telegram
import os
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from module import services, parser

PROXY = {
    'proxy_url': 'socks5://alterlife.me:1818',
    'urllib3_proxy_kwargs': {
        'username': 'nutelebot',
        'password': 'h8#jU2mQ',
    }
}

with open("config.json", "r") as file:
    config = json.load(file)

TOKEN = config['TOKEN']
WEBHOOK_URL = config['WEBHOOK_URL']
PORT = config['PORT']

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

def get_skills(update, context):
    args = " ".join(context.args)
    args_list = args.split(' ')
    #регион
    arg1 = args_list[0]
    t_arg2 = args_list[1::]
    #ключевая фраза
    arg2 = ' '.join(t_arg2)
    if services.get_req(arg1, arg2):
        id_area, text_req = services.get_req(arg1, arg2)
        filename = (parser.get_result_for_bot(id_area, text_req, arg1))
        result = services.load_result_from_file(filename)
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ошибочно введен город, Чтобы повторить запрос, снова полностью отправьте команду, проверив правильность написания города.')
get_skills_handler = CommandHandler('get_skills', get_skills, pass_args=True)
dispatcher.add_handler(get_skills_handler)

def chating(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Просто поболтать к сожалению со мной пока нельзя.')
chating_hundler = MessageHandler(Filters.text, chating)
dispatcher.add_handler(chating_hundler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю такой команды")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#если на хероку разворачивать то порт из переменной окружения берем
if 'HEROKU_ENV' in os.environ:
    PORT = int(os.environ.get('PORT'))
print(PORT)
print(WEBHOOK_URL + TOKEN)
updater.start_webhook(listen='0.0.0.0',
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook(WEBHOOK_URL + TOKEN)
