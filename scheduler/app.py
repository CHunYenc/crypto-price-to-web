from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, config
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from config import config
from functions import getBinance, getCrypto
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


@scheduler.task("interval", id="get_symbol_price", seconds=10, max_instances=1)
def get_symbol_price():
    print(f"== {datetime.now()} get_symbol_price 排程開始")
    sql = "SELECT *" "FROM focus_symbol"
    with db.engine.connect() as connection:
        result = connection.execute(sql)
        for i in result:
            exchange_name = str.lower(i[1])
            symbol_A = str.upper(i[2])
            symbol_B = str.upper(i[3])
            if exchange_name == "BINANCE".lower():
                data = getBinance.get_binance_specify_symbol_price(f'{symbol_A}{symbol_B}')
                # print(data)
                if "code" in data:
                    # print(f"binance isn't [], {data}")
                    sql = f"DELETE FROM focus_symbol WHERE id={i[0]};"
                    detail_result = connection.execute(sql)
                    detail_result.close()
                else:
                    # print(f"binance is [], {data}")
                    r.set(f"{exchange_name}_{symbol_A}/{symbol_B}", json.dumps(data))
            elif exchange_name == "CRYPTO".lower():
                data = getCrypto.get_crypto_specify_symbol_price(f'{symbol_A}_{symbol_B}')
                if data["result"]["data"] is not []:
                    # print(f"crypto.com isn't [], {data}")
                    r.set(f"{exchange_name}_{symbol_A}/{symbol_B}", json.dumps(data))
                else:
                    # print(f"crypto.com is [], {data}")
                    sql = f"DELETE FROM focus_symbol WHERE id={i[0]};"
                    detail_result = connection.execute(sql)
                    detail_result.close()
        result.close()
        connection.close()
    print(f"== {datetime.now()} get_symbol_price 排程結束")


scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
