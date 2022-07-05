import json
from os import symlink
from flask_socketio import Namespace, emit, send

from app import socketio, app, redis as r


class MyCryptoPriceNamespace(Namespace):
    def on_connect(self):
        app.logger.info('connect.')
        exchange_list = r.keys('CRYPTO_*')
        print(exchange_list)
        emit("get_exchange", exchange_list)

    def on_disconnect(self):
        app.logger.info('disconnect.')

    def on_get_symbol(self, data):
        symbol_list = r.get(data["data"])
        symbol_list = json.loads(symbol_list)
        result = []
        for i in symbol_list:
            result.append(i)
        emit("get_symbol", result)