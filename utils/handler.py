# -*- coding: UTF-8 -*-
# My variables
import gettext
import html
import json
import logging
import traceback

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from utils import controller

_, languages = gettext.gettext, dict()
# gettext.find('myapplication', languages=['zh_CN', 'en_US'], localedir='locale')
languages['Chinese'] = gettext.translation('myapplication', localedir='locale', languages=['zh_CN'])
languages['English'] = gettext

keys = ['url', 'token']
auto_delete_duration = 20  # seconds
VERSION = '0.0.2'
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Command handlers
def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a message with inline buttons attached."""
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    disclaimer = [_("version: {}").format(VERSION),
                  # f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))) + ' CST'}",
                  f"Hi {update.effective_user.mention_html()}!",
                  _("This bot is used to query servers details on ") +
                  '<a href="https://nezhahq.github.io/">Nezha Dashboard</a>.',
                  _("<i>DISCLAIMER: </i>"),
                  _("<b>Security of sensitive information is guaranteed.</b>"),
                  _("Please be aware of the risks."),
                  "===========================\n",
                  ]
    disclaimer = '\n'.join(disclaimer)
    if 'url' not in context.user_data and 'token' not in context.user_data:
        text = _("No saved data.\nPlease Set Up your Nezha Dashboard First‼️")
    elif 'url' not in context.user_data:
        text = _("🔗URL is not set.\nPlease send /url YOUR_URL ❗")
    elif 'token' not in context.user_data:
        text = _("🔑TOKEN is not set.\nPlease send /token YOUR_TOKEN ❗")
    else:
        keyboard = [
            [
                InlineKeyboardButton(_("Set URL & TOKEN 🆙"), callback_data='add'),
                InlineKeyboardButton(_("Check My Panel Params"), callback_data='info'),
            ],
            [InlineKeyboardButton(_("Query Server DATA>>"), callback_data='check')],
            [InlineKeyboardButton(_("Delete Saved 🔗URL and 🔑TOKEN ‼️"), callback_data='delete')],
            [
                InlineKeyboardButton(_("Refresh Main Menu"), callback_data='main menu'),
                InlineKeyboardButton(_("切换语言"), callback_data='switch language'),
            ],
            [InlineKeyboardButton(_("Close Menu"), callback_data='close menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.callback_query is None:
            send_message = update.message.reply_text
        else:
            send_message = update.callback_query.edit_message_text
        text = disclaimer + _("Your Nezha Dashboard is:\n") + context.user_data['url'] + '\n' + _("<b>Start NOW</b>!")
        if text != update.effective_message.text_html:
            send_message(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
        return

    # Need to set something:
    keyboard = [
        [
            InlineKeyboardButton(_("Set up 🔗URL"), callback_data='url'),
            InlineKeyboardButton(_("Set up 🔑TOKEN"), callback_data='token'),
        ],
        [
            InlineKeyboardButton(_("Set up ALL"), callback_data='add'),
            InlineKeyboardButton(_("Delete ALL"), callback_data='delete'),
        ],
        [
            InlineKeyboardButton(_("Refresh Main Menu"), callback_data='main menu'),
            InlineKeyboardButton(_("切换语言"), callback_data='switch language'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query is None:
        update.message.reply_text(
            disclaimer
            + text,
            reply_markup=reply_markup,
        )
    elif update.effective_message.text_html != disclaimer + text:
        update.callback_query.edit_message_text(
            disclaimer
            + text,
            reply_markup=reply_markup,
        )


def check_keyboard(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    isListOK, text, server_list = controller.getNezhaList(context)
    context.user_data['server_list'] = server_list

    if isListOK:
        del text
        total_server = len(server_list.list)
        tags, tag_number = server_list.tag, len(server_list.tag)
        offline_server = len(server_list.offline)
        if offline_server > 0:
            offline_status_emoji = '💀'
        else:
            offline_status_emoji = '🆒'
        double_ip = len(server_list.doubleIP)
        texts = [_("Here is the query summary for your Nezha panel:\n============================"),
                 _("Servers number:               {:>4}").format(total_server),
                 _("Tags number:                    {:>4}").format(tag_number),
                 _("Offline servers number:    {:>4}").format(str(offline_server) + offline_status_emoji),
                 _("Servers with ipv4 & ipv6: {:>4}").format(double_ip)]
        text = "\n".join(texts)

        keyboard = []
        line = []
        for tag in server_list.tag:
            line.append(InlineKeyboardButton(tag, callback_data='tag: ' + tag))
            if len(line) == 3:
                # 3 tags one line
                keyboard.append(line.copy())
                line.clear()
        if line:
            keyboard.append(line)
        keyboard.append(
            [
                InlineKeyboardButton(_("Get Summary on All Servers"), callback_data='all'),
                InlineKeyboardButton(_("List All Offline Servers"), callback_data='list offline servers'),
            ]
        )
        keyboard.append([InlineKeyboardButton(_("Back to Main Menu"), callback_data='main menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        update.callback_query.edit_message_text(text=text)


def tag_keyboard(update: Update, context: CallbackContext, tag='') -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    if 'server_list' not in context.user_data:
        update.callback_query.edit_message_text(_("Time out request. Please send /start to return to the Main Menu."))
        return

    server_list = context.user_data['server_list']
    servers_id = server_list.tag[tag]
    keyboard, line = [], []
    for server_id in servers_id:
        line.append(InlineKeyboardButton(server_id, callback_data='id: ' + str(server_id)))
        if len(line) == 6:
            # 6 server id one line
            keyboard.append(line.copy())
            line.clear()
    if line:
        keyboard.append(line)
    keyboard.append([InlineKeyboardButton(_("{} summary in detail").format(tag), callback_data='tag in detail ' + tag)])
    keyboard.append([InlineKeyboardButton(_("Back to Main Menu"), callback_data='main menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Get Servers Details in tag
    texts = [_("Here is the summary for tag {}").format(tag), '===========================',
             _("Servers number:  {}").format(len(servers_id)),
             _("Offline servers number:      {}").format(len(servers_id & server_list.offline)),
             _("Servers with ipv4 & ipv6:   {}").format(len(servers_id & server_list.doubleIP)),
             '===========================']

    for server_id in servers_id:
        server = server_list.list[server_id]
        isLive = _("❇️Online") if server_id not in server_list.offline else _("☠️Offline")
        texts.append(f'{server_id:<5d}{isLive:<10s}{server["name"]}')
    update.callback_query.edit_message_text(text='\n'.join(texts), reply_markup=reply_markup)


def get_detail_keyboard(update: Update, context: CallbackContext, server_id_str='', tag=''):
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    if update.callback_query is None:
        send_message = update.message.reply_text

        if update.message.text.startswith('/id'):  # /id command
            # number of parameter not equal to 1
            if len(context.args) != 1:
                message = send_message(_("Parameters Error!\nPlease send /id id again."))
                if not controller.isPrivateChat(update):
                    context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)
                return
            server_id_str = context.args[0]
            if not server_id_str.isdigit() or int(server_id_str) < 0:
                message = send_message(_("Input id is not a positive integer.\nPlease send /id id again."))
                if not controller.isPrivateChat(update):
                    context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)
                return
        # elif update.message.text.startswith('/all'): # /all command
        #     pass
    else:
        send_message = update.callback_query.edit_message_text

    # is user's url and token added?
    for key in keys:
        if key not in context.user_data:
            message = send_message(text=_("Please add {} for your nezha monitoring site.").format(key))
            if not controller.isPrivateChat(update):
                context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)
            return

    isListOK, text, server_list_detail = controller.getNezhaDetail(context, server_id_str, tag)
    if isListOK:
        del text
        if len(server_id_str) > 0:
            callback_data = 'refresh id ' + server_id_str
        elif len(tag) > 0:
            callback_data = 'refresh tag ' + tag
        else:
            callback_data = 'all'

        keyboard = [
            [InlineKeyboardButton(_("Refresh"), callback_data=callback_data)],
            [InlineKeyboardButton(_("Back to Main Menu"), callback_data='main menu')],
        ]
        server_list_detail.getDetails(user_language=context.user_data['language'], server_id=server_id_str, tag=tag)
        text = server_list_detail.detail
        reply_markup = InlineKeyboardMarkup(keyboard)
        if not controller.isPrivateChat(update):
            message = send_message(text=text)
        else:
            if update.callback_query and text.strip() == update.effective_message.text_html:
                return
            send_message(text=text, reply_markup=reply_markup)
            # 由于是私聊，所以不需要自动删除
            return
    else:
        message = send_message(text=html.escape(text))

    if not controller.isPrivateChat(update):
        context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)


def language_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton('简体中文', callback_data='language Chinese')],
        [InlineKeyboardButton('English', callback_data='language English')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Please Choose your Language\n请选择语言"
    update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)


def list_offline_keyboard(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    send_message = update.callback_query.edit_message_text

    if 'server_list' not in context.user_data:
        update.callback_query.edit_message_text(_("Time out request. Please send /start to return to the Main Menu."))
        return
    server_list = context.user_data['server_list']
    offline_list = server_list.offline
    texts = list()
    for server_id in offline_list:
        server = server_list.list[server_id]
        isLive = _("❇️Online") if server_id not in server_list.offline else _("☠️Offline")
        texts.append(f'{server_id:<3d}{isLive:<7s}{server["name"]}')
    if len(texts) == 0:
        send_message(text=_("Congratulations! No offline server found."))
    else:
        send_message(text='\n'.join(texts))


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # keyboard = []
    if query.data in {'add', 'url', 'token'}:
        if query.data == 'add':
            to_add = _("`YOUR_URL YOUR_TOKEN`")
        else:
            to_add = _("`YOUR_{}`").format(query.data.upper())

        query.edit_message_text(
            text=_("Please set up your Nezha dashboard by /{} {}").format(query.data, to_add),
            parse_mode='MarkdownV2',
        )
    elif query.data == 'info':
        info_command(update, context)
    elif query.data == 'delete':
        delete_command(update, context)
    elif query.data == 'confirm delete':
        delete_command(update, context)
    elif query.data == 'cancel delete':
        start_command(update, context)
    elif query.data == 'check':
        check_keyboard(update, context)
    elif query.data == 'main menu':
        start_command(update, context)
    elif controller.isTag(query.data):
        tag_keyboard(update, context, query.data.split()[-1])
    elif controller.isID(query.data):
        get_detail_keyboard(update, context, query.data.split()[-1])
    elif controller.isRefreshID(query.data):
        get_detail_keyboard(update, context, query.data.split()[-1])
    elif controller.isDetailTag(query.data):
        get_detail_keyboard(update, context, tag=query.data.split()[-1])
    elif controller.isRefreshTag(query.data):
        get_detail_keyboard(update, context, tag=query.data.split()[-1])
    elif query.data == 'all':
        get_detail_keyboard(update, context)
    elif query.data == 'switch language':
        language_keyboard(update, context)
    elif query.data.startswith('language'):
        context.user_data['language'] = query.data.split()[-1]
        start_command(update, context)
    elif query.data == 'close menu':
        update.callback_query.delete_message()
    elif query.data == 'list offline servers':
        list_offline_keyboard(update, context)


def info_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    texts = [_('Here is your saved data:')]
    icons = ['🔗', '🔑']
    for i in range(len(keys)):
        key = keys[i]
        icon = icons[i]
        if key in context.user_data:
            texts.append(icon + fr'{key.upper()}: <span class="tg-spoiler">{context.user_data[key]}</span>')
        else:
            texts.append(icon + _("{0} is not set.\nPlease send: /{1} YOUR_{0}").format(key.upper(), key))
    context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(texts))


def delete_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    if update.callback_query is None or update.callback_query.data == 'confirm delete':
        user_language = context.user_data['language']
        context.user_data.clear()
        context.user_data['language'] = user_language
        text = _("Your 🔗URL and 🔑TOKEN was <b>DELETED</b>!\nUse /start to go back to the main menu.\nUse /add to"
                 " set your Data. ")
        if update.callback_query is None:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        else:
            update.callback_query.edit_message_text(text=text)
    else:
        # Need confirmation
        keyboard = [
            [InlineKeyboardButton(_("Confirm to Delete"), callback_data='confirm delete')],
            [InlineKeyboardButton(_("Cancel"), callback_data='cancel delete')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = _("Please confirm your request:")
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)


def add_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    if len(context.args) != 2:
        update.message.reply_text(_("Parameters Error!\nPlease send: /add YOUR_URL YOUR_TOKEN"))
        return
    url, token = context.args
    text = [controller.addUrl(url, context), controller.addToken(token, context),
            _("Use /start to Start.")]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\n".join(text)
    )


def url_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    if len(context.args) < 1:
        update.message.reply_text(_("Parameters Error!\nPlease use: /url YOUR_URL"))
        return
    url = context.args[0]
    text = list()
    text.append(controller.addUrl(url, context))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\n".join(text)
    )


def token_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    if len(context.args) < 1:
        update.message.reply_text(_("Parameters Error!\nPlease use: /token YOUR_TOKEN"))
        return
    token = context.args[0]
    text = list()
    text.append(controller.addToken(token, context))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\n".join(text)
    )


def search_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    send_message = update.effective_message.reply_text
    # is user's url and token added?
    for key in keys:
        if key not in context.user_data:
            send_message(text=_("Please add {} for your nezha monitoring site.").format(key))
            return

    if len(context.args) == 0:
        message = send_message(text=_("No input words! Please send /search keywords."))
        if not controller.isPrivateChat(update):
            context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)
        return
    message = send_message(text=_("Loading..."))
    isListOK, text, server_list = controller.getNezhaList(context)
    context.user_data['server_list'] = server_list

    if isListOK:
        del text
        texts = list()
        for server_id in server_list.list:
            server = server_list.list[server_id]
            isThisServer = True
            for arg in context.args:
                if arg not in server["name"]:
                    isThisServer = False
                    break
            if isThisServer:
                isLive = _("❇️Online") if server_id not in server_list.offline else _("☠️Offline")
                texts.append(f'{server_id:<3d}{isLive:<7s}{server["name"]}')
        if len(texts) == 0:
            texts = [
                _("No server detected."), _("Please try again.")
            ]
        message = message.edit_text(text='\n'.join(texts))
    else:
        message = message.edit_text(text)

    if not controller.isPrivateChat(update):
        context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)


def help_command(update: Update, context: CallbackContext) -> None:
    user_language = context.user_data.setdefault('language', 'Chinese')
    _ = languages[user_language].gettext

    message = update.message.reply_text(
        '\n'.join([
            _("Use /start to start."),
            _("Use /add YOUR_URL YOUR_TOKEN to add your site data."),
            _("Use /delete to delete saved data."),
            _("Use /url YOUR_URL to update url."),
            _("Use /token YOUR_TOKEN to update token."),
            _("Use /info to get your url and token."),
            _("Use /id id to query by id directly."),
            _("Use /all to get statistics summary of all servers."),
            _("Use /search keywords to search in server names."),
            _("Please enjoy your time!"),
        ])
    )
    if not controller.isPrivateChat(update):
        context.job_queue.run_once(automatic_delete_message, auto_delete_duration, context=message)


def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096-character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=context.bot_data['developer_chat_id'], text=message)


def automatic_delete_message(context: CallbackContext):
    context.job.context.delete()
