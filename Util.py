# -*- coding: utf-8 -*-
# @Author: hai
# @Date: 2019-02-13 17:49:00


import hashlib
from urllib.parse import urlparse


def get_top_level_domains():
    top_domain = ('abudhabi', 'ac', 'academy', 'accountant', 'ad', 'adult', 'ae', 'aero', 'af', 'africa', 'ag', 'agency', 'ai', 'al', 'alsace', 'am', 'amsterdam', 'an', 'ao', 'apartments', 'app', 'aq', 'ar', 'archi', 'arpa', 'art', 'as', 'asia', 'associates', 'at', 'au', 'audio', 'auto', 'aw', 'ax', 'az', 'ba', 'bar', 'barcelona', 'bargains', 'bb', 'bcn', 'bd', 'be', 'berlin', 'best', 'bf', 'bg', 'bh', 'bi', 'bible', 'bike', 'biz', 'bj', 'bl', 'black', 'blackfriday', 'blog', 'blue', 'bm', 'bn', 'bo', 'bot', 'bq', 'br', 'brussels', 'bs', 'bt', 'builders', 'bv', 'bw', 'by', 'bz', 'bzh', 'ca', 'cab', 'cam', 'camera', 'camp', 'cancerresearch', 'car', 'cards', 'cars', 'cat', 'cc', 'cd', 'center', 'cf', 'cg', 'ch', 'cheap', 'christmas', 'church', 'ci', 'ck', 'cl', 'click', 'clothing', 'cloud', 'club', 'cm', 'cn', 'co', 'codes', 'coffee', 'college', 'com', 'coop', 'country', 'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cymru', 'cz', 'dance', 'date', 'dating', 'de', 'desi', 'design', 'dev', 'diet', 'directory', 'dj', 'dk', 'dm', 'do', 'download', 'dz', 'ec', 'eco', 'edu', 'education', 'ee', 'eg', 'eh', 'email', 'er', 'es', 'et', 'eu', 'eus', 'events', 'exchange', 'exposed', 'faith', 'farm', 'fi', 'fj', 'fk', 'flowers', 'fm', 'fo', 'fr', 'frl', 'futbol', 'ga', 'gal', 'game', 'gb', 'gd', 'gdn', 'ge', 'gent', 'gf', 'gg', 'gh', 'gi', 'gift', 'gl', 'glass', 'global', 'gm', 'gn', 'gop', 'gov', 'gp', 'gq', 'gr', 'green', 'gs', 'gt', 'gu', 'guitars', 'guru', 'gw', 'gy', 'help', 'hiphop', 'hiv', 'hk', 'hm', 'hn', 'holdings', 'hosting', 'house', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'info', 'ink', 'int', 'international', 'io', 'iq', 'ir', 'irish', 'is', 'ist', 'istanbul', 'it', 'je', 'jm', 'jo', 'jobs', 'jp', 'juegos', 'kaufen', 'ke', 'kg', 'kh', 'ki', 'kim', 'kiwi', 'km', 'kn', 'kp', 'kr', 'krd', 'kw', 'ky', 'kz', 'la', 'land', 'lat', 'lb', 'lc', 'lgbt', 'li', 'life', 'lighting', 'link', 'live', 'lk', 'loan', 'lol', 'london', 'love', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'map', 'market', 'mc', 'md', 'me', 'med', 'meet', 'melbourne', 'men', 'menu', 'mf', 'mg', 'mh', 'miami', 'mil', 'mk', 'ml', 'mm', 'mn', 'mo', 'mobi', 'moda', 'moe', 'mom', 'movie', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'museum', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'name', 'nc', 'ne', 'net', 'new', 'nf', 'ng', 'ngo', 'ni', 'ninja', 'nl', 'no', 'np', 'nr', 'nu', 'nyc', 'nz', 'om', 'one', 'ong', 'onl', 'ooo', 'org', 'organic', 'pa', 'paris', 'pe', 'pf', 'pg', 'ph', 'pharmacy', 'photo', 'photos', 'pics', 'pink', 'pizza', 'pk', 'pl', 'plumbing', 'pm', 'pn', 'porn', 'post', 'pr', 'pro', 'properties', 'property', 'ps', 'pt', 'pub', 'pw', 'py', 'qa', 'quebec', 're', 'realtor', 'red', 'rich', 'rio', 'ro', 'rocks', 'rs', 'ru', 'rw', 'sa', 'saarland', 'sale', 'sb', 'sc', 'science', 'scot', 'sd', 'se', 'sex', 'sexy', 'sg', 'sh', 'shiksha', 'shop', 'si', 'singles', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'social', 'solar', 'sr', 'ss', 'st', 'stream', 'su', 'sucks', 'sv', 'swiss', 'sx', 'sy', 'sydney', 'sz', 'taipei', 'tattoo', 'tc', 'td', 'tel', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'today', 'tokyo', 'top', 'tp', 'tr', 'travel', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'um', 'uno', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vegas', 'ventures', 'vg', 'vi', 'video', 'vlaanderen', 'vn', 'voting', 'vu', 'wales', 'wedding', 'wf', 'wien', 'wiki', 'win', 'work', 'ws', 'wtf', 'xxx', 'xyz', 'ye', 'yt', 'za', 'zm', 'zw', 'бг', 'бел', 'ею', 'католик', 'мкд', 'мон', 'онлайн', 'рф', 'сайт', 'срб', 'укр', 'қаз', 'հայ', 'ابوظبي', 'بيتك', 'عرب', 'كاثوليك', 'كوم', 'موبايلي', 'भारत', 'भारतम्', 'भारोत', 'বাংলা', 'ভারত', 'ভাৰত', 'ਭਾਰਤ', 'ભારત', 'இந்தியா', 'இலங்கை', 'சிங்கப்பூர்', 'భారత్', 'ಭಾರತ', 'ഭാരതം', 'ලංකා', 'ไทย', 'გე', 'コム', '中国', '中國', '公司', '台湾', '台灣', '广东', '新加坡', '澳門', '澳门', '网络', '香港', '한국')
    return top_domain


def get_website_domain(url):
    if isinstance(url, str):
        hostname = urlparse(url).hostname
        if hostname is None:
            hostname = url
        domains = hostname.split('.')
        result = ''
        top_domains = get_top_level_domains()
        for i, domain in enumerate(reversed(domains)):
            if not result:
                result = domain + result
            else:
                result = domain + '.' + result
            if domain not in top_domains:
                if i == 0:
                    result = str(hostname)
                break
        return result
    return ''


def get_file_sha512(filepath):
    _sha512 = None
    with open(filepath, 'rb') as f:
        sha512 = hashlib.sha512()
        data = f.read()
        sha512.update(data)
        _sha512 = sha512.hexdigest()
    return _sha512