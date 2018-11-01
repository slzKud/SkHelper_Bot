#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
import config,Message
if __name__ == "__main__":
    TOKEN=config.Bot_Token
    if config.Proxy_URL!="":
        REQUEST_KWARGS={
            'proxy_url': config.Proxy_URL,
        }
        updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    else:
        updater = Updater(TOKEN)
    #机器人指令集
    updater.dispatcher.add_handler(CommandHandler('start', Message.hello))
    updater.dispatcher.add_handler(CommandHandler('ping', Message.ping))
    updater.dispatcher.add_handler(CommandHandler('exec', Message.exec_message))
    updater.dispatcher.add_handler(CommandHandler('conoha', Message.conohacharge))
    updater.dispatcher.add_handler(CommandHandler('cloudcone', Message.cloudconecharge))
    updater.dispatcher.add_handler(CommandHandler('eval', Message.eval_message))
    updater.dispatcher.add_handler(CommandHandler('ip', Message.ip_message))

    updater.start_polling()
    updater.idle()