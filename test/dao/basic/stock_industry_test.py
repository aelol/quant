import unittest
from dao.k_data.index_k_data_dao import index_k_data_dao
from log.quant_logging import logger
from test import before_run
from dao.basic.stock_industry_dao import stock_industry_dao


class StockIndustryDaoTest(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_get_list(self):
        df = stock_industry_dao.get_list()
        logger.debug(df.head())
