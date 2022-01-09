from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, config
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from config import config
from functions import getBinance
from datetime import datetime

# from flask_cors import CORS

# initialize
app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

# create app
if app.config["ENV"] == "production":
    app.config.from_object(config["pro"])
else:
    app.config.from_object(config["dev"])

db = SQLAlchemy()
db.init_app(app)
# 切記一定要指定 timezone，反則會跳出多於訊息
scheduler = APScheduler(scheduler=BackgroundScheduler(timezone="Asia/Taipei"))


@scheduler.task("interval", id="get_symbol_price", seconds=10, max_instances=1)
def job1():
    print(f"== {datetime.now()} get_symbol_price 排程開始")
    with app.app_context():
        sql = "SELECT *" \
              "FROM focus_symbol"
        symbol_lists = db.engine.execute(sql)
        for i in symbol_lists:
            symbol = i[2]
            data = getBinance.get_binance_all_symbol_price(symbol)
            sql = f"INSERT INTO crypto_price (exchange, symbol, price, create_time) VALUES('Binance', '{symbol}', {data['price']},'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');"
            result = db.engine.execute(sql)
            result.close()
        symbol_lists.close()
    print(f"== {datetime.now()} get_symbol_price 排程結束")


scheduler.start()

if __name__ == "__main__":
    app.run()
