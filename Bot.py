#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
import config,Message
if __name__ == "__main__":
    if config.Master_ID==0:
        print("[WARN]你的管理员ID为0,将无法使用某些功能.")
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
    print("[INFO]机器人已启动.")
    updater.start_polling()
    updater.idle()