# coding = utf-8
# ae_h - 2018/5/29

import unittest

from common_tools import datetime_utils
from dao.k_data_60m.index_k_data_60m_dao import index_k_data_60m_dao
from dao.k_data_60m.k_data_60m_dao import k_data_60m_dao
from log.quant_logging import logger
from models.pca_model import PCAModel
from test import before_run

from models.k_data_60m.sequantial_neural_classifier import SequantialNeuralClassifier


class Sequantial_Neural_classifier_60m_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600276'

        data, features = k_data_60m_dao.get_k_data_with_features(code, '2015-01-01', datetime_utils.get_current_date())

        pac = PCAModel('k_data_60m');
        pac.training_model(code=code, data=data, features=features)

        model = SequantialNeuralClassifier()
        model.training_model(code, data, features)

    def test_predict(self):
        code='600704'

        df_index = index_k_data_60m_dao.get_rel_price();
        df, features = k_data_60m_dao.get_k_predict_data_with_features(code, df_index)
        logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = SequantialNeuralClassifier()
        y_predict = model.predict(code, df[features])

        logger.debug("predict:%s" % y_predict)