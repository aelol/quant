import os
import sys

from futuquant import StockQuoteHandlerBase, RET_OK, RET_ERROR

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

from dao.futu_opend import futu_opend
from dao.trade.target_dao import target_dao

# Append project path to system path
from dao.k_data import fill_market
from dao.trade.position_dao import position_dao

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def monitor():
    monitor_targets()
    monitor_positions()


def monitor_positions():
    position_all = position_dao.query_all()

    codes = [fill_market(p.code) for p in position_all]

    state, df = futu_opend.quote_ctx.get_stock_quote(codes)
    # 更新实时数据
    for index, row in df.iterrows():
        code = row['code'][3:]
        last_price = row['last_price']

        positions = [position for position in position_all if position.code == code]

        for position in positions:
            position.price = last_price

            profit = round((last_price / position.price_in - 1) * 100, 2)
            position.profit = profit
            position.worth = round(position.price * position.shares, 2)
            position.profit_value = round((position.price - position.price_in) * position.shares, 2)
            position.update_time = datetime.now()
            position_dao.update(position)


def monitor_targets():
    target_all = target_dao.query_all()
    codes = [fill_market(t.code) for t in target_all]

    state, df = futu_opend.quote_ctx.get_stock_quote(codes)
    # 更新实时数据
    for index, row in df.iterrows():
        code = row['code'][3:]
        targets = [target for target in target_all if target.code == code]

        for target in targets:
            last_price = row['last_price']
            target.price = last_price
            target.update_time = datetime.now()
            target_dao.update(target)


def subscribe_positions():
    positions = position_dao.query_all()
    codes = [fill_market(p.code) for p in positions]
    futu_opend.subscribe(codes)


def subscribe_targets():
    targets = target_dao.query_all()
    codes = [fill_market(t.code) for t in targets]
    futu_opend.subscribe(codes)


def subscribe_refresh():
    futu_opend.unsubscribe_all()
    subscribe_positions()
    subscribe_targets()


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(StockQuoteTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data

        print("StockQuoteTest ", data)  # StockQuoteTest自己的处理逻辑

        return RET_OK, data


if __name__ == '__main__':
    subscribe_positions()
    subscribe_targets()

    handler = StockQuoteTest()
    futu_opend.quote_ctx.set_handler(handler)

    '''


    scheduler = BlockingScheduler()
    scheduler.add_job(monitor, 'cron', day_of_week='0-4', hour='9-15', second='*/5')

    scheduler.add_job(subscribe_refresh, 'cron', day_of_week='0-4', hour='23')
    scheduler.start()
    '''
