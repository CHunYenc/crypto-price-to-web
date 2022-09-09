FROM python:3.7-slim

COPY . /app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    freetds-dev \
    libpq-dev
    # postgresql-client \
    # postgresql-client-common

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","wsgi.py"]
# uwsgi
# CMD ["uwsgi", "app.ini"] 

# 1. 使用哪一個 image
# 2. 建立工作目錄
# 3. 複製指定的檔案 到容器中的指定位置
# 4. 執行 pip install -r requirements.txt
# 5. 執行 app.py