# -*- coding: UTF-8 -*-
import gettext
import re
import requests as requests
import time
from utils import nezha
from telegram import Update

_, languages = gettext.gettext, dict()
# gettext.find('myapplication', languages=['zh_CN', 'en_US'], localedir='locale')
languages['Chinese'] = gettext.translation('myapplication', localedir='locale', languages=['zh_CN'])
languages['English'] = gettext

LIST_ROUTER = "/api/v1/server/list?"
DETAILS_ROUTER = "/api/v1/server/details?"

Unclassified = "Untagged"


# valid url must begin with https:// or http://
def isUrlOK(url: str) -> bool:
    """
    :param url:  str
    :return:     bool
    """
    if re.match(r'^https?:/{2}\w.+$', url):
        return True
    else:
        return False


def isTag(data: str) -> bool:
    if re.match(r'^tag: .*', data):
        return True
    else:
        return False


def isDetailTag(data: str) -> bool:
    if re.match(r'^tag in detail .*', data):
        return True
    else:
        return False


def isRefreshTag(data):
    if re.match(r'^refresh tag .*', data):
        return True
    else:
        return False


def isID(data: str) -> bool:
    if re.match(r'^id: .*', data):
        return True
    else:
        return False


def isRefreshID(data: str) -> bool:
    if re.match(r'^refresh id .*', data):
        return True
    else:
        return False


def addUrl(url: str, context) -> str:
    """
    :param url:      str
    :param context:  CallbackContext
    :return:         text to reply
    """
    user_language = context.user_data['language']
    _ = languages[user_language].gettext

    if not isUrlOK(url):
        text = _("🔗URL must begin with <b>https://</b> or <b>http://</b>❗")
        return text
    context.user_data['url'] = url
    text = _("🔗<b>Successfully</b> saved:\n") + url
    return text


def addToken(token: str, context) -> str:
    """
    :param token:    str
    :param context:  CallbackContext
    :return:         text to reply
    """
    user_language = context.user_data['language']
    _ = languages[user_language].gettext

    context.user_data["token"] = token
    text = _("🔑<b>Successfully</b> saved:\n") + f'<span class="tg-spoiler">{token}</span>'
    return text


def getNezhaList(context, tag=''):
    user_language = context.user_data['language']
    _ = languages[user_language].gettext
    url, token = context.user_data["url"], context.user_data["token"]

    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    url = url.strip('/')
    url = url + LIST_ROUTER + 'tag=' + tag
    try:
        r = requests.get(url, headers=headers)
        timestamp = int(time.time())
    except BaseException as e:
        msg = '%s' % e
        return [False, msg, None]

    if not r.ok:
        msg = _("{} Connection Failed.\nStatus Code: {}.\nError: {}").format(r.url, r.status_code, r.reason)
        return [False, msg, None]

    if r.json()['code'] != 0:
        return [False, r.json()['message'], None]

    try:
        result = r.json()['result']
        if len(result) > 0:
            server_list = nezha.ServersList(result, timestamp, context.user_data['language'])
            del result
            return [True, "", server_list]
        else:
            # no server
            return [False, _("No server detected."), None]
    except BaseException as e:
        msg = '%s' % e
        return [False, msg, None]


def getNezhaDetail(context, server_id='', tag=''):
    user_language = context.user_data['language']
    _ = languages[user_language].gettext

    if tag == Unclassified:
        tag = ''
    url, token = context.user_data["url"], context.user_data["token"]

    headers = {
        'Authorization': token,
    }
    url = url.strip('/')
    url = url + DETAILS_ROUTER + 'id=' + server_id + '&tag=' + tag

    try:
        r = requests.get(url, headers=headers)
        timestamp = int(time.time())
    except BaseException as e:
        msg = '%s' % e
        return [False, msg, None]

    if not r.ok:
        msg = _("{} Connection Failed.\nStatus Code: {}.\nError: {}").format(r.url, r.status_code, r.reason)
        return [False, msg, None]

    if r.json()['code'] != 0:
        return [False, r.json()['message'], None]

    try:
        result = r.json()['result']
        if len(result) > 0:
            server_list = nezha.ServerDetail(result=result, timestamp=timestamp)
            del result
            return [True, '', server_list]
        else:
            # no server
            return [False, _("No server detected."), None]
    except BaseException as e:
        msg = '%s' % e
        return [False, msg, None]


def isPrivateChat(update: Update) -> bool:
    return update.effective_chat.type == 'private'
