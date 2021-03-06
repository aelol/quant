# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06

from crawler.east_money_api import east_money_api
from dao.data_source import dataSource

from common_tools.decorators import exc_time, error_handler



@exc_time
@error_handler
def collect_all():

    df_industry = east_money_api.get_industry_all()
    for index,row in df_industry.iterrows():
        data = east_money_api.get_stock_industry_by_bk_code(row["code"], row["name"])
        data.to_sql('stock_industry', dataSource.mysql_quant_engine, if_exists='append', index=False)

    collect_concept_board()

def collect_concept_board():
    dict = east_money_api.get_concept_board()
    for k, v in dict.items():
        data = east_money_api.get_stock_industry_by_bk_code(k[:-1], v)
        data.to_sql('stock_industry', dataSource.mysql_quant_engine, if_exists='append', index=False)