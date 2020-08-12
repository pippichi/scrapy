#! encoding=utf-8

import random
import re

import requests
import string

# 验证码识别
from datetime import datetime
from urllib.request import urlretrieve

import pymysql
import pytesseract
import requests
from PIL import Image


# 验证码识别
def code_verify(img_url, code_verify_url):
    urlretrieve(img_url, './code.png')
    image = Image.open('./code.png')
    content = pytesseract.image_to_string(image)
    res = requests.get(code_verify_url.format(code=content))
    return res


# 识别日期
def parse_date(date):
    pattern = re.compile(r'.*?(\d{4}-\d{2}-\d{2}) ')
    return re.search(pattern, date).group(1)

def insert_value(date, value, index_id):
    conn = pymysql.connect(
        host='192.168.1.183', port=3306, user='deya_research_dev', password='research123',
        database='deya_research_dev', charset='utf8'
    )
    cursor = conn.cursor()
    select_sql = 'select id from dy_index_data where date=%s and index_id=%s;'
    ret = cursor.execute(select_sql, [date, index_id])
    # 如果返回的id为0，说明数据库中没有该日该指标的数据，新增数据
    if ret == 0:
        insert_sql = 'insert into dy_index_data (date, value, index_id, created_at, updated_at) ' \
                     'values (%s, %s, %s, %s, %s);'
        cursor.execute(insert_sql, [date, value, index_id, datetime.now(), datetime.now()])
    # 如果返回id不为0，说明数据库中已存在该日该指标的数据，更新数据
    else:
        id = cursor.fetchone()
        update_sql = 'update dy_index_data set value=%s, updated_at=%s where id=%s;'
        cursor.execute(update_sql, [value, datetime.now(), id])

    conn.commit()
    cursor.close()
    conn.close()



headers ={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3622.0 Safari/537.36"
    }


def random_sentence(size):
    '''
    获取随机请求的id
    '''
    char_lists = string.ascii_lowercase + string.digits
    return ''.join(random.choice(char_lists) for _ in range(size))


def get_par(RequestId):
    '''
    获取post提交的参数
    '''
    url = f'https://plas.chem99.com/include/login.aspx?RequestId={RequestId}'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3622.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    res = requests.get(url=url, headers=headers).text
    __EVENTTARGET = 'ctl04'
    __EVENTARGUMENT = ''
    __VIEWSTATE = re.findall(r'id="__VIEWSTATE" value="(.*?)"', res)[0]
    __VIEWSTATEGENERATOR = re.findall(r'id="__VIEWSTATEGENERATOR" value="(.*?)"', res)[0]
    __EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION" value="(.*?)"', res)[0]
    data =  {
        '__EVENTTARGET': __EVENTTARGET,
        '__EVENTARGUMENT': __EVENTARGUMENT,
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': __EVENTVALIDATION,
        "chemname": "zjzhongcai",
        "chempwd": "zcqh123",
        "fl1": 0
    }
    return data

def get_zc_cookie():
    '''
    登陆，获取cookie
    '''
    RequestId = random_sentence(16)
    url_1 = f"https://plas.chem99.com/include/login.aspx?RequestId={RequestId}"
    data = get_par(RequestId)


    # 第一次请求
    res_1 = requests.post(url_1, data=data, headers=headers, allow_redirects=False)
    cookies_1 = res_1.cookies
    cookie_dict_1 = requests.utils.dict_from_cookiejar(cookies_1)
    url_2 = 'https:' + res_1.headers.get('Location')

    # 第二次请求
    res_2 = requests.get(url_2, headers=headers, cookies=cookie_dict_1,allow_redirects=False)
    url_3 = 'https:' + res_2.headers.get('Location')
    # 第三次请求
    res_3 = requests.get(url_3, headers=headers, cookies=cookie_dict_1, allow_redirects=False)
    url_4 = 'https://plas.chem99.com' + res_3.headers.get('Location')
    # 第4次请求
    res_4 = requests.get(url_4, headers=headers, cookies=cookie_dict_1 ,allow_redirects=False)


    return cookie_dict_1