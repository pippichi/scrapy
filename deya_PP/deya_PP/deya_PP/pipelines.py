# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pandas as pd
import os

from deya_PP.properties import PP_AIM_FILE, PE_AIM_FILE
from deya_PP.tools import gen_temp_file, gen_aim_file, gen_excel_and_sheet, send_email


class DeyaPpPipeline(object):

    def __init__(self):
        self.today = datetime.date.today()

    def process_item(self, item, spider):
        # PP
        if len(item['title']) == 5:
            pp_middle_file_name, pp_origin_excel, pp_origin_excel_sheet = gen_excel_and_sheet("PP", self.today)
            df = gen_temp_file(item, pp_middle_file_name)
            additional_content = list(pd.read_excel('爬虫-PP.xlsx', sheet_name='Sheet1', index_col=False)['石化名称备注'])
            gen_aim_file('PP排号', additional_content, df, pp_origin_excel_sheet.max_column, pp_origin_excel, pp_origin_excel_sheet, PP_AIM_FILE, "PP")

        # PE
        if len(item['title']) == 7:
            pe_middle_file_name, pe_origin_excel, pe_origin_excel_sheet = gen_excel_and_sheet("PE", self.today)
            df = gen_temp_file(item, pe_middle_file_name)
            additional_content = list(pd.read_excel('爬虫备注-PE排产 (1).xlsx', sheet_name="Sheet1", index_col=False)['企业名称备注2'])
            gen_aim_file('PE排号', additional_content, df, pe_origin_excel_sheet.max_column, pe_origin_excel, pe_origin_excel_sheet, PE_AIM_FILE, "PE")
        return item

    def close_spider(self, spider):
        file_path_list = []
        if os.path.exists(PP_AIM_FILE):
            file_path_list.append(PP_AIM_FILE)
        if os.path.exists(PE_AIM_FILE):
            file_path_list.append(PE_AIM_FILE)
        send_email(file_path_list)
        if len(file_path_list) > 0:
            for f in file_path_list:
                os.remove(f)
