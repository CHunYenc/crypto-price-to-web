import logging
import sys
from unittest import TestCase

from flask_socketio import SocketIO

from app import create_app, socketio

logger = logging.getLogger()
logger.level = logging.DEBUG


class BaseTestCase(TestCase):
    """ reference https://ithelp.ithome.com.tw/articles/10274387 """

    def setUp(self):
        # 可不寫。測試前會執行的東西，相當於 pytest 中 @pytest.fixture 這個裝飾器
        # 可以用於生出一個乾淨(沒有資料)的資料庫之類的，不過因為我是用奇怪的方式弄出類似資料庫的東東，所以就沒有寫
        self.app = create_app('test')
        self.socketio = SocketIO(self.app)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(self.stream_handler)
        logger.info('=== add handler')

    def tearDown(self):
        # 可不寫。測試後會執行的東西，相當於 pytest 中 @pytest.fixture 這個裝飾器 function 內 yield 之後的程式
        # 可以用於刪除不乾淨(測試後被塞入資料)的資料庫之類的
        logger.info('=== remove handler')
        logger.removeHandler(self.stream_handler)

    @classmethod
    def setUpClass(self):
        # 可不寫。相當於 setUp ，不過不同於 setUp 是執行一個 Function ，而是先執行一個 Class，詳細用法參考 @classmethod 或是下面的網址
        # https://docs.python.org/zh-tw/3/library/unittest.html#unittest.TestCase.setUpClass
        pass

    @classmethod
    def tearDownClass(self):
        # 可不寫。相當於 tearDown ，不過 setUpClass 同樣為執行一個 Class，詳細用法參考 @classmethod 或是下面的網址
        # https://docs.python.org/zh-tw/3/library/unittest.html#unittest.TestCase.tearDownClass
        pass
