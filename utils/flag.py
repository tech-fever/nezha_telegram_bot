# -*- coding: UTF-8 -*-
symbols = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷",
           "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]


def flag(country_code: str) -> str:
    res = list()
    BASE = ord("A")
    for s in country_code:
        res.append(symbols[ord(s.upper()) - BASE])
    return "".join(res)
