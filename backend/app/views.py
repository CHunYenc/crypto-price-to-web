import json

from flask import Blueprint, render_template, current_app
# from app.models import *
from app import redis as r  # , db

simple_page = Blueprint('', __name__,
                        template_folder='templates')


@simple_page.route("/")
def index():
    return f"目前執行環境：{current_app.config['ENV']} <br> Connect Status is OK!"


@simple_page.route("/<string:exchange>/<string:symbol_A>/<string:symbol_B>")
def symbol_price(exchange, symbol_A, symbol_B):
    redis_key = f"{str.upper(exchange)}_{str.upper(symbol_A)}/{str.upper(symbol_B)}"
    data = r.get(f'{redis_key}')
    # print(data)
    result = json.loads(data)
    return render_template(
        "price.html",
        data=result
    )
