import json
from math import fabs

from flask import Blueprint, render_template, current_app as app, abort

from app import make_redis

simple_page = Blueprint('', __name__,
                        template_folder='templates')

r = make_redis(app)


@simple_page.route("/")
def index():
    return render_template("index.html", data={"env": app.config['ENV']})


@simple_page.route("/<string:exchange>/<string:symbol_A>/<string:symbol_B>")
def symbol_price(exchange, symbol_A, symbol_B):
    c_exchange = str.upper(f"CRYPTO_{exchange}")
    symbol_A = str.upper(symbol_A)
    symbol_B = str.upper(symbol_B)
    r_data = r.get(f'{c_exchange}')
    # system not exchange data
    if r_data is None:
        abort(404)
    result = json.loads(r_data)
    symbol_data = result.get(f'{symbol_A}/{symbol_B}',
                             f"the symbol : {symbol_A}/{symbol_B} not exist.")
    exist = True if type(symbol_data) is dict else False
    # system not symbol data
    if not exist:
        abort(404)

    data = {"data": symbol_data, "exchange":exchange.upper()}
    return render_template("price.html", data=data)


@simple_page.route("/socket")
def symbol_price_socket():
    return render_template("price_s.html")
