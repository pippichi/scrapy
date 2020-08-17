# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

from sqlalchemy import create_engine

class DeyaResearchSpiderPipeline:
    df_market_price = pd.DataFrame()
    df_market_index = 0
    df_spider_17 = pd.DataFrame()
    df_spider_17_index = 0
    spider_17_dates = []
    date = ''
    con = create_engine(
        'mysql+pymysql://deya_research_dev:research123@192.168.1.183:3306/deya_research_dev?charset=utf8'
    )

    def process_item(self, item, spider):
        if (spider.name == 'Spider1516'):
            index = self.df_market_index
            standard_new_name = {
                '拉丝': '拉丝',
                '均聚注塑': '注塑',
                '纤维': '纤维',
                '共聚注塑': '低熔共聚'
            }
            self.date = item['date']
            if (item['price'] != '-' and item['price'] != '--' and item['price'] != ''):
                self.df_market_price.loc[index, 'specificationName'] = item['specificationName']
                self.df_market_price.loc[index, 'standard'] = standard_new_name[item['standard']]
                self.df_market_price.loc[index, 'date'] = item['date']
                self.df_market_price.loc[index, 'price'] = item['price']
                self.df_market_price.loc[index, 'regionName'] = item['regionName']
                self.df_market_index += 1
        elif (spider.name == 'Spider17'):
            date = item['date']
            if not(date in self.spider_17_dates):
                self.spider_17_dates.append(date)
            current_item = {
                'type': item['type'],
                'rank': item['rank'],
                'memberName': item['memberName'],
                'value': item['value'],
                'date': item['date'],
                'contract': item['contract'],
            }
            self.df_spider_17 = self.df_spider_17.append(current_item, ignore_index = True)
        return item

    def close_spider(self, spider):
        if (spider.name == 'Spider1516'):
            self.df_market_price['price'] = self.df_market_price['price'].astype(float)
            date_list = self.df_market_price['date'].unique()
            needs_region_and_standard = [
                {'region': '华东地区', 'standard': '拉丝', 'index_id': 64},
                {'region': '华东地区', 'standard': '注塑', 'index_id': 65},
                {'region': '华东地区', 'standard': '纤维', 'index_id': 66},
                {'region': '华东地区', 'standard': '低熔共聚', 'index_id': 67},
                {'region': '华北地区', 'standard': '拉丝', 'index_id': 68}
            ]
            for date in date_list:
                df_to_sql = pd.DataFrame()
                df_to_sql_index = 0
                current_df = self.df_market_price.loc[self.df_market_price['date'] == date]
                for content in needs_region_and_standard:
                    now_price = current_df.loc[
                        (current_df['regionName'] == content['region'])
                        & (current_df['standard'] == content['standard'])
                        & (current_df['price'] > 2000)
                        ]['price']
                    if (now_price.empty == False):
                        min_price = now_price.min()
                        df_to_sql.loc[df_to_sql_index, 'date'] = date
                        df_to_sql.loc[df_to_sql_index, 'value'] = min_price
                        df_to_sql.loc[df_to_sql_index, 'index_id'] = content['index_id']
                        df_to_sql_index += 1
                df_to_sql.to_sql(name="dy_pp_market_price", con=self.con, if_exists="append", index=False)

        elif (spider.name == 'Spider17'):
            self.df_spider_17['value'] = self.df_spider_17.loc[:, 'value'].apply(lambda x: float(x.replace(",", "")))
            df17_to_sql = pd.DataFrame()
            df17_to_sql_index = 0
            spider17_contract = ['01', '05', '09']
            spider17_type = ['持买单量', '持卖单量', '总持买单量', '总持卖单量']
            needs_17 = {
                '仓单量': 78,
                '01总持买单量': 79,
                '01总持卖单量': 82,
                '01持买单量1数值': 88,
                '01持买单量1会员': 85,
                '01持买单量2数值': 94,
                '01持买单量2会员': 91,
                '01持卖单量1数值': 100,
                '01持卖单量1会员': 97,
                '01持卖单量2数值': 106,
                '01持卖单量2会员': 103,
                '05总持买单量': 80,
                '05总持卖单量': 83,
                '05持买单量1数值': 89,
                '05持买单量1会员': 86,
                '05持买单量2数值': 95,
                '05持买单量2会员': 92,
                '05持卖单量1数值': 101,
                '05持卖单量1会员': 98,
                '05持卖单量2数值': 107,
                '05持卖单量2会员': 104,
                '09总持买单量': 81,
                '09总持卖单量': 84,
                '09持买单量1数值': 90,
                '09持买单量1会员': 87,
                '09持买单量2数值': 96,
                '09持买单量2会员': 93,
                '09持卖单量1数值': 102,
                '09持卖单量1会员': 99,
                '09持卖单量2数值': 108,
                '09持卖单量2会员': 105,
            }
            for date in self.spider_17_dates:
                current_date_df17 = self.df_spider_17.loc[self.df_spider_17['date'] == date]
                df17_cd = current_date_df17.loc[current_date_df17['type'] == '仓单量']
                if (df17_cd.empty != True):
                    df17_to_sql.loc[df17_to_sql_index, 'date'] = df17_cd.loc[0, 'date']
                    df17_to_sql.loc[df17_to_sql_index, 'value'] = df17_cd.loc[0, 'value']
                    df17_to_sql.loc[df17_to_sql_index, 'index_id'] = needs_17['仓单量']
                    df17_to_sql_index += 1
                for contract in spider17_contract:
                    df17_new = current_date_df17.loc[
                        current_date_df17['contract'] == contract
                    ]
                    if df17_new.empty != True:
                        for type in spider17_type:
                            df17_type_new = df17_new.loc[df17_new['type'] == type]
                            if (df17_type_new.empty != True):
                                if (type == '总持买单量' or type == '总持卖单量'):
                                    df17_type_new = df17_type_new.reset_index(drop=True)
                                    if (df17_type_new.loc[0, 'value'] != 0):
                                        df17_to_sql.loc[df17_to_sql_index, 'date'] = df17_type_new.loc[0, 'date']
                                        df17_to_sql.loc[df17_to_sql_index, 'value'] = df17_type_new.loc[0, 'value']
                                        df17_to_sql.loc[df17_to_sql_index, 'index_id'] = needs_17[contract + type]
                                        df17_to_sql_index += 1
                                else:
                                    df17_type_new.sort_values(by="value", axis=0, ascending=False, inplace=False)
                                    # 重置索引 从0开始
                                    df17_type_new = df17_type_new.reset_index(drop=True)
                                    for num in [1, 2]:
                                        df17_to_sql.loc[df17_to_sql_index, 'date'] = df17_type_new.loc[num - 1, 'date']
                                        df17_to_sql.loc[df17_to_sql_index, 'value'] = df17_type_new.loc[num - 1, 'value']
                                        df17_to_sql.loc[df17_to_sql_index, 'index_id'] = needs_17[contract + type + str(num) + '数值']
                                        df17_to_sql_index += 1
                                        df17_to_sql.loc[df17_to_sql_index, 'date'] = df17_type_new.loc[num - 1, 'date']
                                        df17_to_sql.loc[df17_to_sql_index, 'value'] = df17_type_new.loc[num - 1, 'memberName']
                                        df17_to_sql.loc[df17_to_sql_index, 'index_id'] = needs_17[contract + type + str(num) + '会员']
                                        df17_to_sql_index += 1

            df17_to_sql['index_id'] = df17_to_sql['index_id'].astype(int)
            df17_to_sql['value'] = df17_to_sql['value'].astype(str)
            df17_to_sql.to_sql(name="dy_index_data", con=self.con, if_exists="append", index=False)

