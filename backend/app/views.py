import json

from flask import Blueprint, render_template, current_app
# from app.models import *
from flask_socketio import emit

from app import redis as r, socketio  # , db

simple_page = Blueprint('', __name__,
                        template_folder='templates')


@simple_page.route("/")
def index():
    return f"目前執行環境：{current_app.config['ENV']} <br> Connect Status is OK!"


@simple_page.route("/<string:exchange>/<string:symbol_A>/<string:symbol_B>")
def symbol_price(exchange, symbol_A, symbol_B):
    exchange = str.upper(f"CRYPTO_{exchange}")
    data = r.get(f'{exchange}')
    result = json.loads(data)
    return render_template(
        "price.html",
        data=result[f'{symbol_A}/{symbol_B}']
    )


@simple_page.route("/socket")
def symbol_price_socket():
    return render_template("price_s.html")
