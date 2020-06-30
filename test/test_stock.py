import datetime
import unittest
from twstock import stock
import pandas as pd


class FetcherTest(object):
    def test_convert_date(self):
        date = '106/05/01'
        cv_date = self.fetcher._convert_date(date)
        self.assertEqual(cv_date, '2017/05/01')

    def test_make_datatuple(self):
        data = ['106/05/02', '45,851,963', '9,053,856,108', '198.50',
                '199.00', '195.50', '196.50', '+2.00', '15,718']
        dt = self.fetcher._make_datatuple(data)
        self.assertEqual(dt.date, datetime.datetime(2017, 5, 2))
        self.assertEqual(dt.capacity, 45851963)
        self.assertEqual(dt.turnover, 9053856108)
        self.assertEqual(dt.open, 198.5)
        self.assertEqual(dt.high, 199.0)
        self.assertEqual(dt.low, 195.5)
        self.assertEqual(dt.close, 196.5)
        self.assertEqual(dt.change, 2.0)
        self.assertEqual(dt.transaction, 15718)

    def test_make_datatuple_without_prices(self):
        data = ['106/05/02', '45,851,963', '9,053,856,108', '--',
                '--', '--', '--', ' 0.00', '15,718']
        dt = self.fetcher._make_datatuple(data)
        self.assertEqual(dt.date, datetime.datetime(2017, 5, 2))
        self.assertEqual(dt.capacity, 45851963)
        self.assertEqual(dt.turnover, 9053856108)
        self.assertEqual(dt.open, None)
        self.assertEqual(dt.high, None)
        self.assertEqual(dt.low, None)
        self.assertEqual(dt.close, None)
        self.assertEqual(dt.change, 0.0)
        self.assertEqual(dt.transaction, 15718)


class TWSEFetcerTest(unittest.TestCase, FetcherTest):
    fetcher = stock.TWSEFetcher()


class TPEXFetcherTest(unittest.TestCase, FetcherTest):
    fetcher = stock.TPEXFetcher()

    def test_make_datatuple(self):
        data = ['106/05/02', '45,851', '9,053,856', '198.50',
                '199.00', '195.50', '196.50', '2.00', '15,718']
        dt = self.fetcher._make_datatuple(data)
        self.assertEqual(dt.date, datetime.datetime(2017, 5, 2))
        self.assertEqual(dt.capacity, 45851000)
        self.assertEqual(dt.turnover, 9053856000)
        self.assertEqual(dt.open, 198.5)
        self.assertEqual(dt.high, 199.0)
        self.assertEqual(dt.low, 195.5)
        self.assertEqual(dt.close, 196.5)
        self.assertEqual(dt.change, 2.0)
        self.assertEqual(dt.transaction, 15718)

    def test_make_datatuple_without_prices(self):
        data = ['106/05/02', '45,851', '9,053,856', '--',
                '--', '--', '--', '0.00', '15,718']
        dt = self.fetcher._make_datatuple(data)
        self.assertEqual(dt.date, datetime.datetime(2017, 5, 2))
        self.assertEqual(dt.capacity, 45851000)
        self.assertEqual(dt.turnover, 9053856000)
        self.assertEqual(dt.open, None)
        self.assertEqual(dt.high, None)
        self.assertEqual(dt.low, None)
        self.assertEqual(dt.close, None)
        self.assertEqual(dt.change, 0.0)
        self.assertEqual(dt.transaction, 15718)

    def test_make_datatuple_with_asterisk(self):
        data = ['106/05/02＊', '45,851', '9,053,856', '198.50',
                '199.00', '195.50', '196.50', '2.00', '15,718']
        dt = self.fetcher._make_datatuple(data)
        self.assertEqual(dt.date, datetime.datetime(2017, 5, 2))
        self.assertEqual(dt.capacity, 45851000)
        self.assertEqual(dt.turnover, 9053856000)
        self.assertEqual(dt.open, 198.5)
        self.assertEqual(dt.high, 199.0)
        self.assertEqual(dt.low, 195.5)
        self.assertEqual(dt.close, 196.5)
        self.assertEqual(dt.change, 2.0)
        self.assertEqual(dt.transaction, 15718)


class StockTest(object):
    def test_fetch_31(self):
        self.stk.fetch_31()
        self.assertEqual(len(self.stk.data), 31)
        self.assertEqual(len(self.stk.price), 31)

    def test_date(self):
        self.assertIsInstance(self.stk.date, list)
        self.assertEqual(len(self.stk.date), len(self.stk.data))
        self.assertEqual(self.stk.date, [d.date for d in self.stk.data])

    def test_capacity(self):
        self.assertIsInstance(self.stk.capacity, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.capacity), len(self.stk.data))
        self.assertEqual(self.stk.capacity, pd.DataFrame([d.capacity for d in self.stk.data], columns = [self.stk.data[0]._fields[1]]))

    def test_turnover(self):
        self.assertIsInstance(self.stk.turnover, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.turnover), len(self.stk.data))
        self.assertEqual(self.stk.turnover, pd.DataFrame([d.turnover for d in self.stk.data], columns = [self.stk.data[0]._fields[2]]))

    def test_price(self):
        self.assertIsInstance(self.stk.price, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.price), len(self.stk.data))
        self.assertEqual(self.stk.price, pd.DataFrame([d.close for d in self.stk.data], columns = [self.stk.data[0]._fields[6]]))

    def test_high(self):
        self.assertIsInstance(self.stk.high, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.high), len(self.stk.data))
        self.assertEqual(self.stk.high, pd.DataFrame([d.high for d in self.stk.data], columns = [self.stk.data[0]._fields[4]]))

    def test_low(self):
        self.assertIsInstance(self.stk.low, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.low), len(self.stk.data))
        self.assertEqual(self.stk.low, pd.DataFrame([d.low for d in self.stk.data], columns = [self.stk.data[0]._fields[5]]))

    def test_open(self):
        self.assertIsInstance(self.stk.open, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.open), len(self.stk.data))
        self.assertEqual(self.stk.open, pd.DataFrame([d.open for d in self.stk.data], columns = [self.stk.data[0]._fields[3]]))

    def test_close(self):
        self.assertIsInstance(self.stk.close, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.close), len(self.stk.data))
        self.assertEqual(self.stk.close, pd.DataFrame([d.close for d in self.stk.data], columns = [self.stk.data[0]._fields[6]]))

    def test_change(self):
        self.assertIsInstance(self.stk.change, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.change), len(self.stk.data))
        self.assertEqual(self.stk.change, pd.DataFrame([d.change for d in self.stk.data], columns = [self.stk.data[0]._fields[7]]))

    def test_transaction(self):
        self.assertIsInstance(self.stk.transaction, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.transaction), len(self.stk.data))
        self.assertEqual(self.stk.transaction, pd.DataFrame([d.transaction for d in self.stk.data], columns = [self.stk.data[0]._fields[8]]))


class TWSEStockTest(unittest.TestCase, StockTest):
    @classmethod
    def setUpClass(cls):
        cls.stk = stock.Stock('2330')

    def test_price(self):
        self.stk.fetch(2015, 5)
        self.assertIsInstance(self.stk.price, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.price), len(self.stk.data))
        self.assertEqual(self.stk.price, pd.DataFrame([d.close for d in self.stk.data]))
        self.assertEqual(self.stk.price,
                         pd.DataFrame([147.5, 147.0, 147.5, 146.5, 146.5, 148.5, 147.5,
                          148.0, 146.0, 146.5, 146.5, 146.5, 146.5, 145.5,
                          145.5, 147.5, 146.5, 145.0, 147.0, 146.0], columns = ['price']))

    def test_capacity(self):
        self.stk.fetch(2015, 5)
        self.assertIsInstance(self.stk.capacity, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.capacity), len(self.stk.data))
        self.assertEqual(self.stk.capacity, pd.DataFrame([d.capacity for d in self.stk.data]))
        self.assertEqual(self.stk.capacity,
                         pd.DataFrame([30868640, 27789400, 18824208, 21908150, 20035646,
                          20402529, 24956498, 19437537, 39888654, 24831890,
                          26212375, 26321396, 26984912, 41286686, 22103852,
                          16323218, 16069726, 24257941, 36704395, 61983862], columns = ['capacity']))


class TPEXStockTest(unittest.TestCase, StockTest):
    @classmethod
    def setUpClass(cls):
        cls.stk = stock.Stock('6223')

    def test_price(self):
        self.stk.fetch(2015, 5)
        self.assertIsInstance(self.stk.price, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.price), len(self.stk.data))
        self.assertEqual(self.stk.price, pd.DataFrame([d.close for d in self.stk.data]))
        self.assertEqual(self.stk.price,
                         pd.DataFrame([91.4, 91.8, 91.8, 93.5, 91.0, 84.7, 84.0, 85.8, 87.1,
                          86.1, 83.9, 84.5, 86.7, 86.3, 86.0, 86.2, 91.1, 90.9,
                          91.7, 90.4], columns = ['price']))

    def test_capacity(self):
        self.stk.fetch(2015, 5)
        self.assertIsInstance(self.stk.capacity, pd.core.frame.DataFrame)
        self.assertEqual(len(self.stk.capacity), len(self.stk.data))
        self.assertEqual(self.stk.capacity, pd.DataFrame([d.capacity for d in self.stk.data]))
        self.assertEqual(self.stk.capacity,
                         pd.DataFrame([374000, 474000, 468000, 1257000, 1079000, 3400000,
                          3424000, 1078000, 1433000, 891000, 1202000, 1008000,
                          999000, 488000, 706000, 231000, 1890000, 782000,
                          1214000, 583000], columns = ['capacity']))
