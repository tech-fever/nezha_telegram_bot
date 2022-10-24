#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

import pytz
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, PicklePersistence, CallbackQueryHandler, Filters, Defaults

from utils import handler
from utils.get_config import GetConfig


def main():
    # TimeZone
    # Bot config
    bot_token = config['TELEBOT']['bot_token']
    base_url = None if len(config['TELEBOT']['base_url']) == 0 else config['TELEBOT']['base_url']
    base_file_url = None if len(config['TELEBOT']['base_file_url']) == 0 else config['TELEBOT']['base_file_url']

    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Asia/Shanghai'))

    """Start the bot."""
    # mkdir if path not exists
    if not os.path.exists('data'):
        os.mkdir('data')
    my_persistence = PicklePersistence(filename='./data/my_file')
    updater = Updater(token=bot_token, persistence=my_persistence, use_context=True, base_url=base_url,
                      base_file_url=base_file_url, defaults=defaults)
    # PS：use_context is by default False in v12, and True in v13
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.bot_data['developer_chat_id'] = int(config['DEVELOPER']['developer_chat_id'])
    dispatcher.bot_data.pop('group_enabled_command', None)
    dispatcher.bot_data.pop('group_banned_command', None)
    # on different commands - answer in Telegram

    dispatcher.add_handler(
        CommandHandler('start', handler.start_command, run_async=True, filters=Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('help', handler.help_command, run_async=True))
    dispatcher.add_handler(CommandHandler('add', handler.add_command, filters=Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('url', handler.url_command, filters=Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('token', handler.token_command, filters=Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('info', handler.info_command, filters=Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('delete', handler.delete_command, filters=Filters.chat_type.private))
    dispatcher.add_handler(CommandHandler('id', handler.get_detail_keyboard, run_async=True))
    dispatcher.add_handler(CommandHandler('all', handler.get_detail_keyboard, run_async=True))
    dispatcher.add_handler(CommandHandler('search', handler.search_command, run_async=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(handler.button, run_async=True))
    dispatcher.add_error_handler(handler.error_handler, run_async=True)

    # start the bot using polling
    updater.start_polling()
    # runs the bot until a termination signal is send
    updater.idle()


if __name__ == '__main__':
    config = GetConfig()
    main()
