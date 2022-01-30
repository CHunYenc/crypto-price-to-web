from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, config
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from config import config
from functions import getBinance
from datetime import datetime
import redis
import json

# from flask_cors import CORS

# initialize
app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

# create app
if app.config["ENV"] == "production":
    app.config.from_object(config["pro"])
else:
    app.config.from_object(config["dev"])

db = SQLAlchemy(app)
# 切記一定要指定 timezone，反則會跳出多於訊息
scheduler = APScheduler(scheduler=BackgroundScheduler(timezone="Asia/Taipei"))

r = redis.from_url(app.config['CACHE_REDIS_URL'])
r.ping()


@scheduler.task("interval", id="get_symbol_price", seconds=10, max_instances=1)
def get_symbol_price():
    print(f"== {datetime.now()} get_symbol_price 排程開始")
    sql = "SELECT *" "FROM focus_symbol"
    with db.engine.connect() as connection:
        result = connection.execute(sql)
        for i in result:
            exchange_name = str.lower(i[1])
            symbol_name = str.upper(i[2])
            if exchange_name == "binance":
                data = getBinance.get_binance_specify_symbol_price(symbol_name)
                r.set(f"{exchange_name}_{data['symbol']}", json.dumps(data))
        result.close()
    print(f"== {datetime.now()} get_symbol_price 排程結束")


scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)
