from flask import Flask, request
from flask_cors import CORS
from .log_config import configure_logging
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['REMOTE_URL'] = os.environ['REMOTE_URL']
app.config['SESSION_COOKIE_PATH'] = '/'
CORS(app, resources={
    # r"/moderation/check2": {
    #     "origins": "https://chat.openai.com",
    #     "allow_headers": ["Content-Type", "X-Chat-Url"]
    # }
    r"*": {
        "origins": "*",
        "allow_headers": ["Content-Type", "X-Chat-Url"]
    }
})
configure_logging(app)

# ルーティングをインポート
from . import barcode

@app.context_processor
def inject_common_variables():
    return dict(remote_url=app.config['REMOTE_URL'])
    # 必要に応じて他の変数も辞書に追加します。

def get_locale():
    # return request.accept_languages.best_match(['ja', 'fr', 'de', 'es', 'ko', 'pt', 'uk', 'zh_CN', 'zh_TW'])  # , 'ja_JP', 'en'
    return request.accept_languages.best_match(['ja'])

@app.before_request
def set_application_root():
    '''
    アプリケーションルートを設定
    '''
    request.environ['SCRIPT_NAME'] = app.config['APPLICATION_ROOT']

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')
