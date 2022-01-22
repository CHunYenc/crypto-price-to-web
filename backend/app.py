from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc
from config import config

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


@app.route('/')
def index():
    return "Connect Status is OK!"

@app.route('/add/<string:symbol>')
def add_symbol(symbol):
    with app.app_context():
        sql = f"INSERT INTO focus_symbol (exchange, symbol) VALUES('binance', '{symbol}');"
        try:
            result = db.engine.execute(sql)
            print(result)
        except exc.OperationalError:
            return "資料庫連線失敗"
        else:
            result.close()
    return "新增成功, 已加入排程抓取資料"


@app.route("/<string:exchange>/<string:symbol>")
def symbol_price(exchange, symbol):
    query_data = (
        CryptoPrice.query.filter_by(exchange=exchange, symbol=symbol)
            .order_by(CryptoPrice.create_time.desc())
            .first()
    )

    return render_template(
        "price.html",
        data={
            "symbol": query_data.symbol,
            "price": query_data.price,
            "update_time": query_data.create_time,
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
