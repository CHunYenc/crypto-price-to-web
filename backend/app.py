from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc
from config import config
import json
import redis

# initialize
app = Flask(__name__)

# create app
if app.config["ENV"] == "production":
    app.config.from_object(config["pro"])
else:
    app.config.from_object(config["dev"])

db = SQLAlchemy(app)

Migrate = Migrate(app, db)

from models import *

r = redis.from_url(app.config['CACHE_REDIS_URL'])

@app.route("/")
def index():
    return "Connect Status is OK!"


@app.route("/add/<string:exchange>/<string:symbol>")
def add_symbol(exchange, symbol):
    exchange = str.lower(exchange)
    symbol = str.upper(symbol)
    query = FocusSymbol(exchange=exchange, symbol=symbol)
    db.session.add(query)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "新增失敗, 資料庫連線失敗", 400
    else:
        return "新增成功", 200
    finally:
        db.session.close()



@app.route("/<string:exchange>/<string:symbol>")
def symbol_price(exchange, symbol):
    exchange_name = str.lower(exchange)
    symbol_name = str.upper(symbol)
    data = r.get(f'{exchange_name}_{symbol_name}')
    print(data)
    result = json.loads(data)

    # result =
    # {'symbol': 'BTCUSDT', 'priceChange': '68.35000000', 'priceChangePercent': '0.181',
    #  'weightedAvgPrice': '38006.69916863', 'prevClosePrice': '37841.26000000', 'lastPrice': '37909.61000000',
    #  'lastQty': '0.00179000', 'bidPrice': '37909.61000000', 'bidQty': '1.11443000', 'askPrice': '37909.62000000',
    #  'askQty': '0.06278000', 'openPrice': '37841.26000000', 'highPrice': '38720.74000000', 'lowPrice': '37268.44000000',
    #  'volume': '26491.90779000', 'quoteVolume': '1006869969.77755200', 'openTime': 1643461058345,
    #  'closeTime': 1643547458345, 'firstId': 1240333233, 'lastId': 1241145111, 'count': 811879}

    return render_template(
        "price.html",
        data=result
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
