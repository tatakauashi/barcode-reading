from flask import session
from datetime import datetime
from typing import Tuple
import string, random, uuid, re, logging
from urllib.parse import urlparse, parse_qs
from enum import Enum

CHAT_NAME_NEW = '<New Chat>'

class TimeConstants(Enum):
    ONE_YEAR = 60 * 60 * 24 * 365   # 1年の秒数
    THREE_HOURS = 60 * 60 * 3  # 3時間の秒数
    FIVE_MINUTES = 60 * 5   # 5分の秒数

def get_query_param_from_url(url, param_name):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get(param_name, [None])[0]

def is_empty(s) -> bool:
    if (type(s) == str):
        s = s.strip()
        if s == '':
            return True
        if is_numeric(s):
            if int(s) != 0:
                return False
            return True
        return False
    return not bool(s)

def valid_datetime(dt) -> bool:
    try:
        # strptimeは文字列を日時オブジェクトに変換します
        # 引数には変換したい文字列とその形式を指定します
        datetime.strptime(dt, '%Y%m%d%H%M%S%f')
        return True
    except ValueError:
        # ValueErrorが発生した場合は、引数の文字列が指定した形式に従っていないことを意味します
        return False

def is_valid_uuid(uuid_str):
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj) == uuid_str  # 正しい形式のUUIDであればTrueを返す
    except ValueError:
        return False  # UUIDの形式でない場合はFalseを返す

def is_numeric(s) -> bool:
    return bool(s) and s.isdigit()

def get_current_time() -> str:
    return datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]

def get_display_time(s) -> str:
    # 入力の文字列を解析する
    dt = datetime.strptime(s, '%Y%m%d%H%M%S%f')

    # datetimeオブジェクトを任意の文字列形式に変換する
    # ここでは例として、'%Y-%m-%d %H:%M:%S'形式に変換するとします。
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def checkbox_to_save(c) -> int:
    if '1' == c:
        return True
    return False

def generate_random_string(length=48) -> str:
    # string.ascii_lettersには半角アルファベット（大文字小文字両方）が含まれています
    # string.digitsには0から9までの数字が含まれています
    characters = string.ascii_letters + string.digits

    # 指定した長さのランダムな文字列を生成
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

import re

def is_alnum(s) -> bool:
    return re.match(r'^[a-zA-Z0-9-_]*$', s) is not None

def is_alpha_digits(s, min, max, required=False) -> bool:
    if required:
        if is_empty(s):
            return False
    if not is_empty(s):
        if len(s) < min or len(s) > max or not is_alnum(s):
            return False
    return True

def remove_control_characters(input_string):
    # 制御文字を除去する正規表現パターン
    control_chars = ''.join(map(chr, list(range(0, 32)))) + ''.join(map(chr, list(range(127, 160))))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    return control_char_re.sub('', input_string)

def create_error_info(message = '', details = {}, status = 500, path = '', code = '') -> dict:
    '''
    エラーレスポンスを生成して返す。
    
    :param message: エラーメッセージを示す文字列。デフォルトは空文字。
    :param details: エラー詳細情報
    :param status: エラーのステータスを示す整数。デフォルトは500。
    :param path: エラーが発生したリソースのパスを示す文字列。デフォルトは空文字。
    :param code: エラーコードを示す文字列。デフォルトは空文字。
    :return: エラー情報を含む辞書。
    '''
    return {
        'error': {
            'code': code,
            'message': message,
            'status': status,
            'path': path,
            'details': details,
            'timestamp': datetime.utcnow().isoformat() + "Z"
        }
    }

def check_datetime_str(s: str) -> bool:
    app_logger = logging.getLogger('app_logger')
    app_logger.debug(f'@@@@@@@@@@ s=[{s}]')
    try:
        expire_datetime = None
        if len(s) == 14:
            app_logger.debug(f'@@@@@@@@@@ len(s)=14')
            expire_datetime = datetime.strptime(s, "%Y%m%d%H%M%S")
            app_logger.debug(f'@@@@@@@@@@ expire_datetime(14)=[{str(expire_datetime)}]')
        elif len(s) == 17:
            app_logger.debug(f'@@@@@@@@@@ len(s)=17')
            expire_datetime = datetime.strptime(s, "%Y%m%d%H%M%S%f")
            app_logger.debug(f'@@@@@@@@@@ expire_datetime(17)=[{str(expire_datetime)}]')
        
        if expire_datetime is not None:
            return True
    except:
        app_logger.debug(f'@@@@@@@@@@ except!')
        return False
