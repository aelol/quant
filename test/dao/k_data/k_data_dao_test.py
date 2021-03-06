import unittest

from common_tools.datetime_utils import get_next_date, get_current_date
from config import default_config
import futuquant as ft
from dao.k_data.k_data_dao import k_data_dao
from feature_utils.momentum_indicators import cal_macd


class K_Data_Dao_Test(unittest.TestCase):
    def setUp(self):
        # before_run()
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST, port=default_config.FUTU_OPEND_PORT)

    def test_get_k_data(self):

        df = k_data_dao.get_k_data(code = "600196", start="2018-01-02", end="2018-01-06")
        print(df)
        self.assertIsNotNone(df)

    def get_multiple_k_data(self):

        df = k_data_dao.get_multiple_k_data(code_list = ["601398", '600196', '000001'], start="2018-07-02", end="2018-07-28")
        print(df)
        self.assertIsNotNone(df)


    def test_get_trading_days(self):
        df = k_data_dao.get_trading_days(start="2015-01-01", end="2018-05-27", futu_quote_ctx= self.futu_quote_ctx)
        print(df)
        self.assertIsNotNone(df)

    def test_get_market_snapshot(self):
        df = k_data_dao.get_market_snapshot(code_list=['600196', '601398'], futu_quote_ctx= self.futu_quote_ctx)
        print(df)

    def test_get_last_macd_cross_point(self):
        df = k_data_dao.get_k_data(code = "601668", start=get_next_date(-120), end=get_current_date())
        df = df.join(cal_macd(df))
        item = k_data_dao.get_last_macd_cross_point(df, window_size=8)

        print(item)

    def tearDown(self):
        self.futu_quote_ctx.close()

    '''
    def test_get_k_data_with_features(self):
        df, feature = k_data_dao.get_k_data_with_features("600000", start="2015-01-01", end="2018-06-30")
        df.to_csv("result.csv")
        logger.debug("features:%s" % feature)

    def test_get_k_predict_data_with_features(self):
        df_index = index_k_data_dao.get_rel_price();

        df, features = k_data_dao.get_k_predict_data_with_features('600000', df_index)
        print(features)
        df.to_csv("result.csv")
        logger.debug(df.tail())

    def test_rolling_tree_days(self):
        data = k_data_dao.get_k_data("600196", start="2018-06-01", end="2018-07-10", cal_next_direction=True)
        #next_3 = pd.Series(pd.Series.rolling(data['p_change'], 3).sum(), name='next_p_change_3')
        #data = data.join(next_3)
        #data['next_p_change_3'] = data['next_p_change_3'].shift(-3)
        #data['next_direction_3'] = data['next_p_change_3'].apply(cal_direction, i=0.03)
        print(data)

    '''