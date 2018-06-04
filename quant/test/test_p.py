# ae_h - 2018/6/4

import tushare as ts
from sqlalchemy import create_engine, MetaData

from quant.config import default_config
from quant.dao import dataSource
from quant.dao.k_data_tech_feature_dao import k_data_tech_feature_dao
from quant.common_tools.datetime_utils import get_current_date

def init_db():
    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=100, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine
        dataSource.mysql_quant_conn = mysql_quant_engine.connect()
        dataSource.mysql_quant_metadata = MetaData(dataSource.mysql_quant_conn)

init_db()

df = k_data_tech_feature_dao.get_k_data('000568', start='2018-06-01', end='2018-06-04')
df.to_csv('result.csv')