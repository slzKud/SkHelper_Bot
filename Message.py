#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
import config,os,Tools

def hello(bot, update):
    print(update.message)
    if update.message.from_user.username==config.Master_ID:
        update.message.reply_text(
            'Hello Master! {}'.format(update.message.from_user.first_name))
    else:
        update.message.reply_text(
            'Hello! {}'.format(update.message.from_user.first_name))

def ping(bot,update):
    print(update.message)
    bot.send_message(reply_to_message_id=update.message.message_id, chat_id=update.message.chat.id, text="pong!\nUser id:"+str(update.message.from_user.id))

def exec_message(bot,update):
    print(update.message)
    if update.message.from_user.username==config.Master_ID:
        m=update.message.text
        if " " in m:
            command_m=m.split(" ",1)[1]
            pipe_m=os.popen(command_m)
            pipe_text=pipe_m.read()
            bot.send_message(reply_to_message_id=update.message.message_id, chat_id=update.message.chat.id, text=pipe_text)
        else:
            bot.send_message(reply_to_message_id=update.message.message_id, chat_id=update.message.chat.id, text="不知道要执行啥呢,请确认")

    else:
        bot.sendMessage(reply_to_message_id=update.message.message_id,chat_id=update.message.chat_id,text=config.PermissionError_Text)

def conohacharge(bot,update):
    if update.message.from_user.username==config.Master_ID:
        a=Tools.ConohaCharge()
        bot.sendMessage(reply_to_message_id=update.message.message_id,chat_id=update.message.chat_id,text=a)
    else:
        bot.sendMessage(reply_to_message_id=update.message.message_id,chat_id=update.message.chat_id,text=config.PermissionError_Text)

def cloudconecharge(bot,update):
    if update.message.from_user.username==config.Master_ID:
        a=Tools.CloudConeCharge()
        bot.sendMessage(reply_to_message_id=update.message.message_id,chat_id=update.message.chat_id,text=a)
    else:
        bot.sendMessage(reply_to_message_id=update.message.message_id,chat_id=update.message.chat_id,text=config.PermissionError_Text)
