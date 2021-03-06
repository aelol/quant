# ae_h - 2018/5/28

import os

from common_tools.decorators import exc_time
from dao.k_data_60m.k_data_60m_model_log_dao import k_data_60m_model_log_dao
from log.quant_logging import logger
from models.base_model import BaseModel
from models.k_data_60m import MODULE_NAME
from sklearn import preprocessing
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV

from models.pca_model import PCAModel


class SupportVectorClassifier(BaseModel):
    module_name = MODULE_NAME
    model_name = "support_vector_classifier"

    @exc_time
    def training_model(self, code, data, features):
        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                            shuffle=False)

        tuned_parameters = [
            {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]

        # # tsne缩放
        # X_train = TSNE(n_components=2, learning_rate=100).fit_transform(X_train)
        # X_test = TSNE(n_components=2, learning_rate=100).fit_transform(X_test)

        # 网格搜寻最优参数
        grid = GridSearchCV(svm.SVC(), tuned_parameters, cv=None, n_jobs=-1)
        grid.fit(X_train, y_train)

        logger.debug(grid.best_estimator_)  # 训练的结果
        logger.debug("Support Vector Classifier's best score: %.4f" % grid.best_score_)  # 训练的评分结果

        support_vector_classifier = grid.best_estimator_
        # 使用训练数据, 重新训练
        support_vector_classifier.fit(X_train, y_train)

        # 使用测试数据对模型进评平分
        y_test_pred = support_vector_classifier.predict(X_test)

        # 在测试集中的评分
        test_score = accuracy_score(y_test, y_test_pred)
        logger.debug('test score: %.4f' % test_score)

        # 使用所有数据, 重新训练
        support_vector_classifier.fit(X, y)

        # 记录日志
        k_data_60m_model_log_dao.insert(code=code, name=self.model_name
                                    , best_estimator=grid.best_estimator_,
                                    train_score=grid.best_score_, test_score=test_score)

        # 输出模型
        joblib.dump(support_vector_classifier, self.get_model_path(code, self.module_name, self.model_name))

    @exc_time
    def predict(self, code, data):
        model_path = self.get_model_path(code, self.module_name, self.model_name)

        if not os.path.exists(model_path):
            logger.error('model not found, code is %s:' % code)
            return

        X = preprocessing.scale(data)
        pac = PCAModel(self.module_name).load(code)
        X = pac.transform(X)

        support_vector_classifier = joblib.load(model_path)

        y_pred = support_vector_classifier.predict(X)

        return int(y_pred[0])
