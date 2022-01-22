from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
def add_symbol():
    with app.app_context():
        sql = "SELECT *" \
              "FROM focus_symbol"
        symbol_lists = db.engine.execute(sql)
        sql = f"INSERT INTO crypto_price (exchange, symbol, price, create_time) VALUES('Binance', '{symbol}', {data['price']},'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
        result = db.engine.execute(sql)
        result.close()
        symbol_lists.close()
    return "新增成功"


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
