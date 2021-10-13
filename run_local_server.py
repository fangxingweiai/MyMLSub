import os

from flask import Flask
from flask import make_response

app = Flask(__name__)

conf_folder = './conf'


@app.route('/')
def root():
    clients = ''
    if os.path.exists(conf_folder):
        clients = os.listdir(conf_folder)
    return f'支持的客户端：{", ".join(clients)}'


@app.route('/<client>/')
def sub(client):
    clients = ''
    if os.path.exists(conf_folder):
        clients = os.listdir(conf_folder)

    clients = list(map(lambda x: x.lower(), clients))

    sub = ''
    if client in clients:
        with open(f'{conf_folder}/{client}', 'r') as f:
            sub = f.read()

    # Content-Type: text/plain; charset=utf-8
    resp = make_response(sub, 200)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
