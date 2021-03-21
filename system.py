from datetime import datetime
from bs4 import BeautifulSoup as bs
from colorama import Fore, init
import requests
import json
import random
import re
import base64
import calendar
import time
import config
import connect_db
cursor, conn = connect_db.baglanti()
init()


def debug(text):
    _file = open('logs.txt', 'a', encoding='utf-8')
    _file.write(f"[{get_current_time()}] {str(text)}\n")
    print(
        f"{Fore.LIGHTRED_EX}[{Fore.CYAN}{get_current_time()}{Fore.LIGHTRED_EX}] {Fore.LIGHTGREEN_EX}{str(text)}{Fore.RESET}")


def is_user(user):
    try:
        user = int(user)
        return 'yes'
    except:
        return 'no'


def get_timestamp(select, timestamp=None):
    if select == 'timestamp':
        ts = calendar.timegm(time.gmtime())
        return ts
    elif select == 'date':
        date_time = datetime.fromtimestamp(int(timestamp))
        d = date_time.strftime("%Y/%m/%d, %H:%M:%S")
        return d


def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_visitor():
    now = datetime.now()
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    data = f'{ip},{now.strftime("%Y-%d-%m %H:%M:%S")}'
    data_bytes = data.encode('UTF-8')
    base64_bytes = base64.b64encode(data_bytes)
    base64_data = base64_bytes.decode('UTF-8')
    return base64_data


def update(table, _set, where=""):

    wh = ""
    if where != "":
        wh = (f"WHERE {where}")

    sonuc = cursor.execute(f'UPDATE {table} SET {_set} {wh}')
    conn.commit()


def get_user(discordid):
    try:
        cursor.execute(f"SELECT * FROM users WHERE d_id = '{discordid}' ")
        kodoku = cursor.fetchone()
        return kodoku
    except:
        return 'hata'


def get_data(sql):
    try:
        cursor.execute(f"SELECT * FROM {sql}")
        kodoku = cursor.fetchall()
        return kodoku
    except:
        return 'hata'


def get_data_one(sql):
    try:
        cursor.execute(f"SELECT * FROM {sql}")
        kodoku = cursor.fetchone()
        return kodoku
    except:
        return 'hata'


def get_transactions(userid):
    try:
        cursor.execute(
            f"SELECT * FROM transactions WHERE user = '{userid}' ORDER BY date DESC")
        kodoku = cursor.fetchall()
        return kodoku
    except:
        return 'hata'


def check_transactions(transactions):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    count = 0
    for transaction in transactions:
        transaction_timestamp = transaction['date']
        date_time = datetime.fromtimestamp(int(transaction_timestamp))
        used_timestamp = date_time.strftime("%Y-%m-%d")

        if today == used_timestamp:
            count += 1
    return count


def get_short_links():
    try:
        cursor.execute(f"SELECT * FROM links")
        kodoku = cursor.fetchall()
        return kodoku
    except:
        return 'hata'


def arg_to_link(arg_data):
    try:
        cursor.execute(f"SELECT * FROM links WHERE arg = '{arg_data}'")
        kodoku = cursor.fetchone()
        if kodoku != None:
            return kodoku
        else:
            return 'hata'
    except:
        return 'hata'


def get_bildirim_url(html):
    #url_data = re.findall("url = '\D+", str(html))
    #url = url_data[0].split("'")[1]
    url_data = re.findall(
        "url = '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", str(html))
    url = url_data[0][0]
    return url


def setup_request():
    proxy_origin = select_random_proxy()
    proxies = {
        'http': f'http://{proxy_origin}',
        'https': f'http://{proxy_origin}'
    }
    return proxies


def siteye_get_at(linki_gir, domain, short_name):
    burp0_url = f"https://{domain}/{linki_gir}"
    burp0_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "pragma": "no-cache",
        "Accept": "*/*"
    }
    siteye_get = requests.get(burp0_url, headers=burp0_headers, timeout=5)
    if short_name in siteye_get.url:

        veri = bs(str(siteye_get.text), 'lxml')
        mesaj = veri.find_all('script', type='text/javascript')
        mesaj = str(mesaj[6])

        mesaj = mesaj.replace(
            """app['current'] = app['base_url'] + '/' + app['alias'];\nlet ref_id = 97783;\nlet category_id = 3;\n</script>""", "")
        mesaj = mesaj.replace('<script type="text/javascript">\n', '')
        mesaj = mesaj.replace('let app = [];', '')
        mesaj = mesaj.replace(';', '')

        selam = ""

        for i in mesaj:
            if i != "\n":
                selam += i
            if i == "\n":
                selam += "\n"
        selam = selam.replace(' ', '')

        for line in selam.splitlines():
            if "app['csrf']=" in line:
                csrf = line[14:].replace("'", "")
            if "app['token']=" in line:
                token = line[15:].replace("'", "")

        return token, csrf
    else:
        return 'hata', 'hata'


def siteye_post_at(linki_gir, token, csrf, domain):
    burp0_url = f"https://{domain}/links/go2"
    visitor = get_visitor()
    burp0_cookies = {
        "visitor": f"{visitor}"
    }
    burp0_headers = {
        "x-requested-with": "XMLHttpRequest",
        "origin": f"https://{domain}",
        "Referer": f"https://{domain}/{linki_gir}"
    }
    burp0_data = {"alias": f"{linki_gir}",
                  "csrf": f"{csrf}", "token": f"{token}"}
    r = requests.post(burp0_url, headers=burp0_headers,
                      data=burp0_data, cookies=burp0_cookies)

    # print(r.text)
    url_bul = json.loads(r.text)
    print(url_bul)
    url_git = requests.get(str(url_bul['url']))
    if 'https://bildirim.eu' in str(url_bul['url']):
        finish_url = get_bildirim_url(str(url_git.text))
    else:
        finish_url = url_bul['url']
    print(f"Gitmek İstediğiniz Url: {finish_url}")

    print(f"\n\nDurum : {str(url_bul['message'])}")

    url_bul = dict(url_bul)

    if url_bul['status'] != 'success':
        return 'hata'
    if url_bul['message'] == 'Go With earning :)':
        url_bul['message_bot'] = 'Link sahibi para kazandı!'
    else:
        url_bul['message_bot'] = 'Link sahibi para kazanamadı :('
    url_bul['finish_url'] = finish_url
    return url_bul


def tr_link_spam(data_spam):

    code = data_spam['code']
    domain = data_spam['domain']
    short_name = data_spam['short_name']
    sınır = data_spam['max']
    _count = 0
    _kazanilan_para = 0
    while _count < int(sınır):
        token, csrf = siteye_get_at(
            code, domain, short_name)
        if token != 'hata':
            data = siteye_post_at(
                code, token, csrf, domain)
            if data != 'hata':
                if data["message"] == 'Go With earning :)':
                    _count += 1
                    _kazanilan_para += 0.022  # TR için
                else:
                    pass
    data_output = {
        'money': _kazanilan_para
    }
    return data_output


def ouo_get(code):
    url = f"https://ouo.io:443/{code}"
    headers = {
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    r = requests.get(url, headers=headers)

    verim = bs(r.text, 'lxml')
    token = verim.find("input", {"name": "_token"})['value']
    ouoio_session = r.cookies.get_dict()['ouoio_session']

    data = {
        "token": token,
        "ouoio_session": ouoio_session,
        "code": code
    }
    return data


def ouo_get2(data):
    try:
        url = f"https://ouo.io/xreallcygo/{data['code']}"
        cookies = {
            " ouoio_session": f"{data['ouoio_session']}"
        }
        headers = {
            "Connection": "close",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://ouo.io",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": f"https://ouo.io/go/{data['code']}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        data = {"_token": f"{data['token']}"}
        r = requests.post(url, headers=headers, cookies=cookies,
                          data=data, allow_redirects=False)
        soup = bs(r.text, 'lxml')

        metas = soup.find_all('a')
        finish_url = str(metas[0].attrs['href'])

        data = {
            'finish_url': finish_url,
            'message_bot': 'Mission completed',
            'status': 'success'
        }
        return data
    except:
        return 'hata'


def met_get(code):
    try:
        url = f"https://met.bz/{code}"
        headers = {
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        web_data = requests.get(url, headers=headers)
        if web_data.status_code == 200:

            visitor_data = web_data.cookies.get_dict()['visitor']
            csrf_token = web_data.cookies.get_dict()['csrfToken']

            verim = bs(web_data.text, 'lxml')
            token_fields = verim.find(
                "input", {"name": "_Token[fields]"})['value']
            token_unlocked = verim.find(
                "input", {"name": "_Token[unlocked]"})['value']

            ci = verim.find("input", {"name": "ci"})['value']
            cui = verim.find("input", {"name": "cui"})['value']

            cii = verim.find("input", {"name": "cii"})['value']
            ref = verim.find("input", {"name": "ref"})['value']

            data = {
                'code': code,
                'visitor_data': visitor_data,
                'csrf_token': csrf_token,
                'token_fields': token_fields,
                'token_unlocked': token_unlocked,
                'ci': ci,
                'cui': cui,
                'cii': cii,
                'ref': ref
            }
            return data
        else:
            return 'hata'
    except:
        return 'hata'


def met_post(data):
    url = "https://met.bz/links/go"
    cookies = {
        " csrfToken": f"{data['csrf_token']}",
        "visitor": f"{data['visitor_data']}"}
    headers = {
        "Connection": "close",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://met.bz",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://met.bz/{data['code']}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    datam = {
        "_method": "POST",
        "_csrfToken": f"{data['csrf_token']}",
        "alias": f"{data['code']}",
        "ci": f"{data['ci']}",
        "cui": f"{data['cui']}",
        "cii": f"{data['cii']}",
        "ref": f"{data['ref']}",
        "_Token[fields]": f"{data['token_fields']}",
        "_Token[unlocked]": f"{data['token_unlocked']}"
    }
    r = requests.post(url, headers=headers, cookies=cookies, data=datam)
    try:
        veriler = r.json()
        data = {
            'status': veriler['status'],
            'message': veriler['message'],
            'finish_url': veriler['url']
        }
        return data
    except:
        return 'hata'
