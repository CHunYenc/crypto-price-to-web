import json
from os import symlink
from flask_socketio import Namespace, emit, send
from flask import current_app
from app import redis as r


class MyCryptoPriceNamespace(Namespace):
    def on_connect(self):
        current_app.logger.info('connect.')
        exchange_list = r.keys('CRYPTO_*')
        current_app.logger.info(exchange_list)
        emit("get_exchange", [x.decode() for x in exchange_list])

    def on_disconnect(self):
        current_app.logger.info('disconnect.')

    def on_get_symbol(self, data):
        symbol_list = r.get(data["data"])
        symbol_list = json.loads(symbol_list)
        result = []
        for i in symbol_list:
            result.append(i)
        emit("get_symbol", result)

    def on_get_symbol_data(self, data):
        exchange = str.upper(f"{data['exchange']}")
        queryset = r.get(f'{exchange}')
        result = json.loads(queryset)
        emit("get_symbol_data", result[data['symbol']], broadcast=True)