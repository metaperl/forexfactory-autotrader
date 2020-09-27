import pymt5adapter as pymt5
from pymt5adapter.order import Order
from pymt5adapter.symbol import Symbol

from loguru import logger

import logging

class MySymbol:

    def get_symbol(s):
        s = s.replace('/', '')
        logger.debug(f"Looking for symbol {s}")
        return Symbol(s)


def order_method(direction):
    order_method = dict(sell=Order.as_sell, buy=Order.as_buy)
    direction = direction.lower()
    return order_method[direction]

def market_order(trade):

    my_logger = pymt5.get_logger(loglevel=logging.DEBUG, path_to_logfile='./logfile.txt')


    with pymt5.connected(
        ensure_trade_enabled=True,
        enable_real_trading=True,
    ) as conn:

        symbol = MySymbol.get_symbol(trade.symbol)
        # alt constructor
        order = order_method(trade.direction)(
            volume=0.01,
            expiration=pymt5.ORDER_TIME.DAY,
            symbol=symbol.name,
            server='AAFX-DEMO',
            login=9015,
            password='a1SkwRBUyc',
            logger=my_logger,
        )

        res = order.send()
        retcode = pymt5.TRADE_RETCODE(res.retcode)
        if retcode is pymt5.TRADE_RETCODE.DONE:
            print('done')
            return res.order
        else:
            print('trade error', pymt5.trade_retcode_description(retcode))

