import sys
import unittest
from . import BaseTestCase, logger


class Test(BaseTestCase):
    def test_create_app(self):
        """ test online """
        client = self.app.test_client()
        response = client.get('/')
        logger.info(f'response = {response}')
        self.assertEqual(response.status_code, 200)
        assert b'test' in response.data

    def test_views_symbol_price_exchange_error(self):
        """ test exchange variable """
        client = self.app.test_client()
        response = client.get('/fake/btc/usdt')
        self.assertEqual(response.status_code, 404)

    def test_views_symbol_price_normal(self):
        """ test symbol variable """
        sys.setrecursionlimit(3000)
        client = self.app.test_client()
        response = client.get('/binance/btc/usdt')
        self.assertEqual(response.status_code, 200)

    def test_views_symbol_price_unnormal(self):
        sys.setrecursionlimit(3000)
        client = self.app.test_client()
        response = client.get('/binance/abc/def')
        logger.info(f'data = {response.status_code}')
        self.assertEqual(response.status_code, 404)

    def test_socketio(self):
        client = self.socketio.test_client(self.app)
        client2 = self.socketio.test_client(self.app)
        self.assertTrue(client.is_connected())
        self.assertTrue(client2.is_connected())
        self.assertNotEqual(client.eio_sid, client2.eio_sid)
        # self.assertEqual()
    # def test_get_binance_tickers(self):
    #     from app.tasks import get_binance_tickers, make_redis
    #     app = self.create_app('development')
    #     redis = make_redis(app)


if __name__ == '__main__':
    unittest.main()
