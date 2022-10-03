# -*- coding: UTF-8 -*-
import gettext
import time
from collections import defaultdict
from datetime import datetime

import humanize as humanize
import pytz

from utils import flag

languages = dict()
# gettext.find('myapplication', languages=['zh_CN', 'en_US'], localedir='locale')
languages['Chinese'] = gettext.translation('myapplication', localedir='locale', languages=['zh_CN'])
languages['English'] = gettext

Unclassified = "Untagged"


class ServersList:
    def __init__(self, result, timestamp, user_language):
        _ = languages[user_language].gettext

        self.list = dict()  # {id: server_info}
        self.tag = defaultdict(set)  # {tag: {servers_id}}
        self.offline = set()  # {offline_server_id}
        self.doubleIP = set()  # server with ipv4 and ipv6
        self.timestamp = timestamp
        for server in result:
            server_id = server['id']
            tag = server['tag'] if server['tag'] else Unclassified
            last_active = server['last_active']
            ipv4, ipv6 = server['ipv4'], server['ipv6']

            del server['id']
            self.list[server_id] = server
            self.tag[tag].add(server_id)
            if not isLive(last_active, self.timestamp):
                self.offline.add(server_id)

            if len(ipv4) * len(ipv6) != 0:
                self.doubleIP.add(server_id)


class ServerDetail:
    def __init__(self, result, timestamp):
        self.detail = list()  # output text split line by line
        if len(result) == 1:
            self.type = 'id'
        else:
            self.type = 'tag'
        self.list = dict()  # {id(int): server}
        self.timestamp = timestamp
        for server in result:
            server_id = server['id']
            del server['id']
            self.list[server_id] = server

    def getDetails(self, user_language, server_id, tag):
        if self.type == 'id':
            self.queryByID(user_language, server_id)
        else:
            self.queryByTag(user_language, tag)

    def queryByID(self, user_language, server_id=''):
        _ = languages[user_language].gettext

        self.detail.clear()
        if not server_id.isdigit():
            server_id = list(self.list.keys())[0]
        if int(server_id) in self.list:
            server = self.list[int(server_id)]
        else:
            server = self.list[int(list(self.list.keys())[0])]
        host = server['host']
        status = server['status']

        emoji_flag = flag.flag(host['CountryCode'])
        live = _("❇️Online") if isLive(server['last_active'], self.timestamp) else _("☠️Offline")
        CPUinfo = host['CPU'][0] if host['CPU'] else _("No CPU info")
        IPv4 = server['ipv4']
        if len(IPv4) > 0:
            IPv4_list = IPv4.split('.')
            IPv4_list[-1] = IPv4_list[-2] = '**'
            del IPv4
            IPv4 = '.'.join(IPv4_list)
        IPv6 = '✅' if len(server['ipv6']) > 0 else '❌'
        mem_used = status['MemUsed'] / host['MemTotal'] if host['MemTotal'] != 0 else 0
        swap_usage = status['SwapUsed'] / host['SwapTotal'] if host['SwapTotal'] != 0 else 0
        disk_used = status['DiskUsed'] / host['DiskTotal'] if host['DiskTotal'] != 0 else 0

        MemUsed = humanize.naturalsize(status['MemUsed'], gnu=True)
        MemTotal = humanize.naturalsize(host['MemTotal'], gnu=True)
        SwapUsed = humanize.naturalsize(status['SwapUsed'], gnu=True)
        SwapTotal = humanize.naturalsize(host['SwapTotal'], gnu=True)
        DiskUsed = humanize.naturalsize(status['DiskUsed'], gnu=True)
        DiskTotal = humanize.naturalsize(host['DiskTotal'], gnu=True)
        NetInTransfer = humanize.naturalsize(status['NetInTransfer'], gnu=True)
        NetOutTransfer = humanize.naturalsize(status['NetOutTransfer'], gnu=True)
        NetInSpeed = humanize.naturalsize(status['NetInSpeed'], gnu=True)
        NetOutSpeed = humanize.naturalsize(status['NetOutSpeed'], gnu=True)
        details = [r"{} {} {}".format(emoji_flag, server['name'], live),
                   '==========================',
                   'tag: {:10s} id: {}'.format(server['tag'], server_id),
                   'ipv4: {}'.format(IPv4),
                   'ipv6: {}'.format(IPv6),
                   _("Platform:  {}").format(host['Platform']),
                   _("CPU info:        {}").format(CPUinfo),
                   _("Uptime:    {}").format(calUptime(host['BootTime'], user_language)),
                   _("Load:       {:.2f} {:.2f} {:.2f}").format(status['Load1'], status['Load5'], status['Load15']),
                   _("CPU:        {:.2%} [{}]").format(status['CPU'] / 100, host['Arch']),
                   _("MemUsed:   {:<3.1%} [{}/{}]").format(mem_used, MemUsed, MemTotal),
                   _("SwapUsed:  {:<3.1%} [{}/{}]").format(swap_usage, SwapUsed, SwapTotal),
                   _("DiskUsed:    {:<3.1%} [{}/{}]").format(disk_used, DiskUsed, DiskTotal),
                   _("Transfer:      ↓{:<10s} ↑{}").format(NetInTransfer, NetOutTransfer),
                   _("TransRate:   ↓{:<10s} ↑{}/s").format(NetInSpeed + '/s', NetOutSpeed),
                   _("\nUpdated on:{:>25}").format(getTime(self.timestamp)),
                   ]
        self.detail = '\n'.join(details)

    def queryByTag(self, user_language, tag=''):
        _ = languages[user_language].gettext
        isAllServers = (tag == '')
        if tag == Unclassified:
            tag = ''

        self.detail.clear()
        server_number = 0
        online_server_number = 0
        CPU_total = mem_total = mem_used = swap_total = swap_used = disk_total = disk_used = 0
        NetInTransfer = NetInSpeed = NetOutTransfer = NetOutSpeed = 0
        for server_id in self.list:
            server = self.list[server_id]
            if not isAllServers and server['tag'] != tag:
                continue
            server_number += 1
            host = server['host']
            status = server['status']
            if isLive(server['last_active'], self.timestamp):
                online_server_number += 1
            CPU_total += int(host['CPU'][0].split()[-3]) if host['CPU'] and len(host['CPU'][0].split()) >= 3 else 0
            mem_total += host['MemTotal']
            mem_used += status['MemUsed']
            swap_total += host['SwapTotal']
            swap_used += status['SwapUsed']
            disk_total += host['DiskTotal']
            disk_used += status['DiskUsed']

            NetInTransfer += status['NetInTransfer']
            NetOutTransfer += status['NetOutTransfer']
            NetInSpeed += status['NetInSpeed']
            NetOutSpeed += status['NetOutSpeed']
        mem_usage = mem_used / mem_total if mem_total != 0 else 0
        swap_usage = swap_used / swap_total if swap_total != 0 else 0
        disk_usage = disk_used / disk_total if disk_total != 0 else 0
        if NetOutTransfer * NetInTransfer == 0:
            trans_parity = 0
        elif NetOutTransfer >= NetInTransfer:
            trans_parity = NetInTransfer / NetOutTransfer
        else:
            trans_parity = NetOutTransfer / NetInTransfer

        mem_used = humanize.naturalsize(mem_used, gnu=True)
        mem_total = humanize.naturalsize(mem_total, gnu=True)
        swap_used = humanize.naturalsize(swap_used, gnu=True)
        swap_total = humanize.naturalsize(swap_total, gnu=True)
        disk_used = humanize.naturalsize(disk_used, gnu=True)
        disk_total = humanize.naturalsize(disk_total, gnu=True)
        NetInSpeed = humanize.naturalsize(NetInSpeed, gnu=True)
        NetOutSpeed = humanize.naturalsize(NetOutSpeed, gnu=True)
        NetInTransfer = humanize.naturalsize(NetInTransfer, gnu=True)
        NetOutTransfer = humanize.naturalsize(NetOutTransfer, gnu=True)
        details = [
            _("Total Summary for {}").format(tag),
            '===========================',
            _("Server Number:           {}").format(server_number),
            _("Online Server Number: {}").format(online_server_number),
            _("CPU Cores:       {}").format(CPU_total),
            _("Memory Usage:{:<3.1%} [{}/{}]").format(mem_usage, mem_used, mem_total),
            _("Swap Usage:     {:<3.1%} [{}/{}]").format(swap_usage, swap_used, swap_total),
            _("Disk Usage:       {:<3.1%} [{}/{}]").format(disk_usage, disk_used, disk_total),
            _("NetInSpeed:       ↓{}/s").format(NetInSpeed),
            _("NetOutSpeed:    ↑{}/s").format(NetOutSpeed),
            _("NetInTransfer:     ↓{}").format(NetInTransfer),
            _("NetOutTransfer: ↑{}").format(NetOutTransfer),
            _("Traffic Parity:      {:<3.1%}").format(trans_parity),
            _("\nUpdated on:{:>25}").format(getTime(self.timestamp)),
        ]
        self.detail = '\n'.join(details)


def isLive(last_active, timestamp):
    threshold = 60 * 30  # if time_interval is less than 30 min, then active
    time_interval = timestamp - last_active
    return time_interval < threshold


def calUptime(boot_time: int, user_language: str) -> str:
    _ = languages[user_language].gettext

    if boot_time == 0:
        return 'Offline ❌'
    timestamp = int(time.time())
    duration = timestamp - boot_time

    # Calculate uptime
    DAY = 86400  # 3600 * 24
    HOUR = 3600
    MINUTE = 60
    if duration > DAY:
        return _("{} Days {} Hours").format(duration // DAY, (duration % DAY) // HOUR)
    else:
        return _("{} Hours {} Minutes").format(duration // HOUR, (duration % HOUR) // MINUTE)


# def calSize(byte_num: int) -> str:
#     KB, MB, GB, TB, PB = 1024, 1048576, 1073741824, 1099511627776, 1125899906842624
#     if byte_num > PB:
#         return f"{byte_num / PB:.2f} PB"
#     elif byte_num > TB:
#         return f"{byte_num / TB:.2f} TB"
#     elif byte_num > GB:
#         return f"{byte_num / GB:.2f} GB"
#     elif byte_num > MB:
#         return f"{int(byte_num / MB)} MB"
#     else:
#         return f"{int(byte_num / KB)} KB"
#
#
# def calNetSpeed(byte_num: int) -> str:
#     KB, MB, GB, TB, PB = 1024, 1048576, 1073741824, 1099511627776, 1125899906842624
#     if byte_num > PB:
#         return f"{byte_num / PB:.2f} PB"
#     elif byte_num > TB:
#         return f"{byte_num / TB:.2f} TB"
#     elif byte_num > GB:
#         return f"{byte_num / GB:.2f} GB"
#     elif byte_num > MB:
#         return f"{byte_num / MB:.2f} MB"
#     else:
#         return f"{byte_num / KB:.2f} KB"


def getTime(timestamp: int) -> str:
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.fromtimestamp(timestamp, tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")
