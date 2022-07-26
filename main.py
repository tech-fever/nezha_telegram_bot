#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, PicklePersistence, CallbackQueryHandler, TypeHandler, MessageHandler, \
    Filters

from utils import handler
from utils.get_config import GetConfig


def main():
    # TimeZone
    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()
    # Bot config
    bot_token = config['TELEBOT']['bot_token']
    base_url = None if len(config['TELEBOT']['base_url']) == 0 else config['TELEBOT']['base_url']
    base_file_url = None if len(config['TELEBOT']['base_file_url']) == 0 else config['TELEBOT']['base_file_url']

    """Start the bot."""
    my_persistence = PicklePersistence(filename='./data/my_file')
    updater = Updater(token=bot_token, persistence=my_persistence, use_context=True, base_url=base_url,
                      base_file_url=base_file_url)
    # PS：use_context is by default False in v12, and True in v13
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.bot_data['developer_chat_id'] = int(config['DEVELOPER']['developer_chat_id'])
    dispatcher.bot_data['group_enabled_command'] = {'/help', '/id', '/all', '/search'}
    dispatcher.bot_data['group_banned_command'] = {'/start', '/add', '/url', '/token', '/info', '/delete'}
    # handlers that are forbidden in groups
    group_banned_handlers = MessageHandler(filters=Filters.chat_type.groups & Filters.command,
                                           callback=handler.pre_check_group_banned_cmd)
    dispatcher.add_handler(group_banned_handlers, -1)
    # on different commands - answer in Telegram

    dispatcher.add_handler(CommandHandler('start', handler.start_command))
    dispatcher.add_handler(CommandHandler('help', handler.help_command, run_async=True))
    dispatcher.add_handler(CommandHandler('add', handler.add_command))
    dispatcher.add_handler(CommandHandler('url', handler.url_command))
    dispatcher.add_handler(CommandHandler('token', handler.token_command))
    dispatcher.add_handler(CommandHandler('info', handler.info_command))
    dispatcher.add_handler(CommandHandler('delete', handler.delete_command))
    dispatcher.add_handler(CommandHandler('id', handler.get_detail_keyboard, run_async=True))
    dispatcher.add_handler(CommandHandler('all', handler.get_detail_keyboard, run_async=True))
    dispatcher.add_handler(CommandHandler('search', handler.search_command, run_async=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(handler.button, run_async=True))
    dispatcher.add_error_handler(handler.error_handler, run_async=True)

    # job job_queue

    # start the bot using polling
    updater.start_polling()
    # runs the bot until a termination signal is send
    updater.idle()


if __name__ == '__main__':
    config = GetConfig()
    main()
