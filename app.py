import json
import time
import logging
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
logging.basicConfig(filename="bot.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.bot.set_webhook("https://23bd3afc.ngrok.io/" + TOKEN)
updater.start_webhook(listen='0.0.0.0',
                      port=5000,
                      url_path=TOKEN)
                      #key='private.key',
                      #cert='cert.pem',
                      #webhook_url='https://example.com:8443/TOKEN')

#updater.idle()
