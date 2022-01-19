import os

from flask import Flask
from flask import make_response

import settings

app = Flask(__name__)


@app.route('/')
def root():
    clients = ''
    if os.path.exists(settings.conf_dir):
        clients = os.listdir(settings.conf_dir)
    return f'支持的客户端：{", ".join(clients)}'


@app.route('/<client>/')
def sub(client):
    clients = ''
    if os.path.exists(settings.conf_dir):
        clients = os.listdir(settings.conf_dir)

    sub = ''
    if client in clients:
        with open(f'{settings.conf_dir}/{client}', 'r') as f:
            sub = f.read()

    resp = make_response(sub, 200)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
