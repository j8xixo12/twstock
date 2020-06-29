# -*- coding: utf-8 -*-

import twstock


def run(argv):
    for sid in argv:
        s = twstock.Stock(sid)
        print('-------------- %s ---------------- ' % sid)
        print('high : {:>5} {:>5} {:>5} {:>5} {:>5}'.format(*s.high.iloc[-5:, 0]))
        print('low  : {:>5} {:>5} {:>5} {:>5} {:>5}'.format(*s.low.iloc[-5:, 0]))
        print('price: {:>5} {:>5} {:>5} {:>5} {:>5}'.format(*s.price.iloc[-5:, 0]))
